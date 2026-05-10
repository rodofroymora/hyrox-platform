# ADR-006: Landing page Sled Pull con waitlist

**Status:** Accepted
**Date:** 2026-05-09 (revisado v1.2)
**Deciders:** Founder
**Tags:** marketing, validation, scope-change, naming

## Resumen de la decisión

Lanzar una landing page de waitlist para el producto bajo el nombre **Sled Pull**, dominio principal **sledpull.app**, ejecutado en paralelo con las entrevistas de validación de la semana actual.

## Decisión sobre el nombre

Tras evaluación de múltiples opciones (HyroxOS, AthleteLab, PaceLab, Sled, Sled Pull, Sled Push) con verificación de disponibilidad de dominio, conflictos de marca registrada, productos competidores existentes, y alineación con el nicho HYROX:

Se elige **Sled Pull** por las siguientes razones:

1. **Cero conflictos de software:** no existe app, SaaS o plataforma de fitness/coaching con este nombre
2. **Conexión emocional fuerte:** Sled Pull es el ejercicio más temido de HYROX, el storytelling es natural
3. **SEO defendible:** término muy nicho, baja competencia vs. nombres genéricos
4. **Disponibilidad de dominio:** sledpull.app disponible y registrado
5. **Sin riesgo de marca HYROX:** "sled pull" es nombre descriptivo del ejercicio, no infringe marca registrada de HYROX

### Nombres descartados y razón

| Nombre | Razón de descarte |
|---|---|
| HyroxOS | HYROX es marca registrada de Upsolut Sports & Entertainment GmbH; uso no autorizado |
| AthleteLab | Conflicto con "Generator Athlete Lab" (TM registrada), "Athlete Lab Detroit" (gym), "Athletic Lab" (TM apps) |
| PaceLab | getpacelab.com es competidor directo (blood-based performance for endurance athletes) |
| Sled (solo) | sled.com es dominio premium ($$$ inviable en MVP); muchos significados compiten en SEO |
| Sled Push | Equivalente válido, founder mantuvo decisión previa por Sled Pull |

## Decisiones técnicas

### Dominio principal
- **sledpull.app** — registrado el 2026-05-09
- TLD .app: forced HTTPS (Google requirement), comunica claramente "producto digital"

### Dominios pendientes de evaluar
- **sledpull.com** — recomendado adquirir defensivamente cuando haya tracción (~$10/año)
- Decisión: NO comprar en MVP, evaluar en 30-60 días según métricas

### Handles sociales reservados
- Instagram: @sledpull (o @sledpullapp si tomado)
- Twitter/X: @sledpull
- LinkedIn: página empresa Sled Pull
- TikTok: @sledpull
- YouTube: canal Sled Pull

### Stack técnico landing
- **Frontend:** Next.js 14 + TypeScript + Tailwind + App Router
- **Hosting:** Vercel (free tier inicial)
- **Email:** Loops (free tier hasta 1000 contacts)
- **Analytics:** Vercel Analytics (privacy-first, alineado con ADR-004)
- **Repositorio:** subdirectorio apps/landing/ en monorepo existente
- **i18n:** ES/EN con toggle de idioma

### Audiencia
Landing dual con segmentación visible:
- Sección principal para atletas (B2C)
- Sección secundaria /gyms para dueños de gimnasios (B2B)
- CTA principal: captura email para waitlist

## Plan de ejecución

### Esta semana (paralelo a entrevistas)

**Día 1 (hoy):** dominio + setup técnico
- ✅ Comprar sledpull.app en registrar
- Reservar handles sociales (pendiente)
- Setup de Next.js en apps/landing/ con Claude Code
- Configurar Vercel deployment
- Crear cuenta Loops + API key

**Día 2:** copy V1 + componentes
- Copy V1 basado en PRD v1.0 + insights de primeras entrevistas
- Maquetación de Hero + Problem + Solution + Waitlist Form + FAQ + Footer
- Integración con Loops API
- Toggle ES/EN funcional

**Día 3:** testing + lanzamiento soft
- Testing en mobile y desktop
- Lanzamiento soft a círculo cercano (10-20 personas) para feedback
- Iteración rápida según feedback

