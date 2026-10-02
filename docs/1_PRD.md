# PRD — Lead Flow v2.0

> Estado: **BORRADOR PARA GATE 0**
> Product Owner: humano
> Fecha base: 2026-10-02
> Las cifras de rendimiento son objetivos de piloto, no SLA comercial.

## 1. Problema

Empresas que compran tráfico digital pierden oportunidades porque sus formularios cargan mal, los leads quedan dispersos o el equipo comercial recibe el aviso demasiado tarde. El comprador no necesita “otro formulario”: necesita evidencia de que cada prospecto fue guardado y encaminado rápidamente a una persona capaz de responder.

## 2. Hipótesis de producto

Si una empresa puede instalar un widget ligero en su sitio y recibir una alerta trazable pocos segundos después de cada envío, entonces reducirá el tiempo de primera respuesta y estará dispuesta a pagar por la captura, operación y confiabilidad del flujo.

Esta hipótesis todavía debe validarse con 1–3 pilotos. No se declara product-market fit, margen probado ni capacidad para 50 clientes.

## 3. Usuario inicial

### Comprador inicial

Empresa pequeña o mediana que:

- Genera leads mediante campañas digitales.
- Usa WhatsApp como canal cotidiano de ventas.
- Tiene una web existente, frecuentemente WordPress o HTML administrado.
- No dispone de integración confiable entre formulario y vendedor.
- Puede designar a una persona responsable del piloto y del tratamiento de datos.

### Usuario operativo

Vendedor o coordinador comercial que necesita recibir datos suficientes para contactar al prospecto, distinguir el origen del lead y saber si hubo un fallo de entrega.

### Prospecto

Persona que completa el formulario, principalmente desde móvil, y debe recibir una experiencia rápida, accesible y transparente sobre el uso de sus datos.

## 4. Job to be done

> Cuando una campaña genera interés, quiero que cada solicitud válida quede guardada y llegue al vendedor correcto rápidamente, para responder antes de que el prospecto pierda intención y sin depender de revisar manualmente varias bandejas.

## 5. Propuesta de valor

**Lead Flow convierte una web existente en un canal de captura medible:** instala un widget configurable, persiste primero cada lead y entrega alertas mediante un proveedor reemplazable, con reintentos y evidencia operacional.

## 6. Resultado del MVP

El MVP debe demostrar un flujo vertical para un tenant piloto:

```text
configuración pública segura
        ↓
widget accesible
        ↓
API de captura
        ↓
lead + evento durable en una transacción
        ↓
adaptador de mensajería
        ↓
alerta al vendedor + trazabilidad + reintento
```

## 7. Alcance MVP

### Incluido

- SDK instalable como Web Component con Shadow DOM y Preact como implementación interna reemplazable.
- Formulario definido mediante un esquema versionado por cliente.
- Endpoint público que devuelve únicamente configuración presentacional permitida.
- Endpoint de captura con validación, consentimiento, idempotencia, honeypot y rate limiting durable.
- Persistencia multi-tenant en PostgreSQL.
- Outbox durable y reintentos para la entrega.
- Adaptador de proveedor de mensajería con Evolution API como implementación inicial.
- Integración con la instancia n8n existente como capa de routing, después de inventario read-only y validación de licencia para el modelo operativo.
- Métricas y correlation ID desde recepción hasta aceptación del proveedor.
- Operación interna para 1–3 pilotos.
- Aviso de privacidad, retención y procedimiento de eliminación/exportación.

### Fuera de alcance

- Dashboard de autoservicio para clientes.
- Editor visual drag-and-drop.
- Chatbot conversacional.
- CRM completo.
- Atribución avanzada o scoring con IA.
- Mensajería masiva o campañas outbound.
- SLA contractual de 99.9%.
- Escala declarada para 50 clientes antes de medir pilotos.
- Landing pages personalizadas como requisito del MVP técnico.

## 8. Requisitos funcionales

