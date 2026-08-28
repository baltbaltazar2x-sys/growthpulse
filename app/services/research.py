import os
import shlex
import subprocess
import tempfile
from pathlib import Path

import httpx


class ResearchService:
    """Orchestrates Agent Reach + PixelRAG without coupling GrowthPulse to either codebase."""

    def __init__(self):
        self.agent_reach = os.getenv("AGENT_REACH_COMMAND", "agent-reach")
        self.pixelrag_url = os.getenv("PIXELRAG_URL", "").rstrip("/")
        self.pixelshot = os.getenv("PIXELSHOT_COMMAND", "pixelshot")
        self.timeout = float(os.getenv("RESEARCH_TIMEOUT_SECONDS", "120"))

    def run(self, url: str, query: str) -> dict:
        source = self._agent_reach(url, query)
        visual = self._pixelrag(url, query)
        return {
            "url": url,
            "query": query,
            "source": source,
            "visual_retrieval": visual,
            "pipeline": ["agent-reach", "pixelrag", "growthpulse"],
        }

    def _agent_reach(self, url: str, query: str) -> dict:
        """Run the configured Agent Reach executable and capture JSON/text output.

        The exact upstream CLI is intentionally not hard-coded here; Agent Reach can
        change installation and channel-specific commands independently of GrowthPulse.
        """
        command = shlex.split(self.agent_reach)
        if not command:
            return {"status": "not_configured"}
        try:
            completed = subprocess.run(
                command + [url, query],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )
            return {
                "status": "ok" if completed.returncode == 0 else "error",
                "returncode": completed.returncode,
                "output": completed.stdout[-20000:],
                "error": completed.stderr[-5000:],
            }
        except FileNotFoundError:
            return {"status": "unavailable", "reason": f"Command not found: {command[0]}"}
        except subprocess.TimeoutExpired:
            return {"status": "timeout"}

    def _pixelrag(self, url: str, query: str) -> dict:
        if self.pixelrag_url:
            return self._pixelrag_http(query)

        with tempfile.TemporaryDirectory(prefix="growthpulse-pixelshot-") as tmp:
            output_dir = Path(tmp) / "tiles"
            try:
                completed = subprocess.run(
                    shlex.split(self.pixelshot) + [url, "-o", str(output_dir)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False,
                )
                return {
                    "status": "rendered" if completed.returncode == 0 else "error",
                    "returncode": completed.returncode,
                    "tiles": sorted(str(p) for p in output_dir.glob("**/*") if p.is_file()),
                    "output": completed.stdout[-10000:],
                    "error": completed.stderr[-5000:],
                    "query": query,
                }
            except FileNotFoundError:
                return {"status": "unavailable", "reason": f"Command not found: {self.pixelshot}"}
            except subprocess.TimeoutExpired:
                return {"status": "timeout"}

    def _pixelrag_http(self, query: str) -> dict:
        payload = {"queries": [{"text": query}], "n_docs": 5}
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(f"{self.pixelrag_url}/search", json=payload)
            response.raise_for_status()
            return {"status": "ok", "results": response.json()}
