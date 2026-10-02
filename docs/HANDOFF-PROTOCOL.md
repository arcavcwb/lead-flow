# Protocolo de handoff — Lead Flow v2.0

> Estado: **APROBADO COMO BASELINE; COMMIT PENDIENTE**
> orch registra estado y ejecución; Git transporta artefactos; los gates humanos transportan autoridad.

## 0. Cadena Codex → orch → Gemini

```text
Codex: define arquitectura, agente, skills, alcance y verificación
  → orch: registra ID, dependencias, estado y worktree
  → Gemini/Antigravity: ejecuta solo la tarea aprobada
  → Codex: revisa diff, evidencia y bloqueos
  → Product Owner: concede merge/release o solicita cambios
```

El chat o la visibilidad simultánea de los sidebars no son parte de la autoridad. Si Codex o Gemini no ven el otro panel, continúan leyendo los mismos archivos y entregando el formato de este protocolo.

## 1. Identidad de una entrega

El ID `LEADFLOW-XX` debe aparecer en:

- ID de tarea orch.
- SPEC `docs/SPEC-LEADFLOW-XX.md`.
- Branch `feature/LEADFLOW-XX-slug` o `fix/LEADFLOW-XX-slug`.
- Commits `type(LEADFLOW-XX): descripción`.
- Título/cuerpo del PR.
- Evidencia de QA.

Un ticket representa un resultado verificable. Si requiere más de un contrato independiente, se divide antes de GATE 1.

## 2. Transiciones

| Transición | Quién | Entrega obligatoria | Gate |
| --- | --- | --- | --- |
| Crear → `todo` | Product Owner | Brief, valor, límites y prioridad | GATE 0 vigente |
| `todo` → `ready` | Analista/Humano | SPEC + Gherkin + riesgos aprobados | GATE 1 |
| `ready` → `in-progress` | Implementador | Declaración de inicio y worktree | GATE 1 vigente |
| `in-progress` → `review` | Implementador/Tester | SHA, auto-check y evidencia por escenario | — |
| `review` → `in-progress` | Revisor | Hallazgos accionables | — |
| Cualquier estado → `blocked` | Actor actual | Condición, evidencia y decisión requerida | — |
| `review` → `done` | Humano | Merge + cierre | GATE 3 |

En Lead Flow, el implementador operativo es Gemini/Antigravity. Codex no considera evidencia una implementación que no haya sido revisada sobre diff y comandos.

GATE 2 se solicita en la etapa donde surja una escritura externa y no se reutiliza para otra operación.

## 3. Etiquetas canónicas

| Etiqueta | Actor | Significado |
| --- | --- | --- |
| `gate-0-ok` | Humano | Baseline v2 aprobada |
| `spec-listo` | Analista | SPEC espera decisión |
| `spec-aprobado` | Humano | GATE 1 para versión citada |
| `remote-write-requested` | Agente | Operación remota documentada, no autorizada |
| `remote-write-approved` | Humano | GATE 2 con target/ventana exactos |
| `listo-para-revision` | Tester | Evidencia completa para SHA |
| `cambios-solicitados` | Revisor | Rechazo accionable |
| `aprobado-para-merge` | Revisor | Revisión técnica aprobada; falta humano |
| `bloqueado` | Actor actual | No puede avanzar sin condición externa |

Las etiquetas sin comentario/versiones asociadas no conceden autoridad suficiente.

## 4. Handoff Analista → Humano

```markdown
SPEC listo: `docs/SPEC-LEADFLOW-XX.md`
Versión/commit: `<versión> / <sha>`
Objetivo: <resultado único>
Decisiones humanas: <lista>
Riesgos: <lista>
Requiere escritura remota: sí/no; cuál
Verificación prevista: <resumen>

Solicito GATE 1. No se inició implementación.
```

## 5. Inicio de implementación

