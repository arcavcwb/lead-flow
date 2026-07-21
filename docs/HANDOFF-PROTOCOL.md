# HANDOFF-PROTOCOL — Lead Flow Engine v1.0

> **Qué es este documento.** El pegamento operacional del flujo Lead Flow Engine. Define, para cada transición de estado en Plane, **quién actúa, qué modelo usa, qué artefacto produce (archivo + ubicación exacta), qué comentario/etiqueta deja en el ticket que activa al próximo actor, y qué Gate humano lo bloquea.**
>
> **Regla madre.** La frontera entre sesiones de Antigravity (Analista/Revisor vs. Implementador/Tester) **no es una conversación**. Las sesiones **nunca se hablan directamente**: ambas leen y escriben en **Plane** (estados, comentarios, etiquetas) y en el **repositorio** (archivos, branches, PRs). Todo handoff ocurre a través de esos dos canales. Si algo no está escrito en Plane o en el repo, no existe.

---

## 1. Actores, roles y modelos

| Rol | Actor / Modelo | Herramienta | Escribe en |
| --- | --- | --- | --- |
| **Product Owner** (Fase Zero / PRD) | Humano + **Antigravity Pro** (Gemini Pro) | Antigravity | `docs/1_PRD.md`, Plane (Backlog) |
| **Analista** (SPEC + Gherkin) | **Antigravity Pro** (Gemini Pro) | Antigravity + Plane API | `docs/SPEC-EX.md`, Plane |
| **Implementador** (SolidJS + Deno + n8n) | **Antigravity Pro** (Gemini Pro) | Antigravity + Plane API | Repo (branches, código), Plane |
| **Tester** (cobertura Gherkin) | **Antigravity Flash ⚡** (Gemini Flash) | Antigravity Flash + Plane API | Repo (tests), Plane |
| **Revisor** (auditar PR vs SPEC) | **Claude Opus 🔵** | Antigravity (modo Claude Opus) + Plane API + git | Comentarios en PR, Plane |
| **Merge / decisión** | **Humano** | Plane + Git host | `main`, Plane |

> **La entrega es la unidad de trabajo.** Todo ticket es identificado como `EX`. Ese identificador atraviesa el Plane, el branch (`feature/EX`), los commits (`feat(EX): …`), el SPEC (`docs/SPEC-EX.md`) y el PR. Es la clave que conecta los cuatro canales.

---

## 2. Estados canónicos en Plane

El tablero usa exactamente estos seis estados. No se inventan otros.

| Estado | Significado | Actor que trabaja |
| --- | --- | --- |
| `Backlog` | Entrega creada a partir del PRD, sin plan técnico aún. | — (aguardando GATE 0) |
| `Refinado` | Tiene un SPEC con Gherkin, listo para revisión humana. | Antigravity Pro (Analista) terminó; aguarda GATE 1 |
| `En desarrollo` | Está siendo construido (o corregido tras rechazo). | Antigravity Pro (Implementador) |
| `En pruebas` | Implementación completa; se valida cada Gherkin. | Antigravity Flash (Tester) |
| `En revisión` | PR abierto; Antigravity Pro audita contra el SPEC. | Antigravity Pro (Revisor) |
| `Hecho` | PR mergeado en `main` por el humano. | — (cerrado) |

---

## 3. Gates humanos (donde el humano decide)

Solo **tres** puntos donde el humano bloquea el flujo. Ningún agente los cruza solo.

| Gate | Bloquea la transición | Quién decide | Cómo se libera |
| --- | --- | --- | --- |
| **GATE 0** | `Backlog` no avanza al Analista hasta aprobar el PRD | Humano | Comentario "PRD aprobado" + etiqueta `gate-0-ok` |
| **GATE 1** | `Refinado` → `En desarrollo` | Humano | Etiqueta `spec-aprobado` |
| **GATE final** | `En revisión` → `Hecho` (el merge) | Humano | El humano hace el merge del PR manualmente |

---

## 4. Mapa de transiciones (tabla maestra)

