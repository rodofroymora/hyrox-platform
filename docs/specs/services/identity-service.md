# Spec: Identity Service

**Versión:** 0.1.0
**Status:** Draft
**Autor:** Backend Builder Agent (onboarding task)
**Fecha:** 2026-05-09

## Responsabilidad

Servicio de identidad para la plataforma HYROX Performance Platform.
En esta versión inicial (v0.1.0) expone únicamente el health check del servicio.
Auth, gestión de usuarios y JWT se especifican en versiones futuras.

## Scope v0.1.0 (este ticket)

- Esqueleto del servicio con Poetry
- Endpoint `GET /health`

## Fuera de scope v0.1.0

- Autenticación / autorización
- Base de datos
- Gestión de usuarios

---

## API Contract v0.1.0

### GET /health

**Descripción:** Verifica que el servicio está operativo.

**Request:** ningún parámetro.

**Response 200:**
```json
{ "status": "ok" }
```

**Criterios Gherkin:**

```gherkin
Feature: Health check del identity service

  Scenario: Servicio operativo
    Given el identity service está corriendo
    When hago GET /health
    Then recibo HTTP 200
    And el body es {"status": "ok"}
```

---

## Notas

- Spec mínima creada como artefacto de la tarea de onboarding del Backend Builder Agent.
- Expandir con API contract completo antes de implementar auth.