| ID | Requisito | Resultado observable |
| --- | --- | --- |
| `FR-01` | Identificar tenant y dominio | Un cliente inactivo o un origen no permitido no obtiene configuración operativa ni crea leads |
| `FR-02` | Cargar configuración pública | El widget recibe solo campos, tema, textos y versión permitidos; nunca webhooks ni secretos |
| `FR-03` | Capturar lead | Una solicitud válida recibe `lead_id` y `correlation_id`; una inválida no escribe datos |
| `FR-04` | Persistir de forma durable | Lead y evento de entrega se crean atómicamente antes de responder éxito |
| `FR-05` | Evitar duplicados | Repetir una solicitud con la misma idempotency key no crea otro lead ni otra alerta |
| `FR-06` | Entregar y reintentar | El evento pasa por estados auditables y reintenta con backoff sin duplicar envíos |
| `FR-07` | Aislar tenants | Ningún rol público o tenant puede consultar datos de otro cliente |
| `FR-08` | Registrar consentimiento | El lead conserva versión del texto, instante, URL de origen y finalidad informada |
| `FR-09` | Observar el recorrido | Los tiempos de recepción, persistencia, despacho y aceptación del proveedor se pueden correlacionar |
| `FR-10` | Operar derechos de datos | Un operador autorizado puede localizar, exportar o eliminar/anomizar según la política aprobada |

## 9. Objetivos no funcionales del piloto

| Dimensión | Objetivo | Cómo se mide |
| --- | --- | --- |
| Bundle | `< 50 KiB` comprimido para el SDK funcional | Artefacto de producción, gzip y Brotli reportados por CI |
| Captura | `p95 ≤ 800 ms` entre recepción y respuesta, excluyendo red del usuario | Timestamps del backend en staging/piloto |
| Notificación | `p95 ≤ 5 s` entre `submission_received` y `provider_accepted` | Eventos correlacionados; no se usa “vibración del teléfono” |
| Persistencia | 100% de solicitudes válidas aceptadas dejan lead + outbox | Prueba de 20 envíos y consulta de evidencia |
| Resiliencia | Una caída del proveedor no pierde ni duplica leads | Prueba controlada de fallo y recuperación |
| Accesibilidad móvil | Inputs ≥16 px, targets ≥44×44 px, labels y errores accesibles | Pruebas automáticas + dispositivo real |
| Seguridad | Cero acceso anónimo directo a tablas internas | Tests negativos de grants y RLS |
| Privacidad | Cero PII o secretos en logs de aplicación | Inspección automatizada y manual de logs de prueba |

Los objetivos se convierten en SLA solo después de un piloto estable, capacidad medida, monitoreo activo y aprobación comercial explícita.

## 10. Reglas de datos

- Minimizar campos: recolectar solo lo necesario para la finalidad declarada.
- El teléfono se normaliza en backend; el valor original no se usa como clave de idempotencia pública.
- Los metadatos permitidos se enumeran; el cliente no puede enviar JSON arbitrario ilimitado.
- Toda fila operativa contiene `client_id` y timestamps UTC.
- Los secretos de integración no se guardan en configuración pública.
- Google Sheets, si se habilita, es un espejo operativo; no es backup ni fuente de verdad.
- La política de retención debe definirse antes del primer piloto con datos reales.

## 11. Hipótesis que deben medirse

| Hipótesis | Evidencia mínima |
| --- | --- |
| El comprador valora velocidad sobre un formulario genérico | 5 entrevistas y al menos 1 piloto aceptado |
| La instalación puede completarse en un día | Tiempo registrado en 3 instalaciones reales |
| `p95 ≤ 5 s` es sostenible | Métricas de 100 eventos de prueba y tráfico piloto |
| El modelo puede operar con margen atractivo | Costos reales por tenant, horas de soporte y precio aceptado |
| Un esquema común cubre clientes distintos | 3 configuraciones sin cambios de código específico |

## 12. Criterios de éxito

### MVP técnico

- Cumple todos los requisitos `FR-01` a `FR-10` aplicables al piloto.
- Supera el protocolo de `docs/5_QA_PROTOCOL.md`.
- No depende de una escritura directa del navegador en Supabase.
- Puede reemplazar Evolution API o su modo de conexión sin cambiar el contrato de captura.

### Piloto de producto

- 1–3 clientes instalan el flujo con consentimiento informado.
- Se registran latencia, éxito de entrega, incidentes y horas de soporte.
- Al menos un cliente acepta un precio concreto o paga.
- Se toma una decisión explícita: `continuar`, `iterar` o `detener`.

## 13. Gates del producto

- `GATE 0`: humano aprueba este PRD, la arquitectura y el plan maestro.
- `GATE 1`: humano aprueba cada SPEC antes de implementación.
- `GATE 2`: humano autoriza cualquier migración, deploy, envío real o escritura remota.
- `GATE 3`: humano aprueba merge y liberación del piloto.