| # | Transición (De → A) | Actor / Modelo | Artefacto producido | Trigger en Plane | Gate |
| --- | --- | --- | --- | --- | --- |
| **T0** | (nueva) → `Backlog` | Product Owner (Humano + Pro) | `docs/1_PRD.md` + ticket `EX` por entrega | Ticket creado en `Backlog` con criterios de aceptación | **GATE 0**: humano aprueba PRD (`gate-0-ok`) |
| **T1** | `Backlog` → `Refinado` | Analista (**Pro**) | `docs/SPEC-EX.md` con escenarios **Gherkin** | Estado `Refinado` + etiqueta `spec-listo` + comentario "SPEC listo para GATE 1 → `docs/SPEC-EX.md`" | **GATE 1**: humano aprueba el SPEC |
| **T2** | `Refinado` → `En desarrollo` | Implementador (**Pro**) | Branch `feature/EX` + código en `apps/sdk/src/` o `supabase/functions/` | Detecta `Refinado` + `spec-aprobado`; mueve a `En desarrollo` y comenta "Branch `feature/EX` creado, implementando" | — (GATE 1 ya superado) |
| **T3** | `En desarrollo` → `En pruebas` | Tester (**Flash ⚡**) | Tests en `tests/e2e/EX.spec.ts` o `tests/unit/EX.test.ts` | Estado `En pruebas` + comentario "Implementación completa, commits `feat(EX):`, cubriendo Gherkin" | — |
| **T4** | `En pruebas` → `En revisión` | Revisor (**Claude Opus 🔵**) recibe | Branch `feature/EX` commiteado + auto-check verde | Estado `En revisión` + etiqueta `listo-para-revision` + comentario con resumen y checklist de Gherkin cubiertos | — |
| **T5a** | `En revisión` → `Hecho` | **Claude Opus 🔵** abre PR → **Humano** hace merge | PR `feature/EX` → `main` (template §5) | Etiqueta `aprobado-para-merge` + comentario "Veredicto: **APROBADO**, PR abierto, listo para merge" | **GATE final**: humano hace el merge |
| **T5b** | `En revisión` → `En desarrollo` | Revisor (**Claude Opus 🔵**) — rechazo | Comentarios línea por línea en el PR | Estado `En desarrollo` + etiqueta `cambios-solicitados` | — |
| **T3b** | `En pruebas` → `En desarrollo` | Tester (**Flash ⚡**) — rechazo interno | Reporte de fallos en el comentario | Estado `En desarrollo` + comentario "Falla Gherkin N: …" | — |

---

## 5. Convención de branches, commits y PRs

### Branches

- **Un branch por entrega:** `feature/EX` (ej. `feature/E1-monorepo-setup`).
- **Base:** siempre desde `main` actualizado.
- Nunca se trabaja directamente sobre `main`.

### Commits (Conventional Commits, con el ID de la entrega)

- `feat(EX): descripción` — nueva funcionalidad / componente.
- `test(EX): descripción` — tests que cubren Gherkin.
- `fix(EX): descripción` — correcciones tras un rechazo.
- `chore(EX): descripción` — configuración, scaffolding.
- Commits **atómicos**; cada uno compila.

### Pull Requests

- **Quién abre:** el **Revisor (Antigravity Pro)**, **después** de emitir el veredicto APROBADO.
- **Título:** `EX: <resumen corto>`.
- **Base:** `main` ← **compare:** `feature/EX`.
- **Cuerpo del PR (template obligatorio):**

```markdown
## EX — <título>

- **Ticket Plane:** <URL del ticket>
- **Contrato (SPEC):** docs/SPEC-EX.md
- **Modelo IA:** Implementado por Antigravity Pro · Testeado por Antigravity Flash

### Escenarios Gherkin cubiertos

- [x] Escenario 1: <nombre> → test `tests/e2e/EX...`
- [x] Escenario 2: <nombre> → test `tests/unit/EX...`

### Notas

- <decisiones de implementación, assets nuevos, etc.>
```

- **Nadie hace self-merge.** El merge es el **GATE final**, exclusivo del humano.

---

## 6. Handoff Analista → Implementador (entrega del SPEC)

Así viaja el contrato del Analista (Pro) al Implementador (Pro), **sin que se hablen**:

1. **Antigravity Pro (Analista)** produce `docs/SPEC-EX.md`. El SPEC debe ser **autocontenido y sin ambigüedad**: el Implementador ejecuta literalmente lo que está escrito.
2. Mueve el ticket a `Refinado`, coloca la etiqueta `spec-listo` y comenta con el link al SPEC solicitando el **GATE 1**.
3. **El humano revisa el SPEC.** Si lo aprueba:
   - Agrega la etiqueta **`spec-aprobado`** (este es el disparador real hacia el Implementador).
4. **Antigravity Pro (Implementador)** detecta el ticket en `Refinado` + `spec-aprobado`, lo toma, crea `feature/EX`, mueve a `En desarrollo` y comienza a implementar leyendo **solo** `docs/SPEC-EX.md` + `docs/3_ARCHITECTURE.md` + el repo.

> **Regla de oro del Implementador (ciego al contexto):** NO INVENTES. Si algo falta o el SPEC es ambiguo, usa `__PENDIENTE__` **y comenta en el ticket**. Nunca rellenes con una suposición plausible. Un dato falso invisible es peor que un `__PENDIENTE__` visible.

---

## 7. Handoff Implementador/Tester → Revisor (devolución para revisión)

Así vuelve el trabajo terminado al Revisor (Pro):

