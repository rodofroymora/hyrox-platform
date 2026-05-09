# ADR-005: Estrategia mobile (iOS first + bridge web)

**Status:** Accepted
**Date:** 2026-05-09
**Tags:** mobile, mvp, foundational

## Contexto

App del atleta es el touchpoint principal del producto. Necesitamos:
- Acceso óptimo a HealthKit (iOS) y HealthConnect (Android)
- Conexión con Garmin Connect IQ, Polar SDK, Whoop API
- Captura y subida de video con buena UX
- Buena performance, push notifications fiables, modo offline

Limitación actual: founder no es mobile dev, búsqueda activa de cofounder con ese perfil. No queremos bloquear el desarrollo del producto esperando ese hire.

## Decisión

**Estrategia escalonada:**

### Fase 0-1 (MVP, mes 1-4)

**1. App iOS nativa (Swift) — primer release**
- iOS captura ~60% del mercado HYROX (atletas tienden a tener iPhone + Apple Watch)
- HealthKit nativo es muchísimo mejor que cualquier wrapper
- Mejor calidad para Apple Watch sync

**2. Web App Progresiva (PWA) responsive — bridge para Android**
- React + Tailwind, mismo codebase que el dashboard del coach
- Funcionalidad reducida vs iOS nativa (no Apple Watch obviamente)
- Permite a usuarios Android usar la plataforma con limitaciones explícitas
- Conexión Garmin via Garmin Connect Web API (no SDK móvil)
- Indicación clara: "App Android nativa próximamente"

**3. NO iniciar Android nativa hasta tener cofounder mobile**
- Entrar a Android sin expertise = bugs en producción + reviews 2 estrellas + reputación dañada
- Mejor PWA decente que app Android mediocre

### Fase 2 (mes 5-9, idealmente con cofounder ya)

**4. App Android nativa (Kotlin)**
- Liderada por cofounder mobile
- HealthConnect + Garmin SDK + Samsung Health
- Paridad de features con iOS

### Fase 2-3 (mes 9+)

**5. App tablet del coach (React Native)**
- Cross-platform iPad/Android tablet
- No requiere capacidades nativas críticas
- Acelera desarrollo

## Alternativas evaluadas y rechazadas

| Opción | Pros | Contras | Veredicto |
|---|---|---|---|
| React Native cross-platform desde día 1 | Un solo codebase | Calidad de integración wearables inferior, performance subóptima | Rechazado |
| Flutter | Performance buena | HealthKit bindings inmaduros, menos ecosistema | Rechazado |
| Solo PWA en MVP | Velocidad máxima | Sin acceso a HealthKit ni Apple Watch sync nativo | Rechazado |
| iOS + Android nativos en paralelo | Ideal | Imposible sin equipo mobile completo | Rechazado |
| **iOS nativa + PWA bridge** | Foco MVP, buen UX iOS, no bloquea Android | Android sufre features limitadas temporalmente | **Elegido** |

## Cómo arrancar iOS sin cofounder mobile

Estrategia para no bloquear:

1. **Contratar iOS dev contract por proyecto** (3-4 meses MVP, 8-15k USD/mes según geografía)
2. **Usar agente especializado en Swift** supervisado por contract dev
3. **Founder define producto y revisa UX**, no escribe Swift
4. **Open source SDK de wearables**: aprovechar bibliotecas existentes (e.g., `HealthKitReporter`)
5. **MVP con features core de iOS**, no todas las del spec; iterar

Cuando llegue cofounder, recibe codebase iOS funcional para evolucionar, no tabula rasa.

## Consecuencias

**Positivas:**
- Calidad iOS desde día 1 en plataforma dominante en target
- Andoid no queda totalmente fuera (PWA)
- No bloquea por falta de cofounder
- Estrategia honesta y comunicable a inversores

**Negativas:**
- Usuarios Android tienen experiencia inferior temporalmente (mitigado con comunicación clara)
- Mantenimiento de PWA + iOS + futuro Android nativo = 3 stacks
- Costo contractor iOS si no llega cofounder pronto

**Riesgos a vigilar:**
- Si cofounder mobile no llega en 6 meses, plan B: contratar Android dev como empleado
- Reviews negativas Android en stores (mitigar con landing claro: "Android coming Q4")
- Performance PWA en Android viejos (testear desde día 1)
