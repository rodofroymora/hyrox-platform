# Spec: Identity Service

**Versión:** 0.2.0
**Status:** Approved
**Autor:** Backend Builder Agent
**Fecha:** 2026-05-09
**Reemplaza:** v0.1.0 (health check only)

---

## Responsabilidad

Autenticación y gestión de identidad para la plataforma HYROX Performance Platform.
Emite y valida JWT. Gestiona usuarios, roles, sesiones y el flujo de invitaciones de gimnasios.

---

## Scope v0.2.0

| Feature | Incluido |
|---|---|
| Registro email + password (tenant `self`) | ✅ |
| Registro por invite de gimnasio | ✅ |
| Verificación de email | ✅ |
| Login email + password | ✅ |
| Login Google OAuth (token nativo móvil) | ✅ |
| Login Apple OAuth (token nativo móvil) | ✅ |
| Access token (JWT, 15 min) + Refresh token (30 días, rotativo) | ✅ |
| Logout (revocación de refresh token) | ✅ |
| Password reset por email | ✅ |
| Roles: `athlete`, `gym_admin` | ✅ |
| MFA | ❌ v0.x futuro |
| Borrado de cuenta (Right to be forgotten) | ❌ v0.4.0 |
| Exportación de datos (Art. 15 GDPR) | ❌ v0.4.0 |

---

## Decisiones técnicas

### Tokens
- **Access token:** JWT firmado con RS256, TTL 15 minutos. Stateless — otros servicios validan con clave pública sin llamar al identity service.
- **Refresh token:** opaco (UUID v4), TTL 30 días, **rotativo** (cada uso emite uno nuevo e invalida el anterior). Almacenado como hash SHA-256 en DB.
- RS256 (asimétrico): clave privada en identity service, clave pública expuesta en `GET /.well-known/jwks.json` para consumo de otros servicios.

### OAuth móvil (Google + Apple)
El cliente móvil (iOS) completa el flujo OAuth con el SDK nativo y envía el **ID token** al backend. El backend lo verifica contra los endpoints públicos de Google/Apple y crea o recupera el usuario. No hay redirect web.

### Roles
- `athlete` — usuario final del producto
- `gym_admin` — administrador de un tenant gimnasio

La creación de tenants gimnasio y su primer `gym_admin` se realiza vía **script CLI local** (`scripts/create_gym_tenant.py`), ejecutado por el platform_admin. No hay endpoint HTTP — elimina superficie de ataque y es suficiente para la fase actual. Un admin UI se especificará cuando el volumen de onboarding lo justifique.

### Proveedor de email
**Resend** (`resend` Python SDK). Free tier 3.000 emails/mes, SDK de una línea, entregabilidad excelente. Se añade como dependencia en `pyproject.toml`. La API key se inyecta vía variable de entorno `RESEND_API_KEY`.

### OAuth en web dashboard
Diferido a v0.3.0. El web dashboard (usado por gym admins) usa email + password en v0.2.0. Los gym admins son creados por el script CLI, no se auto-registran. El flujo OAuth PKCE para web es arquitectónicamente distinto al ID token móvil y no justifica el esfuerzo en esta versión.

### Tenant assignment
- Registro libre → `tenant_id = self_tenant_id` (UUID fijo, tenant especial `self`)
- Registro con invite → `tenant_id` del gimnasio que generó la invite

---

## Modelo de datos

> Toda tabla con datos de usuario lleva `tenant_id` y RLS habilitado (ADR-002).
> Las migraciones Alembic son obligatorias y reversibles.

### `users`
```sql
CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  email           VARCHAR(255) NOT NULL UNIQUE,
  hashed_password VARCHAR(255),          -- NULL si solo usa OAuth
  role            VARCHAR(20) NOT NULL CHECK (role IN ('athlete', 'gym_admin')),
  is_verified     BOOLEAN NOT NULL DEFAULT false,
  is_active       BOOLEAN NOT NULL DEFAULT true,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON users
  USING (tenant_id = current_setting('app.current_tenant')::uuid);
ALTER TABLE users FORCE ROW LEVEL SECURITY;
CREATE INDEX idx_users_tenant_email ON users (tenant_id, email);
```

