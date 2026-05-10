# Identity Service

Servicio de identidad de la HYROX Performance Platform.

**Spec:** [`/docs/specs/services/identity-service.md`](../../docs/specs/services/identity-service.md)
**Versión actual:** 0.1.0 — esqueleto + health check

## Stack

- Python 3.12
- FastAPI 0.115+
- Poetry (gestión de dependencias)

## Setup

```bash
poetry install
```

## Correr el servicio

```bash
poetry run uvicorn identity.main:app --reload --port 8001
```

## Tests

```bash
poetry run pytest -v
```

## Endpoints

| Método | Path | Descripción |
|---|---|---|
| GET | /health | Health check del servicio |
| GET | /docs | OpenAPI UI (solo dev) |

## Roadmap

- v0.2.0: registro y login con JWT
- v0.3.0: multi-tenant + RLS
- v0.4.0: consentimientos granulares (ADR-004)
