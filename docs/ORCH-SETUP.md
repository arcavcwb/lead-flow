# Integración de orch — Lead Flow v2.0

> Estado: **INTEGRACIÓN MANUAL APLICADA; VALIDACIÓN ESTÁTICA APROBADA; COMMIT PENDIENTE**
> Decisión: orch será el registro operativo local porque el Product Owner trabaja solo.
> Versión instalada: `v0.16.0` en `/home/arcav/.local/bin/orch`.
> Este documento no autoriza `orch init`, `atomize --apply`, `orch run` ni ejecución de tareas.
> La asociación obligatoria tarea/agente/skills está en `docs/ORCH-AGENT-SKILL-MATRIX.md`.

Notas relevantes de `v0.16.0`: los worktrees pueden transportar ramas de dependencias no mergeadas y `dispatch.worktree_setup` puede ejecutar un comando de instalación por worktree. Esa instalación deberá declararse y verificarse explícitamente; no se habilita por inferencia en Lead Flow.

## 1. Responsabilidades

- Los documentos aprobados definen producto, arquitectura y restricciones.
- Cada SPEC aprobado define el contrato de un ticket.
- `tasks.json` representa el DAG, dependencias y estado operativo.
- `.orchestrator/state/` conserva eventos y ejecución local; no se versiona.
- Git, CI y PR demuestran el resultado técnico.
- El Product Owner concede GATE 0–3; orch no puede concederlos.

## 2. Integración mínima prevista

```text
tasks.json
.orchestrator/config.yaml
.orchestrator/model_router.yaml
.orchestrator/budgets.yaml
scripts/task-start.sh
scripts/task-finish.sh
scripts/task-block.sh
scripts/task-reset.sh
```

La integración se escribirá manualmente y en un diff revisable. No se ejecutará el inicializador genérico sobre el repositorio.

El puente de workspace para ambos agentes está en `AGENTS.md` y `GEMINI.md`. La regla P0 compartida está en `.agents/rules/lead-flow-governance.md`; esos archivos no sustituyen los gates, pero evitan que Codex y Gemini trabajen con contratos distintos.

## 3. Política de ejecución

- `worktree_mode`: habilitado.
- Rama base: `main`.
- `auto_merge`: `false`.
- Concurrencia inicial global: `1`.
- Una tarea solo puede estar lista si su SPEC está aprobado y sus dependencias terminaron.
- `orch run` queda prohibido hasta demostrar que una tarea sin gate no puede despacharse.
- Merge, deploy y escrituras remotas permanecen humanos o requieren su gate explícito.

### Handoff de agentes

```text
Product Owner aprueba
        ↓
Codex define/revisa el contrato
        ↓
orch registra y entrega la tarea
        ↓
Gemini/Antigravity ejecuta en su alcance
        ↓
Codex revisa diff y evidencia
        ↓
Product Owner concede el siguiente gate
```

El panel visual del IDE puede ocultar una extensión cuando se abre la otra; la coordinación no depende de mantener ambos paneles visibles. El repositorio y el contrato de tarea son la fuente de handoff.

## 4. Estados canónicos

| Estado lógico | Significado |
| --- | --- |
| `todo` | Brief existente; SPEC ausente o no aprobado |
| `ready` | SPEC aprobado, dependencias completas y archivos permitidos definidos |
| `in-progress` | Agente trabajando en worktree dedicado |
| `blocked` | Condición de parada registrada con evidencia y siguiente decisión humana |
| `review` | Implementación terminada; espera verificación/revisión |
| `done` | Evidencia aprobada y merge humano completado |

Si la versión instalada no soporta uno de estos nombres, la integración debe mapearlo explícitamente sin perder el significado. Nunca se usa `done` antes del merge y la evidencia.

## 5. Gates humanos

Los gates deben quedar versionados y vinculados al SHA aplicable:

- `GATE 0`: aprueba baseline documental y plan.
- `GATE 1`: aprueba un SPEC concreto.
- `GATE 2`: autoriza una mutación externa exacta.
- `GATE 3`: aprueba merge o release.

Un cambio material invalida la aprobación anterior. Una variable, comentario libre o estado de orch no sustituye el registro del gate.

## 6. Migración desde Plane

Plane queda como historial de solo lectura durante la transición. No habrá sincronización bidireccional.

1. Exportar o consultar Plane solo si el Product Owner necesita preservar información histórica.
2. Crear `tasks.json` desde el plan maestro y el estado comprobado en Git, no desde estados obsoletos.
3. Mantener los IDs `LEADFLOW-01` a `LEADFLOW-12`.
4. Validar dependencias y ciclos.
5. Comparar cada tarea con su SPEC y gate.
6. Declarar orch como operativo únicamente cuando la validación pase.
7. Archivar Plane; no continuar actualizando ambos sistemas.

## 7. Secuencia de integración autorizable

Después de GATE 0, Gemini debe presentar primero el diff propuesto. Tras aprobación del diff:

1. crear los archivos mínimos;
2. validar la matriz tarea/agente/skills;
3. ejecutar `orch atomize --list` sobre un preview aislado;
4. ejecutar `orch validate`;
5. ejecutar `orch router validate`;
6. revisar `orch explain` y `orch tasks`;
7. verificar que `.orchestrator/state/` esté ignorado;
8. probar los bloqueos sin despachar producto;
9. adjuntar evidencia y solicitar revisión.

No se ejecutan `orch doctor`, `orch run`, benchmarks, upgrades, dashboard remoto o instalación de skills sin necesidad y autorización separada.

## 8. Condiciones de parada

- El esquema de `tasks.json` obliga a perder un gate o una dependencia.
- Una tarea queda ejecutable sin SPEC aprobado.
- La configuración habilita auto-merge o concurrencia mayor a uno.
- Se requiere sobrescribir archivos existentes mediante `--force`.
- Aparece una credencial en configuración, eventos o logs.
- El estado de orch contradice Git/CI.

## 9. Criterios para declarar la migración terminada

- `orch validate` y `orch router validate` pasan.
- Los 12 tickets y sus dependencias coinciden con el plan maestro.
- Ninguna tarea de producto fue ejecutada durante la integración.
- Los gates no pueden inferirse ni saltarse automáticamente.
- `auto_merge` está desactivado.
- Estado runtime y secretos están fuera de Git.
- `orch explain`, `orch tasks` y el dashboard local reflejan el mismo DAG.
- Plane queda marcado como histórico y deja de ser autoridad.

## 10. Validación de integración realizada

```text
Comando: orch atomize --list --file docs/SPEC-LEADFLOW-01.md
Versión: orch v0.16.0
Resultado inicial: BLOCKED — faltaban tasks.json y scripts/task-start.sh
Resultado final: PASS — `orch validate --json` y `orch router validate --json`
Estado: 12 tareas `todo`, 0 ejecuciones, coste registrado `$0`
Escrituras de producto/remotas: ninguna
```

La integración final se escribió manualmente a partir del esquema comprobado en
un scaffold aislado de `orch v0.16.0`; no se ejecutó `orch init` en Lead Flow.
La matriz de routing y los gates se conservaron. El warning de `atomize --list`
sobre `docs/SPEC-LEADFLOW-01.md` queda documentado: el SPEC está fuera de la
raíz `specs/` y ese comando no se usa para aplicar tareas.