**Día 4-7:** lanzamiento amplio + entrevistas en paralelo
- Lanzamiento en redes (Instagram HYROX, comunidades WhatsApp, LinkedIn)
- Las 5 entrevistas reales se ejecutan
- Captura de leads continúa

### Próxima semana

- Síntesis de entrevistas con agentes
- Pitch Generator Agent genera copy V2 basado en lenguaje real de usuarios
- Update de landing a V2 (copy validado)
- Evaluar compra defensiva de sledpull.com si hay tracción

## Métricas de éxito

**Día 7 (lanzamiento amplio):**
- Landing live y accesible en sledpull.app
- 50+ visitas únicas
- 10+ emails capturados (conversion rate >20%)

**Día 14 (post-síntesis):**
- Copy V2 desplegado
- 100+ visitas acumuladas
- 25+ emails capturados
- Insight cuantitativo: ¿qué mensaje convierte mejor?

**Día 30:**
- 200+ emails en waitlist
- Segmentación de leads (atletas vs dueños vs coaches)
- Primer email comunicando avance del producto
- Decisión sobre compra de sledpull.com defensivo

## Reglas no negociables

1. **Las 5 entrevistas reales NO se posponen.** La landing no es excusa para evitar conversación humana
2. **El copy se actualiza obligatoriamente** tras la síntesis de entrevistas
3. **Email de bienvenida con expectativas claras:** los inscritos saben que es "early waitlist", no "producto inminente"
4. **Privacy by design (ADR-004):** captura mínima de datos, consent explícito, opt-out fácil, GDPR/LGPD compliance desde día 1
5. **No mockups falsos:** la landing comunica concepto, NO simula un producto que no existe
6. **No usar "HYROX" en el nombre, slogan o branding** del producto. Usar "para atletas HYROX" en copy descriptivo es OK

## Riesgo de marca y mitigación

**Riesgo:** que HYROX (Upsolut Sports & Entertainment GmbH) considere que "Sled Pull" como producto orientado al mercado HYROX infringe su marca o crea confusión.

**Mitigación:**
- "Sled Pull" es término descriptivo de un ejercicio, no de HYROX como marca
- Comunicación en landing: "Para atletas HYROX y gimnasios HYROX afiliados" (uso descriptivo, no de marca)
- NO usar logo, colores oficiales o tipografía de HYROX
- NO claim de partnership, endorsement o afiliación oficial con HYROX
- Considerar contacto futuro con HYROX para licencia/partnership cuando haya tracción
- Disclaimer en footer: "Sled Pull is not affiliated with or endorsed by HYROX. HYROX is a registered trademark of Upsolut Sports & Entertainment GmbH."

## Consecuencias

**Positivas:**
- Marca propia defendible
- Sin riesgo legal con HYROX
- Storytelling natural ("Domina el sled pull, domina HYROX")
- SEO defendible en categoría nicho
- Dominio económico, ahorro de capital
- TLD .app comunica directamente "producto digital"

**Negativas:**
- Algunos usuarios pueden escribir .com por defecto y no llegar al sitio
- Sin .com defensivo, riesgo bajo pero existente de squatter
- Nombre menos universal que un nombre abstracto (Apex, Forge, etc.)
- Menos escalable fuera de HYROX/funcional (CrossFit, running puro)

**Trade-off aceptado:**
TLD .app y nombre específico del nicho HYROX a cambio de velocidad de ejecución y menor inversión inicial. Si la empresa crece, se evaluará compra de .com y rebrand basado en data.

## Próximas decisiones derivadas

- Diseño visual y logo: a definir en la fase de copy
- Política de privacidad: requiere DPIA simplificada antes del lanzamiento (ADR-004)
- Email de bienvenida: redactar antes del lanzamiento
- Tono de voz y guía de marca: V1 honesta, V2 con lenguaje de entrevistados reales
- Compra defensiva de sledpull.com: evaluar a 30 días según tracción

## Histórico de versiones

- **v1.0 (2026-05-09):** decisión inicial de hacer landing con nombre tentativo
- **v1.1 (2026-05-09):** decisión final del nombre Sled Pull
- **v1.2 (2026-05-09):** dominio principal sledpull.app confirmado y comprado, .com pospuesto
