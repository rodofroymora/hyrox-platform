# HYROX Performance Platform

> Plataforma SaaS para transformar gimnasios HYROX en centros de alto rendimiento mediante datos, IA y experiencia gamificada.

## Estado del proyecto

🚧 **Fase 0 — Foundations & Validation** (mes 1-2)

## Estructura del monorepo

```
hyrox-platform/
├── README.md                          # Este archivo
├── docs/                              # Documentación maestra
│   ├── PRD.md                         # Product Requirements Document
│   ├── adrs/                          # Architecture Decision Records
│   ├── specs/                         # Specs funcionales y técnicas
│   │   ├── modules/                   # Specs por módulo de producto (M1-M9)
│   │   └── services/                  # Specs por microservicio
│   ├── dpia/                          # Data Protection Impact Assessments
│   └── runbooks/                      # Operational runbooks
│
├── agents/                            # Agentes IA operativos
│   ├── backend-builder/
│   │   ├── SPEC.md
│   │   ├── PROMPT.md
│   │   └── evals/
│   ├── data-pipeline/
│   ├── ml-ops/
│   ├── security-compliance/
│   ├── coach-virtual/                 # Es feature del producto
│   ├── content-generator/
│   ├── customer-success/
│   └── analytics-insights/
│
├── services/                          # Microservicios backend (Python/FastAPI)
│   ├── identity/                      # Auth, sessions, MFA
│   ├── tenant/                        # Multi-tenancy management
│   ├── athlete/                       # Athlete profiles
│   ├── wearable/                      # Wearable integrations
│   ├── workout/                       # Workouts and plans
│   ├── metrics/                       # Performance metrics
│   ├── biomechanics/                  # Video analysis
│   ├── ai-engine/                     # ML predictions, recommendations
│   ├── validation/                    # Tier validation, anti-fraud
│   ├── ranking/                       # Leaderboards, leagues
│   ├── coaching/                      # Coach assignment, marketplace
│   ├── education/                     # Content, lessons
│   ├── billing/                       # Stripe integration
│   ├── notification/                  # Push, email, SMS
│   ├── social/                        # Feed, social features
│   └── audit/                         # Audit logs, compliance
│
├── apps/                              # Apps cliente
│   ├── ios-athlete/                   # iOS nativo Swift
│   ├── coach-tablet/                  # React Native (post-MVP)
│   └── web-dashboard/                 # Next.js (gimnasios + atletas web)
│
├── shared/                            # Código compartido
│   ├── proto/                         # Definiciones Protobuf (eventos)
│   ├── openapi/                       # Especificaciones OpenAPI consolidadas
│   └── design-system/                 # Tokens y componentes UI
│
├── infra/                             # Infraestructura como código
│   ├── terraform/                     # AWS resources
│   ├── helm/                          # K8s charts (post-MVP)
│   └── github-actions/                # Workflows CI/CD
│
├── ml/                                # Modelos ML y data science
│   ├── notebooks/                     # Exploración
│   ├── models/                        # Modelos entrenados
│   ├── pipelines/                     # Training y serving pipelines
│   └── evals/                         # Evals de modelos
│
├── tests/                             # Tests cross-service
│   ├── e2e/                           # End-to-end
│   ├── load/                          # Performance testing
│   └── security/                      # Security testing
│
├── scripts/                           # Tooling
└── .github/                           # GitHub configs (CODEOWNERS, etc.)
```

## Quick start

### Pre-requisitos

- Python 3.12+
- Docker + Docker Compose
- Node.js 20+ (para web dashboard)
- AWS CLI configurado
- Terraform 1.6+

### Setup local

```bash
# Clonar repo
git clone https://github.com/[org]/hyrox-platform.git
cd hyrox-platform

# Setup backend services
cd services/identity
poetry install
docker-compose -f docker-compose.dev.yml up -d  # PostgreSQL, Redis local
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload

# Tests
poetry run pytest
```

## Documentos clave

| Documento | Path | Descripción |
|---|---|---|
| PRD | `/docs/PRD.md` | Product Requirements Document |
| ADR-001 | `/docs/adrs/ADR-001-stack-tecnologico.md` | Stack tecnológico inicial |
| ADR-002 | `/docs/adrs/ADR-002-multi-tenant-rls.md` | Estrategia multi-tenant |
| ADR-003 | `/docs/adrs/ADR-003-spec-driven-development.md` | Spec-Driven Development |
| ADR-004 | `/docs/adrs/ADR-004-privacy-by-design.md` | Privacy by design |
| ADR-005 | `/docs/adrs/ADR-005-mobile-strategy.md` | Estrategia mobile |

## Workflow de desarrollo

1. **Issue creado** con referencia a spec
2. **Spec revisada** o creada en `/docs/specs/`
3. **Backend Builder Agent** implementa
4. **Founder revisa** PR según matriz ADR-003
5. **CI verde** + revisión humana → merge
6. **Deploy** a dev automático, staging manual, prod con aprobación

## Roadmap

- [ ] **Fase 0 (mes 1-2):** Foundations + validación con atletas y gimnasios
- [ ] **Fase 1 (mes 3-4):** MVP standalone (iOS + 4 servicios core)
- [ ] **Fase 2 (mes 5-9):** Diferenciación (IA, biomecánica, gamificación, primer B2B)
- [ ] **Fase 3 (mes 10-18):** Escala, certificaciones, Series A

## Reglas de oro

1. Sin spec, no hay código
2. Tenant isolation es sagrado
3. Privacidad sobre velocidad
4. Tests obligatorios
5. Code review humano en código crítico (auth, billing, datos sensibles)
6. ADRs versionados cuando hay decisiones arquitectónicas

## Contacto

- Founder técnico: [tu nombre]
- Co-founder mobile: [buscando 🔍]
