# ADR-002: Estrategia multi-tenant con Row-Level Security

**Status:** Accepted
**Date:** 2026-05-09
**Tags:** security, data, foundational

## Contexto

Plataforma multi-tenant con dos casos de uso simultáneos:
1. **B2B:** cada gimnasio es un tenant aislado, sus atletas y datos no deben ser visibles por otros gimnasios
2. **B2C standalone:** atletas sin gimnasio afiliado conviven en la misma plataforma con tenant especial "self"

Requisito crítico: aislamiento estricto de datos entre tenants, incluso ante bugs en código de aplicación.

## Decisión

**PostgreSQL con Row-Level Security (RLS) habilitado en todas las tablas con datos de tenant.**

Cada tabla incluye columna `tenant_id` (UUID) y política RLS que filtra por el `tenant_id` del JWT del usuario autenticado.

### Implementación

```sql
-- Habilitar RLS en cada tabla
ALTER TABLE athletes ENABLE ROW LEVEL SECURITY;

-- Política que filtra por tenant_id del contexto de sesión
CREATE POLICY tenant_isolation ON athletes
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Forzar RLS incluso para owners de tabla
ALTER TABLE athletes FORCE ROW LEVEL SECURITY;
```

En FastAPI middleware:

```python
@app.middleware("http")
async def set_tenant_context(request: Request, call_next):
    tenant_id = extract_tenant_from_jwt(request)
    async with get_db() as db:
        await db.execute(f"SET app.current_tenant = '{tenant_id}'")
    return await call_next(request)
```

### Tenant especial "self"

Atletas standalone pertenecen a un tenant técnico llamado `self`. Cuando se afilian a un gimnasio B2B, sus datos se migran (con consentimiento explícito) al tenant del gimnasio. Esto preserva su historial y habilita la conversión.

### Tabla `tenants`

```sql
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type VARCHAR(20) NOT NULL CHECK (type IN ('gym', 'self')),
  name VARCHAR(255),
  geofence GEOMETRY(POLYGON, 4326),
  branding JSONB,
  plan VARCHAR(50),
  status VARCHAR(20) DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Alternativas evaluadas

| Estrategia | Pros | Contras | Veredicto |
|---|---|---|---|
| Database per tenant | Aislamiento total físico | Costo, complejidad ops, limita features cross-tenant | Solo enterprise tier futuro |
| Schema per tenant | Aislamiento alto | Migrations complejas, scaling limitado | Descartado |
| Application-level filtering (sin RLS) | Simple | Bugs catastróficos posibles | Descartado |
| **RLS + tenant_id en cada tabla** | Aislamiento robusto, una sola DB, performant | Disciplina de schema | **Elegida** |

## Consecuencias

**Positivas:**
- Defensa en profundidad: incluso si código de aplicación tiene bug, DB rechaza la query cross-tenant
- Una sola DB simplifica ops, backups, migrations
- Rankings cross-tenant (rankings globales) son posibles con queries especiales que setean tenant=NULL como super-usuario

**Negativas:**
- Cada query DEBE setear `app.current_tenant` antes (middleware obligatorio)
- Rankings globales requieren bypass deliberado vía rol `ranking_aggregator`
- Performance: índices deben incluir `tenant_id` como primera columna en composites

**Implementación obligatoria:**
- Middleware en FastAPI que extrae tenant_id del JWT y lo setea
- Tests automatizados que verifican aislamiento (test "user de tenant A no puede leer datos de tenant B")
- Linter custom que rechaza migrations sin RLS habilitado
- Auditoría: todo bypass de RLS queda en log de seguridad

## Reglas no negociables

1. Toda tabla con datos de usuario lleva `tenant_id` y RLS habilitado
2. Migrations sin política RLS no pasan CI
3. Tests de aislamiento se ejecutan en cada PR
4. Solo el rol `platform_admin` puede bypassear RLS, y queda registrado
5. Rankings globales y agregaciones cross-tenant usan vistas materializadas con datos anonimizados
