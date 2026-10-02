# SPEC-LEADFLOW-05 — Esquema local, RLS y aislamiento multi-tenant

**Estado:** BORRADOR — requiere GATE 1
**Ticket:** LEADFLOW-05
**Responsable de ejecución:** Gemini, después de aprobación humana
**Tipo de cambio:** migraciones locales y pruebas de base de datos

## 1. Objetivo

Crear una base de datos mínima y reproducible para el MVP, con aislamiento por cliente, permisos explícitos y soporte para entrega durable. La implementación se valida localmente antes de solicitar cualquier mutación remota.

## 2. Baseline limpia

La migración local anterior fue retirada del workspace antes de esta SPEC. No se reutiliza ningún esquema legacy. LEADFLOW-05 debe diseñar y probar el esquema canónico desde cero, siempre en local y dentro de los archivos permitidos.

La ausencia de una migración inicial no autoriza a conectarse a un proyecto remoto ni a improvisar tablas, grants o políticas fuera de este contrato.

## 3. Precondiciones

- GATE 0 aprobado.
- Esta SPEC aprobada mediante GATE 1.
- LEADFLOW-02 y LEADFLOW-03 terminados.
- Entorno local de Supabase reproducible y aislado.
- `docs/SUPABASE-FREE-TIER-READINESS.md` revisado; el proyecto remoto Free sigue sin tocarse.
- Rama dedicada y árbol de trabajo inspeccionado.
- Baseline limpia confirmada: no existe migración legacy dentro del workspace.

## 4. Alcance

### Incluido

- migraciones versionadas para el esquema canónico;
- constraints, índices, grants/revokes y RLS;
- pruebas locales de aislamiento y permisos;
- semilla sintética mínima para pruebas;
- reset local reproducible desde cero.

### Excluido

- `db push`, migración o reset de un proyecto remoto;
- Edge Functions y endpoints públicos;
- SDK embebible;
- workflows de n8n o configuración de Evolution API;
- datos personales o credenciales reales;
- panel administrativo.

## 5. Modelo de datos canónico

La implementación debe respetar `docs/3_ARCHITECTURE.md`. El detalle físico puede ajustarse durante GATE 1, pero como mínimo incluye:

### `clients`

- identificador estable;
- nombre operativo;
- estado activo/inactivo;
- timestamps.

### `client_domains`

- referencia al cliente;
- origen normalizado y único;
- estado de verificación;
- timestamps.

### `form_configs`

- referencia al cliente;
- versión de configuración;
- estado publicado/no publicado;
- definición validable del formulario;
- timestamps;
- unicidad suficiente para resolver una única configuración publicada.

### `integration_configs`

- referencia al cliente;
- tipo de integración, inicialmente `n8n_evolution`;
- identificadores no secretos necesarios para enrutar;
- referencia a secretos almacenados fuera de tablas públicas;
- estado activo/inactivo;
- timestamps.

No se guardan API keys, tokens o credenciales en columnas consultables por clientes públicos.

### `leads`

- referencia al cliente y configuración;
- identificador de idempotencia;
- payload normalizado y limitado;
- metadatos mínimos de origen;
- estado de consentimiento cuando corresponda;
- timestamps;
- constraint única que impida duplicar una captura equivalente dentro del alcance definido.

### `delivery_outbox`

- referencia al lead y cliente;
- tipo de evento;
- estado `pending`, `processing`, `delivered`, `retryable` o `dead_letter`;
- número de intentos y próxima fecha de intento;
- lease/lock con expiración para procesamiento concurrente;
- último código y error sanitizado;
- timestamps;
- unicidad que impida crear dos obligaciones de entrega para el mismo evento lógico.

### `delivery_attempts`

- referencia al outbox;
- número de intento;
- timestamps de inicio y fin;
- resultado y latencia;
- código externo sanitizado;
- error sanitizado;
- identificador externo no secreto cuando exista.

## 6. Permisos y RLS

### Principio

Toda tabla expuesta por la API de datos debe tener RLS activa y políticas explícitas. RLS no reemplaza los grants: ambos se configuran y prueban.

### Roles públicos

`anon` y usuarios no administrativos:

- no pueden leer directamente leads, outbox, intentos o configuraciones internas;
- no pueden insertar directamente en tablas internas;
- no pueden actualizar ni eliminar registros operativos;
- no reciben acceso por una política abierta como `WITH CHECK (true)`.

