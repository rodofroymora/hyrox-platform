# Sled Pull Landing

Landing page para captura de waitlist del producto Sled Pull.

## Stack técnico
- Next.js 16 (App Router) + TypeScript
- Tailwind CSS para estilos
- Framer Motion para animaciones
- Lucide React para íconos
- Zod + React Hook Form para validación
- Loops para captura y email marketing
- Vercel para hosting
- Cloudflare DNS

## Setup local

1. Copia variables de entorno: `cp .env.local.example .env.local`
2. Edita `.env.local` con credenciales reales (NO commits)
3. Instala: `npm install`
4. Arranca: `npm run dev`
5. Abre http://localhost:3000

## Deploy

Push a main triggerea deploy automático en Vercel.
Branch protection requiere PR + CI antes de merge.

## Estructura

```
apps/landing/
├── app/[locale]/         # Pages con i18n (ES/EN)
├── components/           # Componentes UI
├── lib/                  # Utilities (i18n, Loops, types)
└── public/               # Assets estáticos
```

## Documentación
- ADR-006: `docs/adrs/ADR-006-landing-and-waitlist.md`
- PRD: `docs/PRD_v1.0.docx`
