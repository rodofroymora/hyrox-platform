# ADR-003: Spec-Driven Development con agentes IA

**Status:** Accepted
**Date:** 2026-05-09
**Tags:** process, ai-agents, foundational

## Contexto

Equipo arranque ultra-lean (1 founder part-time, búsqueda de cofounder). El multiplicador clave es el uso disciplinado de agentes IA especializados. Sin metodología, los agentes generan código rápido pero frágil. Con metodología, multiplican capacidad por 5-10x.

## Decisión

Adoptar **Spec-Driven Development (SDD)** como metodología principal, con agentes IA generando código a partir de especificaciones formales.

### Flujo SDD

```
1. Escribir SPEC funcional (user story + criterios Gherkin)
2. Escribir SPEC técnica (API contract, modelo de datos, tests esperados)
3. Agente genera código + tests
4. Humano revisa PR según matriz de revisión
5. Merge y deploy
6. Monitoreo en producción
```

### Matriz de revisión humana

| Tipo de cambio | Revisión humana |
|---|---|
| CRUD básico, endpoints estándar | Skim review (escaneo rápido) |
| Lógica de negocio compleja | Review completo |
| Cualquier código de auth/authz | **Obligatorio sí o sí** |
| Cualquier código de billing/pagos | **Obligatorio sí o sí** |
| Cualquier código que toque datos biométricos | **Obligatorio sí o sí** |
| Cualquier migración de DB | **Obligatorio sí o sí** |
| Cambios en políticas RLS | **Obligatorio sí o sí + tests aislamiento** |
| Tests | Skim review |
| Docs | Skim review |
| UI no crítica | Skim review |

### Estructura de specs

```
/docs/specs/
  ├── modules/
  │   ├── M01-wearable-integration.md
  │   ├── M02-biomechanics.md
  │   └── ...
  ├── services/
  │   ├── identity-service.md
  │   ├── tenant-service.md
  │   └── ...
  └── adrs/
      ├── ADR-001-stack.md
      └── ...
```

Cada spec de servicio incluye:
- Responsabilidad del servicio
- API contract (OpenAPI o equivalente)
- Modelo de datos
- Eventos producidos/consumidos
- Tests obligatorios (unit, integration, e2e)
- Criterios Gherkin de aceptación
- Métricas SRE (latencia, error rate, saturation)

### Agentes operativos (8)

1. **Backend Builder** — genera servicios FastAPI desde specs
2. **Data Pipeline** — pipelines de wearables y time-series
3. **ML Ops** — entrenamiento, versionado, deploy de modelos
4. **Security & Compliance** — auditoría, GDPR, scanning
5. **Coach Virtual** — chatbot del producto (es feature del SaaS)
6. **Content Generator** — microlecciones, traducciones
7. **Customer Success** — soporte L1
8. **Analytics & Insights** — reportes B2B mensuales

Cada agente tiene:
- Spec propia en `/agents/{agent-name}/SPEC.md`
- Prompt maestro en `/agents/{agent-name}/PROMPT.md`
- Set de evaluaciones en `/agents/{agent-name}/evals/`
- Lista de herramientas que puede usar
- Guardrails explícitos

## Consecuencias

**Positivas:**
- Velocidad de desarrollo 5-10x vs equipo tradicional sin agentes
- Specs son artefacto durable: si agente cambia, spec persiste
- Onboarding de futuros contratados acelerado (lee specs)
- Trazabilidad: cada línea de código apunta a una spec
- Inversores ven proceso maduro pese a equipo pequeño

**Negativas:**
- Disciplina inicial es alta: si no hay spec, no hay código
- Tiempo de escritura de specs no es trivial
- Riesgo: agente alucinando código que pasa tests pero falla en edge cases (mitigado con eval suite robusta)

**Reglas no negociables:**
1. No se merge código sin spec asociada
2. Tests obligatorios por agente, ejecutados en CI
3. Code review humano según matriz de arriba
4. Toda decisión arquitectónica → ADR antes de codear
5. Specs viven en Git, versionadas, con changelog

## Métricas de éxito del proceso

- % de PRs que pasan CI a la primera (target: >85%)
- Tiempo medio de spec → producción (target: <3 días por feature)
- Bugs en producción atribuibles a código de agente (target: <1 por mes en MVP)
- Coverage de tests automatizados (target: >80%)
