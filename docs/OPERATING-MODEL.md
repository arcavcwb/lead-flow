# Modelo Operacional del Squad — Lead Flow Engine v1.0

> Documento maestro del modelo operacional. Define **quién hace qué**, **con qué modelo de IA**, **en qué momento** y **dónde el humano decide**. Si otra documentación contradice este archivo en materia de roles, estados o Gates, **este archivo manda**.

---

## 1. Propósito y one-liner

**One-liner:** Construir el ecosistema SaaS White-Label de captura de leads B2B/B2C que conecta prospectos con vendedores vía WhatsApp en **menos de 5 segundos**, usando un SDK SolidJS inyectable, Supabase como bóveda de datos y n8n como motor de automatización.

**Propósito de este documento:** Describir el modelo operacional del squad Lead Flow Engine — un esquadrón de roles especializados donde **un solo motor de IA (Antigravity / Gemini) opera en diferentes modos y modelos según el tipo de tarea**, coordinados sin conversación directa entre sesiones. El humano mantiene el control estratégico en tres puntos de control (*Gates*).

**Reglas fundacionales (no negociables):**

1. **Plane es la única fuente de verdad.** Todo ticket, estado, comentario y entregable fluye por Plane. Lo que no está en Plane, no existe.
2. **El PRD Maestro y el SPEC son contratos, no sugerencias.** Nada se implementa si no está mapeado en el PRD y especificado en el SPEC.
3. **Ningún agente salta un Gate.** Los tres Gates humanos son bloqueantes.
4. **Los escenarios Gherkin son el único criterio de aceptación.** Escenario sin cobertura = criterio **NO** cumplido.

---

## 2. Tabla de roles y modelos

| Fase | Rol | Actor / Modelo | Herramienta | Entregable | Gate |
| --- | --- | --- | --- | --- | --- |
| **Fase Zero — PRD** | Product Owner | **Humano + Antigravity Pro** (Gemini Pro) | Antigravity + Plane | `docs/1_PRD.md` + tickets en Backlog | **GATE 0** — el humano aprueba el PRD |
| **Análisis — SPEC** | Analista (Líder Técnico) | **Antigravity Pro** (Gemini Pro) | Antigravity + Plane | `docs/SPEC-EX.md` con escenarios Gherkin | **GATE 1** — el humano aprueba el SPEC |
| **Implementación** | Implementador | **Antigravity Pro** (Gemini Pro) | Antigravity + repo + Plane | Código en branch `feature/EX` | — (transición interna) |
| **Testing** | Tester | **Antigravity Flash ⚡** (Gemini Flash) | Antigravity Flash + repo + Plane | Tests cubriendo cada escenario Gherkin | — (transición interna) |
| **Revisión** | Revisor | **Claude Opus** 🔵 | Antigravity (modo Claude Opus) + Plane + Git | Auditoría del PR contra el SPEC | **GATE final** — el humano hace el merge |

### Lógica de selección de modelo

| Tarea | Modelo | Razón |
| --- | --- | --- |
| Escritura de SPEC, análisis arquitectónico, planning | **Gemini Pro** | Razonamiento profundo, coherencia con PRD |
| Implementación de código (SDK, Edge Functions, tests E2E complejos) | **Gemini Pro** | Lógica compleja, Shadow DOM, Deno, SolidJS |
| Testing de unidad, validaciones Gherkin, linting | **Gemini Flash ⚡** | Velocidad + ahorro de tokens en ciclos repetitivos |
| **Auditoría de PR vs. SPEC (Revisión)** | **Claude Opus 🔵** | Arquitectura distinta a Gemini = revisión verdaderamente independiente, sin los mismos puntos ciegos. Es el auditor externo del sistema. |
| Sync de Plane, actualizaciones de estado | **Gemini Flash ⚡** | Operación mecánica, sin razonamiento complejo |

> **Regla de oro del modelo:**
> - Diseñar, analizar, implementar → **Gemini Pro**
> - Validar rápido, sincronizar → **Gemini Flash ⚡**
> - Auditar con perspectiva independiente → **Claude Opus 🔵**
>
> La separación Gemini (implementa) / Claude (revisa) reproduce la independencia arquitectónica del modelo CNDR original, pero dentro de un único entorno Antigravity.

---

## 3. El ciclo de un ticket a través de Plane

Cada entrega (`EX`) recorre estos estados de Plane. El flujo es lineal hacia adelante, con **un único salto hacia atrás permitido**: de revisión/pruebas de vuelta a desarrollo cuando algo falla.