```markdown
Inicio LEADFLOW-XX
- Rol/sesión: Implementador Gemini
- SPEC aprobado: `<archivo> @ <sha/versión>`
- Evidencia GATE 1: `<comentario/etiqueta>`
- Branch: `feature/LEADFLOW-XX-slug`
- Archivos permitidos: <lista>
- Exclusiones: <lista>
- GATE 2 previsto: sí/no
- Verificación: <comandos>
```

Si el branch ya contiene cambios ajenos al ticket, el implementador debe aislar alcance o bloquear; nunca los descarta.

## 6. Solicitud de GATE 2

```markdown
REMOTE WRITE REQUEST — LEADFLOW-XX
- Servicio/cuenta: <target exacto>
- Entorno: staging | production
- Operación exacta: <comando/acción sin secreto>
- Motivo: <criterio del SPEC>
- Preview/dry-run: <evidencia>
- Impacto esperado: <objetos/recursos>
- Backup/rollback: <procedimiento>
- Verificación posterior: <consulta/smoke test>
- Ventana/expiración: <una ejecución o periodo>

Estado: ESPERANDO APROBACIÓN. No ejecutado.
```

La respuesta humana debe identificar el mismo target y alcance. “Dale”, dado en otro contexto, no se extrapola.

## 7. Implementador → Tester

```markdown
Implementación lista — LEADFLOW-XX
- Commit: `<sha>`
- Cambios: <3–5 puntos>
- SPEC: `<archivo @ versión>`
- Auto-check: <comandos + resultado>
- Mutaciones remotas: ninguna | <evidencia GATE 2 + resultado>
- Riesgos conocidos/exclusiones: <lista>

Mover a `review` para pruebas.
```

## 8. Tester → Revisor

```markdown
QA listo — LEADFLOW-XX
- Commit probado: `<sha>`
- Entorno: local | staging
- Gherkin: X/X cubiertos
- Tests: N pass, 0 fail, 0 omitidos no aprobados
- Métricas: <cuando aplique>
- Hallazgos: ninguno | <lista>
- Evidencia: <CI/artefacto>

Etiqueta: `listo-para-revision`
```

Si falla, vuelve a `in-progress` con escenario, esperado, observado y reproducción; no corrige silenciosamente el criterio.

## 9. Revisor → Humano

El reviewer usa una sesión limpia y revisa el diff, no la explicación del implementador como sustituto.

```markdown
REVIEW — LEADFLOW-XX
- Commit revisado: `<sha>`
- SPEC: `<archivo @ versión>`
- Alcance: conforme/no conforme
- Seguridad/privacidad: conforme/no conforme
- Tests: suficientes/insuficientes
- Hallazgos bloqueantes: <lista>
- Hallazgos no bloqueantes: <lista>
- Veredicto: APROBADO | CAMBIOS SOLICITADOS
```

`APROBADO` añade `aprobado-para-merge`, pero solo el humano concede GATE 3 y hace merge.

## 10. PR obligatorio

```markdown
## LEADFLOW-XX — <título>

- Tarea orch: <id>
- SPEC aprobado: `docs/SPEC-LEADFLOW-XX.md` @ <versión/sha>
- Implementación: <sha>
- GATE 1: <evidencia>
- GATE 2: no aplica | <evidencia>

### Resultado
- <cambios>

### Gherkin y pruebas
- [x] <escenario> → <test/evidencia>

### Riesgos y rollback
- <riesgo>
- <rollback>

### Fuera de alcance
- <lista>
```

## 11. Reanudación tras pérdida de contexto

Una sesión nueva no confía en un resumen de chat como autoridad. Debe releer `STATE`, fuentes, ticket, SPEC, branch/diff y último comentario de handoff. Continúa desde el último artefacto verificable; no rehace trabajo concluido ni inventa decisiones ausentes.

## 12. Contenido prohibido en handoffs

- Valores de `.env`.
- Tokens, PAT, contraseñas o claves.
- URLs firmadas o connection strings.
- Teléfonos, emails o payloads reales sin redacción.
- Logs completos que puedan contener secretos.
- Afirmaciones “todo funciona” sin comando, SHA y resultado.
