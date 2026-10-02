# Configuración de Plane — SUPERADA

> Estado: **SUPERADO EL 2026-10-02 POR DECISIÓN DEL PRODUCT OWNER**

Lead Flow ya no usa Plane como fuente de estado ni como sistema de ejecución. El Product Owner trabaja solo y eligió orch para mantener el DAG, el estado operativo y la trazabilidad local junto al repositorio.

Este archivo se conserva únicamente para que enlaces o sesiones anteriores encuentren una instrucción inequívoca. No debe utilizarse para crear, actualizar, sincronizar o consultar tickets de Plane.

La configuración vigente está en [`ORCH-SETUP.md`](ORCH-SETUP.md). La autoridad por tipo de información está definida en [`SOURCE_OF_TRUTH.md`](SOURCE_OF_TRUTH.md).

Reglas de transición:

- Plane es histórico y deja de recibir actualizaciones.
- No se mantiene sincronización bidireccional.
- Cualquier preservación o exportación histórica se realiza solo si el Product Owner la solicita explícitamente.
- Los IDs `LEADFLOW-01` a `LEADFLOW-12` se conservan en `tasks.json` cuando se apruebe la integración de orch.
