# Modelo de negocio — Lead Flow v2.0

> Estado: **BORRADOR PARA GATE 0**
> Este documento contiene hipótesis comerciales. Ninguna cifra se presenta como resultado probado sin evidencia de piloto.

## 1. Qué se vende

Lead Flow no vende un formulario aislado. Vende una operación administrada de captura y entrega:

- Instalación en una web existente.
- Configuración del formulario sin código específico por cliente.
- Persistencia y trazabilidad del lead.
- Alerta al vendedor mediante un proveedor aprobado.
- Reintentos y monitoreo básico.
- Soporte de operación dentro de límites contractuales.

El valor económico esperado es reducir el tiempo de primera respuesta y evitar leads invisibles. Esa relación debe medirse; no se promete de antemano una reducción concreta del CPL ni un incremento de conversión.

## 2. Cliente inicial

Priorizar empresas que ya tengan:

- Tráfico o campañas activas.
- Volumen suficiente para observar el problema.
- WhatsApp dentro del proceso comercial.
- Un sitio donde instalar el widget.
- Una persona responsable de ventas y otra autorizada para privacidad/datos.
- Capacidad para participar en un piloto medido.

Evitar inicialmente organizaciones reguladas o con datos sensibles hasta tener revisión jurídica y controles acordes.

## 3. Oferta inicial

### Lead Flow Core

Para clientes con sitio propio.

- Widget en la web existente.
- Un formulario/configuración activa.
- Bóveda de leads.
- Una ruta de notificación.
- Métricas básicas de captura y entrega.
- Operación interna, sin acceso directo del cliente a n8n o Supabase.

### Lead Flow Pro

Para clientes que además necesitan una experiencia de campaña administrada.

- Todo Core.
- Landing page o integración avanzada.
- Reglas de routing por campaña/equipo.
- Integraciones adicionales aprobadas.
- Reporte operacional y soporte ampliado.

La alerta rápida forma parte del núcleo de ambos niveles. Un plan sin mensajería debe venderse como producto distinto, no como Lead Flow completo.

## 4. Precio: hipótesis a validar

No se fijan precios definitivos antes del piloto. La infraestructura comienza en Free para validar la idea. Si el proyecto necesita el plan Pro al entrar en validación/piloto, el presupuesto de referencia vigente es **25 USD/mes antes de impuestos y cargos variables**, sujeto a confirmación en billing. Cada prueba comercial debe registrar:

| Variable | Qué se mide |
| --- | --- |
| `setup_price` | Precio inicial presentado y aceptado/rechazado |
| `monthly_price` | MRR presentado y aceptado/rechazado |
| `setup_hours` | Horas humanas reales de onboarding |
| `support_hours` | Horas mensuales por cliente |
| `infra_cost` | Supabase, VPS, dominio, storage, monitoreo y backups |
| `provider_cost` | Mensajes, números, sesiones o licencias |
| `automation_license` | Costo/licencia aplicable de n8n u otra herramienta |
| `incident_cost` | Tiempo y compensaciones por fallos |

Fórmulas mínimas:

```text
gross_profit_per_client = monthly_price - variable_cost_per_client
contribution_margin = gross_profit_per_client / monthly_price
setup_margin = setup_price - (setup_hours × internal_hour_cost) - setup_external_costs
break_even_clients = monthly_fixed_cost / gross_profit_per_client
```

No se publicará “90% de margen” hasta completar estas variables con datos reales y separar margen bruto de costo humano de soporte.

## 5. Costos que el plan debe incluir

- Suscripción y compute de Supabase por proyecto/organización; el MVP parte de Free, sin asumir que seguirá siendo suficiente. El salto a Pro se decide al validar la idea, con presupuesto inicial de 25 USD/mes antes de impuestos/uso.
- Egress, almacenamiento, logs y retención.
- VPS, backups, firewall, monitoreo y tiempo de actualización.
- Recursos por sesión de mensajería.
- Proveedor oficial de WhatsApp, si aplica.
- Licencia de n8n según el uso comercial concreto.
- Dominio, certificados y observabilidad.
- Soporte e incidentes fuera de horario.
- Impuestos, comisiones de pago y adquisición de clientes.

