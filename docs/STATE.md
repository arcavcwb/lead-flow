# STATE — arranque en frío (lee esto primero)

> **Para cualquier agente/persona que entra sin contexto.** Esta página orienta en 1 minuto. La **memoria del proyecto vive en los artefactos (repo + Plane), no en la cabeza de ningún agente** — si algo no está aquí, en el SPEC o en Plane, no existe. Perder el contexto de una sesión no cuesta nada: se recarga releyendo estos archivos.

## Qué es

**Lead Flow Engine** — Ecosistema SaaS White-Label B2B de captura de leads. Un SDK SolidJS inyectable (< 50kb, Shadow DOM) que captura prospectos y los notifica al vendedor vía WhatsApp en **menos de 5 segundos**. Backend: Supabase Edge Functions + PostgreSQL. Automatización: n8n en VPS propio + WAHA (WhatsApp HTTP API).

## Roles y modelos IA (flujo Lead Flow)

| Rol | Actor | Modelo | Hace |
| --- | --- | --- | --- |
| **Analista + Product Owner** | **Antigravity** | **Gemini Pro** | Escribe los SPEC (`docs/SPEC-EX.md`) y analiza requisitos del PRD. **No implementa.** |
| **Implementador** | **Antigravity** | **Gemini Pro** | Implementa leyendo el SPEC + Plane. Es **ciego al contexto**: solo existe lo que está escrito. |
| **Tester** | **Antigravity** | **Gemini Flash ⚡** | Valida cada escenario Gherkin. Rápido y token-eficiente. |
| **Revisor** | **Antigravity** | **Claude Opus 🔵** | Audita el PR contra el SPEC con perspectiva de arquitectura distinta (Gemini/Claude). Máxima independencia de revisión. |
| **Gates (decisión)** | **Humano** | — | GATE 0 (PRD), GATE 1 (aprueba SPEC), GATE final (merge). |

Las sesiones de IA **nunca se hablan directamente** — el handoff es vía **Plane** (estado + etiqueta + comentario corto) + **repo** (SPEC, branch, PR).

**Lógica de selección de modelo:**
- Analizar, diseñar, implementar → **Gemini Pro**
- Testear, validar, sincronizar Plane → **Gemini Flash ⚡**
- Auditar PR vs SPEC (revisión independiente) → **Claude Opus 🔵**

## Estado de las entregas

| ID Plane | Épica / Módulo | Descripción Corta | Estado | Cycle / Sprint |
| --- | --- | --- | --- | --- |
| **LEADFLOW-01** | Infraestructura | Configuración Git, vínculo a remoto, identidad y documentación | 🔄 En desarrollo | Cycle 0 |
| **LEADFLOW-02** | Infraestructura | Setup Monorepo (pnpm workspaces) `apps/sdk` y `supabase/` | 🔄 En desarrollo | Cycle 0 |
| **LEADFLOW-03** | Infraestructura | Reglas de Calidad (Prettier, ESLint) y CI (GitHub Actions) | 🔄 En desarrollo | Cycle 0 |
| **LEADFLOW-04** | SDK Frontend | Scaffold SolidJS + Vite + Web Components (solid-element) | ⬜ Backlog | Cycle 2 |
| **LEADFLOW-05** | Backend & Bóveda | Schema de base de datos (Supabase) + RLS + Edge stub | ⬜ Backlog | Cycle 1 |
| **LEADFLOW-06** | Backend & Bóveda | Gatekeeper: CORS, Rate Limiting, Honeypot, Vault Insert | ⬜ Backlog | Cycle 1 |
| **LEADFLOW-07** | SDK Frontend | Lead Form: UI mobile-first, inputs semánticos, theme dinámico | ⬜ Backlog | Cycle 2 |
| **LEADFLOW-08** | Automatización | Workflow n8n (webhook) → G.Sheets + WAHA (WhatsApp HTTP API) + DLQ | ⬜ Backlog | Cycle 3 |
| **LEADFLOW-09** | SDK Frontend | QA: Playwright E2E Shadow DOM Inmune + Tests | ⬜ Backlog | Cycle 2 |
| **LEADFLOW-10** | Infraestructura | Deploy VPS, Docker, Caddy y configuración de prod | ⬜ Backlog | Cycle 3 |

> Actualizar esta tabla al cerrar cada entrega.

## Convenciones (obligatorias)

- **Idioma:** español para docs, comentarios de Plane y commits. El código en inglés.
- **Branch** `feature/EX` · **commits** `feat(EX): …` · **SPEC** `docs/SPEC-EX.md` · **tests** `tests/e2e/EX.spec.ts` o `tests/unit/EX.test.ts`.
- **Criterio de aceptación = los escenarios Gherkin del SPEC.** Escenario sin test = criterio no cumplido.
- **Portón de auto-check** (antes de devolver): `pnpm build:sdk && pnpm lint && pnpm typecheck` **verdes** + árbol limpio.
- **Regla de oro del Implementador:** NO INVENTAR. Contenido verbatim del SPEC; si falta/es ambiguo → `__PENDIENTE__` + comentar en el ticket.
- **Disciplina de alcance:** tocar solo los archivos que el SPEC nombra.
- **PR:** el **Revisor (Pro) abre el PR tras APROBADO**; el **humano hace el merge** (GATE final). Nadie hace self-merge.

## Ciclo de una entrega

```
SPEC (Antigravity Pro) → GATE 1 (humano) → Refinado
  → Pro implementa (En desarrollo → push del branch)
  → Flash testea (En pruebas → auto-check verde)
  → Pro audita (En revisión → Pro abre PR si APROBADO)
  → GATE final (humano hace merge) → Hecho
```

## Línea de handoff (el humano pega en la sesión de Antigravity)

> Implementá `LEADFLOW-XX`: leé `docs/SPEC-EX.md` + comentarios del ticket, seguí el `docs/HANDOFF-PROTOCOL.md` al pie, usá modelo **Pro** para implementar y **Flash** para testear, y no lo devuelvas hasta que `pnpm build:sdk && pnpm lint && pnpm typecheck` estén en verde y commiteado/pusheado.

## Dónde está cada cosa

- **Fuente de negocio:** `docs/1_PRD.md`
- **Modelo de negocio:** `docs/2_BUSINESS_MODEL.md`
- **Arquitectura técnica:** `docs/3_ARCHITECTURE.md`
- **Go-to-Market:** `docs/4_GO_TO_MARKET.md`
- **Protocolo QA:** `docs/5_QA_PROTOCOL.md`
- **Revisión arquitectónica:** `docs/6_ARCHITECT_REVIEW.md`
- **Modelo operacional:** `docs/OPERATING-MODEL.md`
- **Protocolo de handoff:** `docs/HANDOFF-PROTOCOL.md`
- **Agentes especializados:** `.agents/agent/` (AG Kit)
- **Scripts de validación:** `.agents/scripts/`

## Reutilizar este flujo en otros proyectos

El "kit portátil" a copiar: `.agents/` (AG Kit completo), `docs/HANDOFF-PROTOCOL.md`, `docs/OPERATING-MODEL.md`, este `docs/STATE.md` (como template — cambiar tabla de estado y tickets). La lógica del flujo no cambia; cambia el contenido del proyecto y el stack técnico.