### Acceso servidor

Las operaciones privilegiadas se realizan únicamente desde código servidor autorizado. La futura API de captura debe usar una transacción o función controlada que cree el lead y su evento de outbox de forma atómica; esa función pertenece a LEADFLOW-06 y no debe exponerse anticipadamente en esta SPEC.

### Aislamiento

- toda fila operativa queda vinculada a un cliente;
- no existe lectura o escritura cruzada entre clientes;
- claves foráneas y constraints evitan referencias entre tenants incompatibles;
- las pruebas usan al menos dos clientes sintéticos.

## 7. Índices mínimos

Los índices se justifican con consultas previstas, al menos:

- resolución de dominio activo;
- configuración publicada por cliente;
- idempotencia de captura;
- selección de outbox por estado y `next_attempt_at`;
- expiración/recuperación de leases;
- historial de intentos por evento.

No se añaden índices especulativos sin consulta o constraint asociada.

## 8. Flujo de migración local desde cero

1. inspeccionar el estado del árbol sin exponer secretos;
2. confirmar que no existe una migración legacy dentro del workspace;
3. diseñar una migración nueva y revisable desde el modelo aprobado;
4. reiniciar la base local desde cero;
5. aplicar únicamente las migraciones nuevas y la semilla sintética;
6. ejecutar pruebas de esquema, permisos y aislamiento;
7. repetir el reset desde un checkout limpio;
8. adjuntar evidencia al ticket y solicitar revisión.

Ningún paso de esta SPEC incluye vincular, empujar o reiniciar una base remota.

## 9. Escenarios de aceptación

```gherkin
Escenario: el esquema nace desde cero
  Dado un entorno local vacío
  Cuando se ejecuta el flujo documentado de reset
  Entonces todas las migraciones se aplican sin intervención manual
  Y existen las tablas, constraints e índices aprobados

Escenario: acceso anónimo bloqueado
  Dado el rol anon
  Cuando intenta leer o insertar directamente en leads o delivery_outbox
  Entonces la operación es rechazada

Escenario: aislamiento entre clientes
  Dado un registro del cliente A y otro del cliente B
  Cuando una operación autorizada en el alcance de A intenta acceder al registro de B
  Entonces no obtiene ni modifica el registro de B

Escenario: idempotencia persistente
  Dado un lead guardado con una clave de idempotencia
  Cuando se intenta guardar otro lead equivalente en el mismo alcance
  Entonces una constraint evita la duplicación

Escenario: obligación de entrega única
  Dado un evento lógico asociado a un lead
  Cuando se intenta crear dos filas de outbox para ese evento
  Entonces una constraint conserva una sola obligación de entrega

Escenario: consulta del dispatcher soportada
  Dado un conjunto de eventos con distintos estados y fechas
  Cuando el dispatcher consulta eventos disponibles
  Entonces el plan de consulta puede usar los índices aprobados
  Y no selecciona eventos con lease vigente
```

## 10. Evidencia obligatoria

- diff completo de migraciones;
- resultado de reset local desde cero;
- pruebas positivas y negativas de grants/RLS;
- prueba con dos tenants;
- comprobación de constraints de idempotencia y outbox;
- explicación de índices basada en consultas;
- versiones de CLI y servicios locales;
- SHA exacto probado;
- confirmación explícita de que no se ejecutó una mutación remota.

## 11. Condiciones de parada

Gemini debe detenerse y marcar `BLOCKED` si:

- no existe decisión humana sobre la migración actual;
- una instrucción requiere datos o secretos reales;
- la CLI apunta a un proyecto remoto o propone `db push`, `db reset --linked` o equivalente;
- el modelo físico contradice la arquitectura aprobada;
- no puede demostrar aislamiento con dos clientes;
- un cambio requiere ampliar el MVP o añadir una integración no aprobada.

## 12. Definición de terminado

- reset local reproducible desde cero;
- grants y RLS probados, no solo declarados;
- aislamiento multi-tenant demostrado;
- idempotencia y outbox protegidos por constraints;
- no hay secretos ni datos reales en migraciones o semillas;
- no hubo mutaciones remotas;
- el esquema y sus pruebas no dependen de cuota, plan o credenciales del remoto Free;
- GATE 3 concedido antes del merge.