Las cuotas de proveedores cambian; se consultan en fuentes oficiales al preparar cada SPEC o precio. No se copian cifras volátiles como promesa contractual.

## 6. Política de proveedores

### Mensajería: Evolution API

- Evolution API es el gateway seleccionado porque ya existe una instancia operativa.
- La integración seguirá detrás de `MessagingProvider`; no se acopla el dominio a endpoints concretos.
- Antes del piloto se debe confirmar si la instancia usa Baileys/WhatsApp Web o WhatsApp Cloud API oficial. El perfil de riesgo, costo y política cambia según esa respuesta.
- No se ofrece SLA hasta medir salud, versión, modo de conexión, límites y recuperación de la instancia.
- No se crean, reinician, desconectan ni reconfiguran instancias sin GATE 2.

### n8n

- Se utilizará la instancia n8n existente como capa de routing e integraciones.
- n8n no se expone ni se vende como interfaz al cliente en el MVP.
- Antes de alojar workflows o credenciales de terceros como parte del servicio, el Product Owner debe confirmar por escrito el encaje de licencia.
- Si el caso requiere Enterprise/Embed, su costo entra en la economía del producto.
- El outbox en Supabase conserva la obligación durable; un workflow n8n no es la única copia del evento.
- No se crea, activa, desactiva ni modifica un workflow existente sin inventario read-only y GATE 2.

## 7. Objetivos operativos, no promesas

| Objetivo | Validación requerida antes de venderlo como compromiso |
| --- | --- |
| Onboarding en 24 h | 3 instalaciones consecutivas dentro del objetivo |
| Notificación en menos de 5 s | `p95` de tráfico piloto bajo condiciones publicadas |
| Alta disponibilidad | Monitoreo, presupuesto de error e historial suficiente |
| Configuración sin código | 3 clientes configurados sin cambios específicos |
| Escala multi-tenant | Prueba de capacidad con perfil de carga realista |

## 8. Riesgos comerciales

| Riesgo | Mitigación de negocio |
| --- | --- |
| Desconexión/degradación de Evolution API | Outbox, healthcheck, adaptador, modo de conexión identificado y plan alternativo |
| Cuota o modo read-only de Supabase Free | Retención limitada, monitor de uso, umbral anterior a cuota y decisión de upgrade/pausa |
| Soporte consume el margen | Límites de servicio, runbooks y medición de horas |
| Cada cliente pide un formulario distinto | Esquema versionado y catálogo limitado de campos |
| El cliente exige dashboard | Operación administrada primero; dashboard solo con evidencia de demanda |
| Uso de n8n requiere licencia comercial | Revisión de licencia antes del piloto y costo incorporado |
| El lead rápido no cambia ventas | Medir tiempo de respuesta y conversión, no solo entrega técnica |

## 9. Criterio para escalar

No ampliar infraestructura ni automatizar onboarding masivo hasta que:

- Exista al menos un piloto pagado.
- La entrega y recuperación de fallos estén verificadas.
- El costo por cliente sea conocido.
- El tiempo de soporte sea sostenible.
- Evolution API tenga inventario, modo de conexión y política de producción aprobados.
- Privacidad, retención e incidentes estén operables.

## 10. Fuentes volátiles a revisar antes de cada decisión

- Supabase billing y cuotas: <https://supabase.com/docs/guides/platform/billing-on-supabase>
- Evolution API, proveedores y autenticación: <https://github.com/evolution-foundation/evolution-api>
- Licencia/caso comercial de n8n: <https://support.n8n.io/article/can-i-use-your-license-for-my-use-case>

Última verificación documental: 2026-10-02.