```
Backlog → Refinado → En desarrollo → En pruebas → En revisión → Hecho
   │         │            │              │             │           │
  (Pro)     (Pro)        (Pro)         (Flash)       (Pro)    (Humano)
              │                                          │
           GATE 1                                   GATE final
```

**Recorrido detallado:**

1. **Backlog** — *(origen: Fase Zero)*
   - Aquí residen las entregas extraídas del `docs/1_PRD.md` tras la aprobación del **GATE 0**.
   - Nadie toca el código. Es el pool de trabajo priorizado por el humano/PO.

2. **Refinado** — *(actúa Antigravity Pro, rol Analista)*
   - Antigravity Pro toma un ticket del Backlog, lee `docs/1_PRD.md`, `docs/3_ARCHITECTURE.md` y el estado del repo, y produce `docs/SPEC-EX.md`.
   - El SPEC incluye resumen técnico, estructura de componentes, **escenarios Gherkin obligatorios** y el desglose de subtareas.
   - Al terminar, el ticket queda en **Refinado** con el SPEC vinculado.
   - **GATE 1 (bloqueante):** el humano aprueba el SPEC. Sin aprobación, el ticket **no** avanza a implementación.

3. **En desarrollo** — *(actúa Antigravity Pro, rol Implementador)*
   - Antigravity Pro lee el SPEC aprobado, crea el branch `feature/EX`, mueve el ticket a **En desarrollo** y escribe el código **exactamente como está especificado**.
   - Usa SolidJS + Shadow DOM + Vite para SDK; Deno + TypeScript para Edge Functions. Commits atómicos: `feat(EX): ...`.
   - Al terminar, comenta en el ticket que la implementación está lista.

4. **En pruebas** — *(actúa Antigravity Flash ⚡, rol Tester)*
   - Antigravity Flash mueve el ticket a **En pruebas** y escribe/ejecuta los tests que cubren **cada escenario Gherkin** del SPEC (Playwright / Vitest según el escenario).
   - **Si algo falla:** devuelve el ticket a **En desarrollo** y comenta los errores.
   - **Si todo pasa:** hace commit de los tests, documenta el reporte y avanza a revisión.

5. **En revisión** — *(actúa Antigravity Pro, rol Revisor)*
   - Antigravity Pro mueve el ticket a **En revisión** y audita el PR **mecánicamente contra el SPEC**: verifica que cada escenario Gherkin tenga cobertura, que las convenciones SolidJS/Deno sean respetadas y que no haya riesgos evidentes (código muerto, `console.log`, dependencias pesadas).
   - Emite el veredicto:
     - **CAMBIOS SOLICITADOS** → devuelve a **En desarrollo**.
     - **APROBADO** → comenta en el ticket que está listo para el merge humano.
   - **GATE final (bloqueante):** el humano revisa y **hace el merge**. Antigravity nunca hace merge.

6. **Hecho** — *(cierra el Humano)*
   - Tras el merge, el ticket pasa a **Hecho**. La funcionalidad está aprobada y en branch principal.

---

## 4. La frontera: sesión de análisis ⟷ sesión de implementación

En este modelo, **Antigravity es el único motor de IA**, pero opera en **sesiones separadas** con **modelos distintos** según el rol. Las sesiones nunca se hablan directamente.

**La interfaz entre sesiones es exclusivamente:**

- **Plane** — para estado, asignación, comentarios y trazabilidad.
- **El repositorio** — para el contrato (`docs/SPEC-EX.md`), el PRD, el código y los tests.

```
     SESIÓN ANALISTA/REVISOR (Pro)            FRONTERA                SESIÓN IMPLEMENTADOR/TESTER (Pro/Flash)
   ┌──────────────────────────────┐     ┌──────────────────┐     ┌──────────────────────────────┐
   │ Analista: escribe SPEC       │ ──► │  Plane + Repo    │ ──► │ Implementador: código        │
   │ Revisor: audita PR vs SPEC   │ ◄── │  (SPEC, código,  │ ◄── │ Tester: tests Gherkin        │
   │ Humano: PRD + Gates          │     │  estados, PR)    │     │                              │
   └──────────────────────────────┘     └──────────────────┘     └──────────────────────────────┘
```

