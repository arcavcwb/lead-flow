# Supabase Free Tier — readiness de Lead Flow

> Estado: **BORRADOR PARA GATE 0; NO AUTORIZA ACCESO NI CAMBIOS REMOTOS**  
> Decisión propuesta: usar Supabase Free como un único proyecto remoto de MVP/piloto, con desarrollo local reproducible.  
> Fecha de verificación de límites: 2026-10-02. Volver a verificar antes de activar el piloto.

## 1. Propósito y límite de esta decisión

Supabase Free reduce operación para una persona y es adecuado para validar el MVP de Lead Flow. No equivale a una garantía de disponibilidad, capacidad ni recuperación para producción con SLA.

El plan no presupone que el proyecto remoto ya exista ni que esté configurado correctamente. Hasta el inventario read-only, su estado es **no verificado**.

## 2. Topología de entornos

| Entorno | Tipo | Datos permitidos | Uso |
| --- | --- | --- | --- |
| Local | Supabase CLI/Docker | Solo sintéticos | Migraciones, Edge Functions y pruebas repetibles |
| Remoto Free | Un proyecto de MVP/piloto | Sintéticos; reales mínimos solo tras GATE 2 | Demo, integración y piloto aprobado |
| Segundo proyecto Free | No asumido | Ninguno | Solo se evalúa si el inventario confirma cuota disponible y existe una necesidad real de staging separado |

No se crea un proyecto remoto adicional para “probar rápido”. El desarrollo y la validación de migraciones ocurren primero en local.

## 3. Límites operativos que condicionan el MVP

Según la documentación oficial vigente al redactar este documento, una cuenta puede tener hasta dos proyectos Free activos considerando las organizaciones donde actúa como Owner o Admin, con 500 MB de base de datos por proyecto, 5 GB de egress por organización y 500.000 invocaciones mensuales de Edge Functions. Al superar el límite de tamaño de base de datos, un proyecto Free puede quedar en modo read-only.

Para Lead Flow eso implica:

- no se guarda media, adjuntos, grabaciones ni payloads completos;
- no se usa Storage, Realtime, Vector ni Auth para el MVP salvo que un SPEC aprobado demuestre su necesidad;
- el formulario captura el mínimo de PII y limita tamaño de payload;
- intentos de entrega y logs se retienen de forma limitada y sanitizada;
- la retención/borrado es una condición de entrada al piloto, no una mejora posterior;
- un error de cuota se considera incidente de captura: el cliente no recibe una promesa de SLA.

Los límites exactos se confirman en el dashboard y documentación oficial antes de GATE 2; no se copian a código como constantes de negocio.

## 4. Inventario remoto de solo lectura

Después de GATE 0 y antes de cualquier `supabase link`, Gemini o el operador puede presentar un inventario sin secretos. No modifica schema, secretos, funciones, Auth, Storage ni billing.

El inventario debe registrar solo:

```text
Organización: <nombre no sensible>
Project ref: <parcial/redactado>
Plan observado: Free | otro
Estado: activo | pausado | desconocido
Región: <región>
Uso observado: base de datos, egress, Edge Functions
Servicios habilitados: Database, Functions, Auth, Storage, Realtime
Data API: schemas expuestos y política de nuevas tablas
Historial de migraciones: vacío | existente | desconocido
Propietario humano y fecha de revisión:
```

Si existe schema, funciones, buckets, usuarios o datos previos, el resultado es `BLOCKED_BY_EXISTING_REMOTE_STATE` hasta que el Product Owner decida preservarlos, aislarlos o crear otro proyecto. No se limpia ni reinicia un proyecto existente.

## 5. Presupuesto de datos y retención

Antes de ingresar datos reales, LEADFLOW-11 debe aprobar valores concretos para:

