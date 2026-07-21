# 🚀 Lead Flow Engine

> **Ecosistema SaaS B2B "White-Label" de captura de leads ultrarrápida.**

Lead Flow Engine es un sistema de captura y enrutamiento de leads diseñado para tiempos de carga extremos (TTI < 200ms), inmunidad CSS y despliegue agnóstico. Se compone de un widget inyectable, un backend serverless hiper-seguro y un motor de automatización en tiempo real hacia WhatsApp.

---

## 🏗️ Stack Tecnológico en 4 Capas

1. **Frontend (SDK Inyectable):** `SolidJS` + Web Components (Shadow DOM). Compilado con `Vite` para pesar `< 50kb` y evadir conflictos CSS de sitios heredados.
2. **Gatekeeper (Middleware):** `Supabase Edge Functions` (Deno) para control CORS estricto, honeypot anti-bots y validación multi-dominio.
3. **Bóveda (Base de Datos):** `Supabase PostgreSQL` con *Row Level Security (RLS)* bloqueando accesos anónimos. Usa `JSONB` para máxima flexibilidad *white-label*.
4. **Automatización:** `n8n` hospedado en VPS, conectado a `WAHA` (WhatsApp HTTP API) con políticas de *Dead Letter Queue (DLQ)*.

---

## 📚 Documentación y Fuente de Verdad

Este repositorio está diseñado para ser construido y auditado por un **Squad de Inteligencia Artificial (Antigravity)**. No existe conocimiento tribal; **si no está en los documentos, no existe**.

Si acabas de llegar al proyecto, tu punto de partida obligatorio es:
👉 **[SOURCE OF TRUTH](docs/SOURCE_OF_TRUTH.md)**

### 📖 Enlaces Rápidos (Pilar Estratégico)
- [1. PRD (Product Requirements Document)](docs/1_PRD.md)
- [2. Modelo de Negocio](docs/2_BUSINESS_MODEL.md)
- [3. Arquitectura Técnica](docs/3_ARCHITECTURE.md)

### 🤖 Operaciones y Tickets
- [Modelo Operacional de IA](docs/OPERATING-MODEL.md) - Cómo trabajan Pro, Flash y Claude.
- [Protocolo de Handoff](docs/HANDOFF-PROTOCOL.md) - Cómo se aprueban las fases (Gates).
- **[STATE.md](docs/STATE.md) - El estado vivo de los tickets (Plane).**

---

## 🛠️ Desarrollo Local (Monorepo)

Este proyecto utiliza `pnpm workspaces`.

```bash
# 1. Instalar dependencias
pnpm install

# 2. Correr verificaciones de calidad locales (Mismas que el CI en GitHub Actions)
pnpm lint
pnpm typecheck
```

---
*Proyecto orquestado y desarrollado por la tripulación de IA (Gemini Pro, Flash y Claude).*