1. **Antigravity Flash (Tester)** confirma que cada Gherkin tiene test verde y hace el commit (`test(EX): …`).
2. Ejecuta el **portón de auto-check** (`pnpm build:sdk && pnpm lint && pnpm typecheck` — todos verdes, árbol `git status` limpio) y **pega la salida en el ticket**. Sin esto, **no devuelve**.
3. Mueve el ticket a `En revisión`, coloca la etiqueta **`listo-para-revision`** y comenta el resumen + checklist de Gherkin cubiertos.
4. **Antigravity Pro (Revisor)** detecta `En revisión` + `listo-para-revision`, audita: lee `docs/SPEC-EX.md` (sección Gherkin) contra el **diff del branch** `feature/EX`.
5. Emite veredicto → rechaza (T5b) o aprueba (T5a).
6. **Si APROBADO: el Revisor hace el `push` y abre el PR** `feature/EX` → `main`, dejándolo listo para el **GATE final** (merge humano).

---

## 8. Rechazos (vuelta a `En desarrollo`)

Un rechazo **nunca cierra** el ticket: lo devuelve a `En desarrollo` con comentarios accionables.

| Origen del rechazo | Transición | Actor / Modelo | Qué deja en Plane |
| --- | --- | --- | --- |
| **Tests fallan** (interno del Tester) | `En pruebas` → `En desarrollo` (T3b) | Flash ⚡ | Comentario "Falla en Escenario N (Gherkin): esperado X, obtenido Y" |
| **Auditoría falla** (Revisor) | `En revisión` → `En desarrollo` (T5b) | Pro | Etiqueta `cambios-solicitados` + comentarios línea por línea en el PR + comentario resumen en el ticket |

**Reglas del ciclo de rechazo:**
- El PR y el branch `feature/EX` **se conservan**; el Implementador corrige encima (`fix(EX): …`) y vuelve a empujar.
- Al re-entregar, el Tester **quita** `cambios-solicitados`, repite el ciclo §7 y vuelve a colocar `listo-para-revision`.

---

## 9. Catálogo de etiquetas de Plane (los disparadores)

Las etiquetas son las señales de handoff entre sesiones. Solo el actor indicado las coloca.

| Etiqueta | Quién la coloca | Significa / dispara |
| --- | --- | --- |
| `gate-0-ok` | Humano | PRD aprobado; el Analista puede tomar la entrega |
| `spec-listo` | Antigravity Pro (Analista) | SPEC redactado; pide **GATE 1** al humano |
| `spec-aprobado` | **Humano** (GATE 1) | Contrato aprobado; **dispara el Implementador** |
| `listo-para-revision` | Antigravity Flash (Tester) | Auto-check verde; **dispara al Revisor** |
| `cambios-solicitados` | Antigravity Pro (Revisor) | Rechazo; vuelve a `En desarrollo` |
| `aprobado-para-merge` | Antigravity Pro (Revisor) | Auditoría OK; pide **GATE final** (merge humano) |

---

## 10. Definition of Ready (DoR) — para pasar un ticket al Implementador

Checklist que **debe** cumplirse antes de colocar `spec-aprobado` (cruzar el GATE 1). Si algo falla, el ticket **no** entra en `En desarrollo`.

- [ ] Existe `docs/SPEC-EX.md` y está **aprobado por el humano** (GATE 1).
- [ ] El SPEC tiene **escenarios Gherkin** completos: al menos uno por cada criterio de aceptación del PRD.
- [ ] El SPEC es **autocontenido**: el Implementador puede ejecutarlo sin preguntar nada.
- [ ] Referencia explícita al **stack técnico** (SolidJS, Shadow DOM, Deno, Supabase) donde aplique.
- [ ] Alcance de la entrega claro: qué entra y qué **no** entra.
- [ ] Modelo IA para esta entrega especificado: Pro (implementación) + Flash (testing).

---

## 11. Definition of Done (DoD) — para cerrar un ticket

Checklist que **debe** cumplirse antes de que el humano haga el merge (GATE final) y el ticket pase a `Hecho`.

- [ ] **Cada** escenario Gherkin del SPEC tiene implementación **y** test que lo cubre.
- [ ] Todos los tests pasan (verde).
- [ ] Auto-check verde: `pnpm build:sdk && pnpm lint && pnpm typecheck`.
- [ ] PR abierto contra `main`, con template completo: link al ticket, link al SPEC, modelos IA usados.
- [ ] Sin `console.log`, sin código muerto, sin dependencias pesadas injustificadas.
- [ ] Bundle SDK < 50kb verificado con el build.
- [ ] **Antigravity Pro (Revisor)** emitió veredicto **APROBADO** (`aprobado-para-merge`).
- [ ] El **humano** hizo el merge en `main` (GATE final).
