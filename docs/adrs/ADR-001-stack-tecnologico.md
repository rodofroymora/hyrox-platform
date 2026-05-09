# ADR-001: Stack tecnológico inicial

**Status:** Accepted
**Date:** 2026-05-09
**Deciders:** Founder
**Tags:** stack, infrastructure, foundational

## Contexto

Necesitamos definir el stack tecnológico inicial del MVP de la plataforma HYROX. Las decisiones aquí son foundational: cambiarlas más adelante tiene costo alto. Debe alinear con el perfil del equipo (founder con expertise en data, IA, security, governance, agentes), permitir velocidad con agentes, y soportar la escalabilidad futura sin rework total.

## Decisión

| Capa | Tecnología elegida | Alternativas evaluadas |
|---|---|---|
| Backend | Python 3.12 + FastAPI | Go, Node.js (NestJS) |
| Mobile atleta | Swift (iOS nativo) | React Native, Flutter |
| Mobile coach | React Native | Nativo, web responsive |
| Web dashboard | Next.js 14 + TypeScript | Remix, plain React |
| Cloud | AWS | GCP, Azure |
| Orquestación | Kubernetes (EKS) post-MVP, ECS Fargate en MVP | Vanilla EC2, Lambda |
| DB transaccional | PostgreSQL 15 con RLS (RDS) | MySQL, MongoDB |
| DB time-series | TimescaleDB (extensión PG) | InfluxDB, ClickHouse |
| Object storage | S3 con Object Lock | GCS, R2 |
| Cache + leaderboards | Redis (ElastiCache) | Memcached, KeyDB |
| Event bus (post-MVP) | MSK (Kafka) o EventBridge | RabbitMQ, NATS |
| ML/IA | Claude API + scikit-learn + XGBoost | OpenAI, modelos propios desde día 1 |
| Auth | AWS Cognito (MVP) → Auth0/Keycloak | Clerk, custom |
| Pagos | Stripe + Stripe Connect | MercadoPago, Adyen |
| IaC | Terraform + Terragrunt | CDK, Pulumi |
| CI/CD | GitHub Actions | GitLab CI, CircleCI |
| Observability | Datadog (con créditos startup) | Grafana stack, NewRelic |

## Justificación

**Backend Python+FastAPI:** el founder tiene expertise en data e IA donde Python es el estándar. FastAPI es moderno, async, con tipado fuerte (Pydantic) que reduce bugs. Los agentes generan FastAPI con alta calidad. La velocidad de iteración importa más que micro-optimizaciones de performance en MVP.

**iOS nativo en Swift para app del atleta:** HealthKit y la integración con Apple Watch tienen mejor calidad nativa. La app del atleta es el touchpoint emocional principal del producto, no se puede comprometer. Cuando llegue cofounder mobile, este es su territorio.

**React Native para app del coach:** menos crítico nativamente, prioriza velocidad cross-platform. Coach usa la app principalmente para revisar y validar, no entrenar.

**AWS:** ecosistema más maduro para data, ML, seguridad. AWS Activate ofrece hasta 100k USD en créditos startup (aplicar via aceleradora o Founders.aws). Cognito acelera MVP, migrable a Auth0 si se necesita SSO empresarial. S3 con Object Lock es esencial para auditoría inmutable WORM.

**ECS Fargate en MVP, Kubernetes post-MVP:** Kubernetes es overkill al inicio. Fargate da serverless containers sin gestionar nodos. Migración a EKS cuando haya >5 servicios y haga falta service mesh.

**TimescaleDB sobre InfluxDB:** menos un sistema que mantener. PostgreSQL con extensión, queries SQL familiares, multi-tenant con misma RLS.

**Claude API en MVP:** calidad de razonamiento alta, alineamiento de seguridad, evita complejidad de hosting modelos propios. Evaluar fine-tuning post-PMF.

## Consecuencias

**Positivas:**
- Velocidad de desarrollo máxima con agentes (ecosistema Python rico)
- Stack estándar industria, fácil contratar más adelante
- Créditos AWS aceleran runway 6-12 meses
- Aislamiento multi-tenant con RLS robusto desde día 1

**Negativas:**
- Python no es óptimo para servicios ultra-low-latency (mitigable con caching y async)
- iOS nativo + RN coach requiere mantener dos stacks mobile (asumido conscientemente)
- Lock-in moderado AWS (mitigado con abstracciones en código de aplicación)

**Riesgos a vigilar:**
- Crecimiento de costos AWS post-créditos: instrumentar FinOps desde día 1
- Dependencia de Claude API: diseñar abstracciones para poder cambiar provider
- Performance de TimescaleDB en alto volumen (>1M sesiones/día): plan de migración a ClickHouse si llega
