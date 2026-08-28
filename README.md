# GrowthPulse

Growth intelligence platform scaffold integrating **Agent Reach** for web/source access and **PixelRAG** for visual retrieval.

## Architecture

```text
source URL / document
        |
        v
  Agent Reach  -----> source metadata / extracted content
        |
        v
   PixelRAG adapter -----> screenshots / visual retrieval
        |
        v
 GrowthPulse API -----> normalized research result
        |
        v
     dashboard
```

The integrations are intentionally adapter-based. GrowthPulse does not vendor either upstream project; it calls their installed/runtime interfaces so they can be upgraded independently.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

API health: `GET http://localhost:8000/health`

Research endpoint:

```bash
curl -X POST http://localhost:8000/v1/research \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com","query":"What are the main growth opportunities?"}'
```

## Integration configuration

- `AGENT_REACH_COMMAND`: command used to invoke Agent Reach. Keep this configurable because upstream installation/CLI interfaces may change.
- `PIXELRAG_URL`: optional PixelRAG serve API URL. When present, GrowthPulse uses the HTTP retrieval adapter.
- `PIXELSHOT_COMMAND`: optional local `pixelshot` command for rendering when a PixelRAG server is not configured.

This first commit is an integration foundation, not a claim that either upstream dependency is already installed in the deployment environment.