| Dato | Máximo inicial | Retención | Acción al vencer |
| --- | --- | --- | --- |
| Lead normalizado | Solo campos del formulario aprobado | Pendiente de decisión humana | Eliminar o anonimizar según política aprobada |
| Payload bruto | No persistir por defecto | N/A | Rechazar o normalizar antes de guardar |
| Metadatos/IP | Mínimos y sanitizados | Pendiente de decisión humana | Borrar o agregar |
| Intentos de entrega | Códigos y errores sanitizados | Pendiente de decisión humana | Purgar según política |
| Logs de aplicación | Sin PII completa ni secretos | Según plataforma + política | Revisar y minimizar |

La decisión de retención debe incluir una estimación simple de crecimiento mensual y un umbral operativo anterior a 500 MB. Si no existe medición o rutina de limpieza probada, no se inicia el piloto con datos reales.

## 6. Seguridad mínima del proyecto remoto

- Las tablas internas no se exponen directamente a `anon` ni `authenticated`.
- Data API no recibe grants sobre leads, outbox, intentos o configuraciones internas.
- Toda tabla de schema expuesto mantiene RLS como defensa en profundidad.
- El SDK solo llama Edge Functions; nunca usa `service_role` ni secretos.
- Secrets de funciones viven en el almacén remoto de Supabase; no en `VITE_*`, Git, orch, logs ni documentación.
- Auth, Storage, Realtime y Vector permanecen fuera de alcance hasta un SPEC aprobado.
- No se usan funciones `SECURITY DEFINER` en schema expuesto como atajo de permisos.

## 7. Cambios remotos y rollback

Un proyecto Free no elimina la gobernanza:

1. schema y funciones se prueban localmente;
2. se adjunta diff, pruebas, migración, objetos afectados y rollback;
3. el humano concede GATE 2 para el project ref y operación exactos;
4. se confirma target inmediatamente antes de ejecutar;
5. se aplica solo la migración/deploy aprobados;
6. se ejecutan smoke tests positivos y negativos;
7. se registran resultados redacted en Git/orch.

Quedan prohibidos `db reset --linked`, SQL manual para “probar”, seeds reales y cambios de billing durante el piloto sin autorización separada.

## 8. Criterios para considerar listo el Free Tier

- inventario remoto read-only registrado y sin estado previo no decidido;
- plan Free y cuota disponible confirmados por el propietario;
- un solo proyecto remoto definido para el MVP o una razón aprobada para un segundo;
- desarrollo local reproducible y CI real antes de vincular;
- migraciones seguras probadas localmente;
- Data API, grants y RLS revisados;
- monitor de tamaño/uso y umbral de aviso definidos;
- retención, borrado y respuesta a cuota probados antes de datos reales;
- GATE 2 emitido para toda primera escritura remota.

## 9. Señales para salir del Free Tier

No se migra por intuición. Se reevalúa si ocurre cualquiera de estas condiciones:

- el piloto se aproxima al umbral de base de datos definido;
- el proyecto entra en read-only, se pausa o presenta restricciones de cuota;
- se requiere staging remoto permanente, backups/PITR, dominio personalizado o SLA;
- el soporte manual de retención, observabilidad o recuperación deja de ser sostenible;
- existen más de tres clientes activos o un compromiso comercial incompatible con restricciones de Free.

La decisión económica propuesta es: **Free durante construcción y validación técnica; Pro cuando exista validación comercial o un piloto que justifique el gasto**. El precio de referencia actual del plan Pro es 25 USD/mes antes de impuestos y cargos variables; debe confirmarse en billing justo antes del cambio.

## 10. Fuentes oficiales a revalidar

- [Billing y cuotas de Free](https://supabase.com/docs/guides/platform/billing-on-supabase)
- [FAQ de billing y restricciones](https://supabase.com/docs/guides/platform/billing-faq)
- [Límite de tamaño de base de datos](https://supabase.com/docs/guides/platform/database-size)
- [Límites de Edge Functions](https://supabase.com/docs/guides/functions/limits)
- [Seguridad de Data API](https://supabase.com/docs/guides/api/securing-your-api)