### `oauth_accounts`
```sql
CREATE TABLE oauth_accounts (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider    VARCHAR(20) NOT NULL CHECK (provider IN ('google', 'apple')),
  provider_id VARCHAR(255) NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (provider, provider_id)
);
```

### `refresh_tokens`
```sql
CREATE TABLE refresh_tokens (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash  VARCHAR(64) NOT NULL UNIQUE,  -- SHA-256 hex del token opaco
  expires_at  TIMESTAMPTZ NOT NULL,
  revoked_at  TIMESTAMPTZ,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens (user_id);
```

### `email_verification_tokens`
```sql
CREATE TABLE email_verification_tokens (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash VARCHAR(64) NOT NULL UNIQUE,
  expires_at TIMESTAMPTZ NOT NULL,  -- TTL: 24 horas
  used_at    TIMESTAMPTZ
);
```

### `password_reset_tokens`
```sql
CREATE TABLE password_reset_tokens (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash VARCHAR(64) NOT NULL UNIQUE,
  expires_at TIMESTAMPTZ NOT NULL,  -- TTL: 1 hora
  used_at    TIMESTAMPTZ
);
```

### `gym_invites`
```sql
CREATE TABLE gym_invites (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id    UUID NOT NULL REFERENCES tenants(id),
  token_hash   VARCHAR(64) NOT NULL UNIQUE,
  email        VARCHAR(255),          -- NULL = invite abierta (cualquier email)
  role         VARCHAR(20) NOT NULL DEFAULT 'athlete',
  expires_at   TIMESTAMPTZ NOT NULL,  -- TTL: 7 días
  used_at      TIMESTAMPTZ,
  created_by   UUID NOT NULL REFERENCES users(id),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## API Contract

Base URL: `/api/v1/auth`

### POST /register
Registro libre. Crea usuario con tenant `self`.

**Request:**
```json
{
  "email": "atleta@ejemplo.com",
  "password": "MinLength8!",
  "full_name": "Juan Pérez"
}
```

**Response 201:**
```json
{
  "user_id": "uuid",
  "email": "atleta@ejemplo.com",
  "message": "Verification email sent"
}
```

**Errores:**
- `409` email ya registrado
- `422` password no cumple política (min 8 chars, 1 mayúscula, 1 número)

---

### POST /register/invite
Registro por invite de gimnasio.

**Request:**
```json
{
  "invite_token": "token-opaco",
  "email": "atleta@gym.com",
  "password": "MinLength8!",
  "full_name": "Juan Pérez"
}
```

**Response 201:** igual que `/register`

**Errores:**
- `404` invite no existe
- `410` invite expirada o ya usada
- `409` email ya registrado
- `422` email no coincide con invite (si invite es nominativa)

---

### POST /verify-email
**Request:**
```json
{ "token": "token-opaco-del-email" }
```

**Response 200:**
```json
{ "message": "Email verified" }
```

**Errores:**
- `404` token no existe
- `410` token expirado o ya usado

---

### POST /login
**Request:**
```json
{
  "email": "atleta@ejemplo.com",
  "password": "MinLength8!"
}
```

**Response 200:**
```json
{
  "access_token": "jwt...",
  "refresh_token": "token-opaco",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Errores:**
- `401` credenciales inválidas (mismo mensaje para email y password — no revelar cuál falló)
- `403` cuenta no verificada
- `403` cuenta inactiva

---

### POST /login/oauth/google
**Request:**
```json
{ "id_token": "google-id-token-del-sdk-nativo" }
```

**Response 200:** igual que `/login`

**Errores:**
- `401` token de Google inválido o expirado
- `403` cuenta inactiva

---

### POST /login/oauth/apple
**Request:**
```json
{ "id_token": "apple-id-token-del-sdk-nativo" }
```

**Response 200:** igual que `/login`

**Errores:**
- `401` token de Apple inválido o expirado
- `403` cuenta inactiva

---

### POST /refresh
**Request:**
```json
{ "refresh_token": "token-opaco" }
```

**Response 200:**
```json
{
  "access_token": "jwt-nuevo...",
  "refresh_token": "token-opaco-nuevo",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Comportamiento de rotación:** el refresh token anterior queda inmediatamente revocado. Si se detecta uso de un token ya revocado → revocar toda la familia de tokens del usuario (indicador de robo).

**Errores:**
- `401` token inválido, expirado o revocado

---

### POST /logout
**Header:** `Authorization: Bearer <access_token>`

**Request:**
```json
{ "refresh_token": "token-opaco" }
```

**Response 204:** no content

---

### POST /password-reset/request
**Request:**
```json
{ "email": "atleta@ejemplo.com" }
```

**Response 200:**
```json
{ "message": "If the email exists, a reset link was sent" }
```

> Siempre responde 200 — no revelar si el email existe (ADR-004 privacy).

---

### POST /password-reset/confirm
**Request:**
```json
{
  "token": "token-opaco-del-email",
  "new_password": "NuevoPassword8!"
}
```

**Response 200:**
```json
{ "message": "Password updated" }
```

**Comportamiento adicional:** revocar todos los refresh tokens del usuario al cambiar password.

**Errores:**
- `404` token no existe
- `410` token expirado o ya usado
- `422` password no cumple política

---

### GET /.well-known/jwks.json
Clave pública RS256 para validación de JWT por otros servicios. Sin autenticación.

**Response 200:** JWKS estándar RFC 7517.

---

## Eventos producidos

> Publicados en el message bus (implementación futura — v0.3.0+).
> En v0.2.0 se loggean como eventos estructurados JSON.

| Evento | Trigger |
|---|---|
| `user.registered` | Registro exitoso |
| `user.email_verified` | Verificación de email |
| `user.logged_in` | Login exitoso |
| `user.password_reset` | Reset de password completado |
| `user.token_theft_detected` | Uso de refresh token revocado |

---

## Tests obligatorios

### Unit tests
- Generación y validación de JWT (claims correctos, expiración, RS256)
- Hash de tokens (SHA-256, no reversible)
- Validación de password policy
- Lógica de rotación de refresh tokens

### Integration tests (DB efímera)
- Registro libre → usuario creado con tenant `self`
- Registro con invite válida → usuario con tenant del gimnasio
- Registro con invite expirada → 410
- Login correcto → tokens emitidos
- Login con password incorrecto → 401 (mismo mensaje)
- Cuenta no verificada → 403
- Refresh token → nuevo par emitido, anterior revocado
- Uso de refresh token ya revocado → todos los tokens del usuario revocados
- Logout → refresh token revocado
- Password reset → todos los refresh tokens revocados

### Tests de aislamiento (ADR-002)
- Usuario de tenant `self` no puede leer datos de tenant gimnasio y viceversa

---

## Criterios Gherkin de aceptación

```gherkin
Feature: Registro de atleta libre

  Scenario: Registro exitoso con email nuevo
    Given no existe cuenta con "nuevo@email.com"
    When POST /api/v1/auth/register con email y password válidos
    Then responde 201
    And se envía email de verificación
    And usuario creado con tenant "self" y is_verified=false

  Scenario: Email duplicado
    Given existe cuenta con "existente@email.com"
    When POST /api/v1/auth/register con el mismo email
    Then responde 409

Feature: Login

  Scenario: Login correcto
    Given usuario verificado con email y password registrados
    When POST /api/v1/auth/login con credenciales correctas
    Then responde 200 con access_token y refresh_token

  Scenario: Password incorrecto
    When POST /api/v1/auth/login con password incorrecto
    Then responde 401 con mensaje genérico (no revela si es email o password)

  Scenario: Cuenta no verificada
    Given usuario registrado pero sin verificar email
    When POST /api/v1/auth/login
    Then responde 403

Feature: Rotación de refresh tokens

  Scenario: Uso de token robado detectado
    Given refresh_token RT1 fue usado y se emitió RT2
    When se intenta usar RT1 nuevamente
    Then responde 401
    And todos los refresh tokens del usuario quedan revocados

Feature: Aislamiento de tenants

  Scenario: Atleta self no accede a datos de gym
    Given atleta con tenant "self" autenticado
    When intenta leer datos de un tenant gimnasio
    Then la query RLS no retorna filas
```

---

## Métricas SRE

| Métrica | Target |
|---|---|
| Latencia P99 `/login` | < 300 ms |
| Latencia P99 `/refresh` | < 100 ms |
| Error rate 5xx | < 0.1% |
| Disponibilidad | 99.9% |

---

## Cuestiones abiertas

Ninguna — todas las decisiones bloqueantes están resueltas. Spec lista para implementación.
