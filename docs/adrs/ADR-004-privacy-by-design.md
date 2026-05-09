# ADR-004: Privacy by Design para datos biométricos

**Status:** Accepted
**Date:** 2026-05-09
**Tags:** security, compliance, foundational

## Contexto

Procesamos datos biométricos sensibles (frecuencia cardíaca, HRV, sueño, video de movimiento, ubicación GPS). Bajo GDPR (Art. 9) son "categoría especial de datos" con requisitos reforzados. En LATAM, regulaciones equivalentes (LGPD Brasil, LFPDPPP México, Ley 25.326 Argentina) tienen marcos similares.

Una brecha de seguridad o uso indebido implica:
- Multas hasta 4% revenue global o 20M EUR (GDPR)
- Pérdida de confianza irrecuperable en una comunidad pequeña como HYROX
- Posibles demandas individuales

## Decisión

**Privacy by Design** como principio rector desde día 1, no como capa añadida después.

### Principios aplicados (GDPR Art. 25)

1. **Minimización de datos:** capturar solo lo necesario para la funcionalidad declarada
2. **Limitación del propósito:** datos capturados para X no se usan para Y sin nuevo consentimiento
3. **Limitación del almacenamiento:** retención máxima definida por categoría
4. **Confidencialidad:** cifrado end-to-end donde sea posible
5. **Transparencia:** usuario ve qué datos tenemos y cómo se usan
6. **Control del usuario:** consentimiento granular, revocable, exportable, eliminable

### Clasificación de datos y políticas

| Categoría | Ejemplos | Cifrado | Retención | Consentimiento |
|---|---|---|---|---|
| Identificación | email, nombre | AES-256 reposo + TLS | Hasta borrado | Implícito (cuenta) |
| Contacto | teléfono, dirección | AES-256 + tokenización | Hasta borrado | Explícito separado |
| Biométrico crudo | HR, HRV, sueño | AES-256 + tokenización + minimización | 5 años | Explícito por categoría |
| Video biomecánico | Videos de ejercicio | AES-256 + signed URLs (TTL 1h) | 1 año por defecto | Explícito por video |
| Ubicación | GPS de entrenamientos | AES-256 + agregación | 2 años precisa, indefinida agregada | Explícito |
| Métricas computadas | HPI, splits, predicciones | Estándar | Permanente (anonimizable) | Implícito |
| Logs auditoría | Validaciones, accesos | AES-256 + WORM | 7 años (obligación legal) | No requerido (legítimo interés) |

### Consentimiento granular

Cada usuario tiene un objeto `consents` que contiene flags independientes:

```json
{
  "wearable_sync": { "granted": true, "date": "2026-05-09T10:00:00Z" },
  "biomechanics_video": { "granted": false, "date": null },
  "location_tracking": { "granted": true, "date": "2026-05-09T10:00:00Z" },
  "ai_predictions": { "granted": true, "date": "2026-05-09T10:00:00Z" },
  "ranking_visibility": { "granted": true, "scope": "anonymous", "date": "..." },
  "social_feed_publish": { "granted": false, "date": null },
  "marketing_emails": { "granted": false, "date": null },
  "data_for_model_training": { "granted": false, "date": null },
  "share_with_coach": { "granted": true, "coach_id": "...", "date": "..." }
}
```

### Right to be forgotten (Art. 17 GDPR)

Workflow obligatorio:
1. Usuario solicita borrado vía app, con MFA
2. Sistema marca cuenta como `pending_deletion` (soft delete, datos siguen visibles solo para procesos legales si aplica)
3. Periodo de gracia 30 días (mitigar borrados accidentales)
4. Job batch ejecuta:
   - PII anonimizada (hash irreversible)
   - Métricas agregadas se mantienen sin atribución
   - Videos eliminados de S3 (incluyendo backups)
   - Logs auditoría se anonimizan pero conservan 7 años (obligación legal)
5. Usuario recibe certificado de borrado firmado digitalmente
6. Coaches afectados son notificados
7. Rankings se recalculan eliminando contribuciones del usuario

### Right to access (Art. 15)

Endpoint `/api/v1/me/data-export` que genera ZIP con:
- Todos los datos personales en JSON
- Videos en su formato original
- Métricas históricas en CSV
- Log de consentimientos otorgados/revocados

SLA: <72h.

### Data Protection Impact Assessment (DPIA)

Toda feature nueva que toque datos sensibles requiere DPIA antes de implementar. Template estándar en `/docs/dpia/template.md`. DPO designado (interno o externo según fase).

### Cifrado end-to-end (futuro)

Roadmap: implementar E2EE para videos biomecánicos en fase 2. Atleta y coach asignado tienen las claves; ni siquiera la plataforma puede ver el contenido sin colaboración del usuario. Esto es diferenciador competitivo y reduce superficie de riesgo.

## Consecuencias

**Positivas:**
- Compliance robusto por diseño, no remediación
- Confianza del usuario como diferenciador comercial (especialmente en EU/LATAM)
- Reduce superficie legal y técnica
- Facilita certificaciones futuras (SOC 2, ISO 27001)

**Negativas:**
- Velocidad de desarrollo inicial menor (DPIAs, consentimientos granulares)
- Algunos features de IA limitados sin consent específico
- Costo de infraestructura mayor (cifrado, KMS, auditoría)

**Reglas no negociables:**
1. Toda categoría de datos sensibles tiene flag de consentimiento explícito
2. Sin consent, el dato no se procesa (incluso si está capturado)
3. Auditoría ejecutada anualmente por tercero
4. DPO designado antes de tener 1000 usuarios activos
5. Notificación de brechas en <72h (obligación GDPR)
6. Programa de bug bounty operativo en fase 2