| Situación | Cómo se resuelve |
| --- | --- |
| El Analista necesita comunicar algo al Implementador | Escribe en el **SPEC** o en un **comentario del ticket** en Plane |
| El Implementador encuentra una ambigüedad en el SPEC | **Detiene la implementación** y comenta en el ticket. No adivina. El humano/Analista corrige el SPEC |
| El Implementador terminó | Cambia el **estado en Plane** y sube el **PR**. El Revisor lo detecta por Plane/Git |
| El Revisor pide cambios | Deja **comentarios en el PR** y devuelve el ticket a *En desarrollo* en Plane |

---

## 5. El SPEC / Gherkin como contrato de ejecución

`docs/SPEC-EX.md` **no es documentación descriptiva: es un contrato de ejecución**. El Implementador ejecuta **literalmente** lo que el SPEC dice; **no interpreta intención, no rellena lagunas, no infiere lo "obvio"**.

**Forma canónica de cada criterio en el SPEC:**

```gherkin
Escenario: <nombre claro y único>
  Dado <estado/contexto inicial>
  Cuando <acción del usuario o del sistema>
  Entonces <resultado observable y verificable>
```

Si un criterio del PRD no puede expresarse como Gherkin verificable, **no está listo para pasar a implementación**.

---

## 6. Stack técnico y convenciones de archivos

**Stack Lead Flow Engine:**

| Capa | Tecnología | Nota |
| --- | --- | --- |
| SDK Widget | **SolidJS + Shadow DOM + Vite** | Bundle IIFE < 50kb |
| Web Component | **solid-element** | Aislamiento CSS total |
| Backend / Gatekeeper | **Supabase Edge Functions (Deno)** | CORS + Rate Limiting + RLS |
| Base de datos | **Supabase PostgreSQL** | 3 tablas + RLS |
| Automatización | **n8n (VPS)** | Modo webhook-only + Dead Letter Queue |
| Mensajería | **WAHA (WhatsApp HTTP API)** | WhatsApp, VPS propio |
| Gestión | **Plane** (via API) | Única fuente de verdad |
| Control de versiones | **Git + PR** | Branches `feature/EX`, commits `feat(EX): ...` |
| Testing | **Playwright + Vitest** | Elegido por escenario en el SPEC |
| Paquetes | **pnpm workspaces** | Monorepo |

**Convenciones de archivos (localización fija):**

| Archivo | Ubicación | Dueño / Rol | Contenido |
| --- | --- | --- | --- |
| `docs/1_PRD.md` | `/docs` | Product Owner | Requisitos, entregas, criterios de aceptación |
| `docs/SPEC-EX.md` | `/docs` | Analista (Antigravity Pro) | Contrato técnico + escenarios Gherkin |
| `docs/OPERATING-MODEL.md` | `/docs` | Este documento | Modelo operacional del squad |
| `docs/HANDOFF-PROTOCOL.md` | `/docs` | Protocolo | Transiciones de estado y handoffs |
| `docs/STATE.md` | `/docs` | Estado vivo | Estado actual de entregas |
| Agentes | `.agents/agent/` | Squad | Especialistas del AG Kit |

---

## 7. Lo que cada parte NO hace

**Antigravity Pro (Analista + Revisor) NO:**
- ❌ **No hace merge.** Aprueba técnicamente, pero el merge es del humano (GATE final).
- ❌ **No aprueba sus propios Gates.** El PRD y el SPEC son aprobados por el humano.
- ❌ **No inventa lógica no especificada.** Si algo no está en el SPEC → `__PENDIENTE__` + comenta en Plane.

**Antigravity Pro (Implementador) NO:**
- ❌ **No decide arquitectura.** No cambia el enfoque técnico definido en el SPEC.
- ❌ **No introduce dependencias pesadas** salvo que el SPEC lo indique explícitamente.
- ❌ **No audita su propio trabajo como Revisor.** La revisión final es una sesión separada.

**Antigravity Flash (Tester) NO:**
- ❌ **No escribe el SPEC ni diseña los casos de prueba.** Los Gherkin vienen del SPEC.
- ❌ **No decide si un test "casi pasa".** Verde = verde. Rojo = devuelve a desarrollo.

**El Humano (Product Owner + dueño de los Gates) NO:**
- ❌ **No delega la decisión de los Gates.** GATE 0 (PRD), GATE 1 (SPEC) y GATE final (merge) son suyos e intransferibles.

**Ningún agente (regla transversal) NO:**
- ❌ **No salta un Gate.**
- ❌ **No trata un escenario Gherkin como opcional.**
- ❌ **No usa el chat como canal de handoff entre sesiones.** Toda coordinación ocorre en Plane y el repo.
