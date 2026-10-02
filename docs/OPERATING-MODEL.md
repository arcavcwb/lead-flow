# Modelo operativo — Lead Flow v2.0

> Estado: **APROBADO COMO BASELINE; COMMIT PENDIENTE**
> Plataforma de agentes soportada: Gemini CLI / Google Antigravity.
> El modelo concreto puede cambiar; gobiernan los roles, gates y evidencias.

## 1. Propósito

Permitir que sesiones de Gemini analicen, implementen, prueben y revisen Lead Flow sin perder trazabilidad ni adquirir autoridad humana por inferencia.

## 2. Principios no negociables

1. Un agente no aprueba su propio trabajo.
2. Un documento en estado `BORRADOR` no autoriza implementación.
3. Una aprobación de SPEC no autoriza escritura remota.
4. Una salida verde sin trabajo real es un fallo de gobernanza.
5. Secretos y PII no entran en chat, Git, orch ni evidencia.
6. El trabajo se limita al ticket; ampliar alcance requiere re-refinamiento.
7. Git demuestra contenido, orch registra ejecución y el humano concede autoridad.
8. Cuando hay contradicción, se detiene y se hace visible.

## 3. Roles

| Rol | Responsabilidad | Puede editar | No puede |
| --- | --- | --- | --- |
| Product Owner humano | Prioridad, riesgo, gates y release | Aprobaciones versionadas, decisiones y PR | Delegar gates implícitamente |
| Analista Gemini | Convertir ticket en SPEC verificable | SPEC y propuesta de decisión | Implementar o aprobar el SPEC |
| Implementador Gemini | Ejecutar exactamente el SPEC aprobado | Archivos permitidos del ticket | Cambiar arquitectura o tocar remoto sin gate |
| Tester Gemini | Diseñar/ejecutar pruebas desde Gherkin | Tests y reporte dentro del ticket | Rebajar criterios para hacerlos pasar |
| Revisor Gemini | Auditar diff, pruebas, seguridad y alcance | Comentarios/reporte; corrección solo si se abre ticket | Revisar como continuidad de la misma sesión implementadora |
| Release Operator humano | Autorizar merge y mutaciones remotas | Git/servicios autorizados | Asumir que CI sustituye revisión de riesgo |

Una persona puede usar el mismo modelo de Gemini para varios roles, pero debe hacerlo en sesiones separadas, recargando fuentes y sin reutilizar una autoevaluación como revisión independiente.

## 4. Fuentes de verdad

- Producto/arquitectura: documentos aprobados en Git.
- Contrato del ticket: SPEC aprobado y vinculado a una versión/commit.
- DAG y estado operativo: `tasks.json` + eventos de orch.
- Estado técnico: commit/PR concreto.
- Evidencia: CI y reportes vinculados al mismo SHA.
- Autoridad: acciones humanas de gate.

La resolución completa está en `docs/SOURCE_OF_TRUTH.md`.

## 5. Estados canónicos de ejecución

| Estado | Definición | Actor activo |
| --- | --- | --- |
| `todo` | Brief priorizado, sin SPEC aprobado | Product Owner / Analista |
| `ready` | SPEC aprobado mediante GATE 1 y dependencias completas | Humano / Implementador |
| `in-progress` | Implementación autorizada en worktree | Implementador |
| `blocked` | Condición de parada registrada | Actor actual / Humano |
| `review` | Código, pruebas y evidencia listos para auditoría | Tester / Revisor / Humano |
| `done` | Merge humano y criterios de cierre completos | Ninguno |

Los bloqueos usan el estado `blocked` y un evento estructurado. El mapeo final se valida contra la versión instalada de orch.

## 6. Gates humanos

| Gate | Autoriza | Evidencia necesaria | No autoriza |
| --- | --- | --- | --- |
| `GATE 0` | Baseline de PRD, arquitectura y plan | Versión + SHA + comentario `PRD/plan aprobado` | Implementación de cualquier ticket sin SPEC |
| `GATE 1` | Implementar un SPEC concreto | `spec-aprobado`, versión y SHA del SPEC | Deploy, migración remota o envío real |
| `GATE 2` | Una mutación externa delimitada | Target, operación, ventana, rollback y comentario `remote-write-approved` | Otras cuentas, entornos o ejecuciones futuras |
| `GATE 3` | Merge/release | Review aprobado, CI del SHA y decisión humana | Saltar smoke test o cerrar incidentes pendientes |

### Alcance de GATE 2

Requieren GATE 2, entre otros:

- `supabase link` cuando expone/accede a un proyecto real por primera vez.
- `supabase db push`, deploy de Edge Functions y cambios de secrets.
- Mutaciones manuales de orch que eludan scripts, gates o evidencia.
- Deploy a VPS o cloud.
- Envíos a números reales.
- Creación/modificación de workflows n8n remotos.
- Cualquier escritura en datos de clientes.

El gate es de una sola operación o ventana definida. No es una credencial permanente.

## 7. Flujo de un ticket

```text
todo
  │ Analista redacta SPEC
  ▼
ready ── GATE 1 humano registrado
  │
  ▼
in-progress
  │ implementación + auto-check
  ▼
review
  │ evidencia por Gherkin
  ├─ cambios solicitados → in-progress
  └─ revisión aprobada + GATE 3 → merge humano → done
```

Las mutaciones remotas que aparezcan dentro de cualquier etapa se detienen en `GATE 2` sin cambiar por sí solas el estado del ticket.

## 8. Definition of Ready

Un ticket entra a desarrollo solo si:

- [ ] La tarea existe en `tasks.json` y tiene alcance único.
- [ ] Existe un SPEC `LISTO PARA APROBACIÓN` o `APROBADO`.
- [ ] El SPEC referencia versión vigente de PRD/arquitectura.
- [ ] Entradas, salidas, errores y límites están definidos.
- [ ] Cada criterio tiene Gherkin verificable.
- [ ] Se enumeran archivos permitidos y exclusiones.
- [ ] Dependencias y riesgos están identificados.
- [ ] Se declara si necesitará GATE 2.
- [ ] El humano concedió GATE 1 para esa versión.

## 9. Definition of Done

Un ticket solo llega a `done` cuando:

- [ ] El diff coincide con el SPEC y no amplía alcance.
- [ ] Cada Gherkin tiene evidencia vinculada al SHA.
- [ ] Quality gates reales están verdes.
- [ ] No hay secretos, PII ni artefactos locales versionados.
- [ ] Se actualizaron documentos/ADRs afectados.
- [ ] El reviewer independiente emitió veredicto.
- [ ] El humano hizo el merge.
- [ ] Si hubo mutación remota, se verificó resultado y rollback.
- [ ] orch, Git y `STATE.md` reflejan la realidad.

El merge no equivale automáticamente a deploy. Un ticket de código puede estar `done` con release posterior explícito si el SPEC lo define así.

## 10. Matriz de permisos del agente

| Acción | Sin gate | GATE 1 | GATE 2 | GATE 3/humano |
| --- | --- | --- | --- | --- |
| Leer repo y estado | Sí | — | — | — |
| Redactar propuesta/SPEC | Sí | — | — | — |
| Editar código del ticket | No | Sí | — | — |
| Ejecutar tests locales | No, salvo diagnóstico read-only acordado | Sí | — | — |
| Crear branch/commit/push | Según ticket y permisos | Sí | Push según gobernanza | Merge no |
| Escribir en Supabase/n8n/VPS remoto | No | No | Sí, alcance exacto | — |
| Abrir PR | Tras evidencia/revisión según protocolo | Sí | — | — |
| Hacer merge/release | No | No | No | Humano |

## 11. Selección de Gemini

- Razonamiento, SPEC, arquitectura e implementación compleja: capacidad Pro disponible.
- Pruebas mecánicas y sincronización: capacidad rápida/económica disponible.
- Revisión: sesión limpia y, cuando sea posible, configuración/modelo diferente al implementador.

El nombre del modelo no es evidencia de calidad. El reviewer debe leer fuentes, diff y resultados desde cero.

## 12. Bloqueos y excepciones

Formato obligatorio:

```text
BLOCKED_BY: <condición concreta>
EVIDENCE: <archivo/comando/error sin secretos>
IMPACT: <qué no puede continuar>
NEEDED_FROM_HUMAN: <una decisión o acceso concreto>
SAFE_WORK_REMAINING: <si existe>
```

No usar `__PENDIENTE__` dentro de código de producción para ocultar una decisión ausente. Una excepción temporal debe tener owner, expiración, riesgo y ticket de remediación.

## 13. Trabajo paralelo

Solo se paraleliza cuando los outputs no compiten por los mismos archivos/decisiones. El coordinador define ownership y sintetiza antes del merge. Dos agentes no editan simultáneamente el mismo SPEC, migración o contrato de API.

## 14. Arranque de Gemini

Toda sesión comienza declarando:

```text
Ticket:
Rol:
Estado orch:
SPEC + versión:
Gates observados:
Archivos permitidos:
Mutaciones remotas previstas:
Comandos de verificación:
```

Si no puede completar el bloque con evidencia, la sesión queda en modo investigación/propuesta.
