# DOC 6: Revisión Arquitectónica y Decisiones Técnicas (v1.0)

Este documento registra los **riesgos técnicos identificados**, las **decisiones arquitectónicas tomadas** y su justificación. Sirve como fuente de verdad para debates con líderes técnicos, code reviews y evaluación de alternativas futuras.

---

## Riesgo 1 — Peso del SDK (> 50kb)

| Atributo | Detalle |
| :--- | :--- |
| **Riesgo** | Usar React + ReactDOM supera fácilmente los 50kb gzippeados, comprometiendo el KPI de < 200ms TTI en redes 4G. |
| **Decisión** | **SolidJS** como runtime del SDK inyectable. |
| **Justificación** | SolidJS compila los componentes a DOM mutations directas (sin Virtual DOM). El runtime base es < 10kb. No existe penalty de reconciliación en runtime. Esto garantiza holgadamente el límite de peso y la velocidad de carga. |
| **Alternativa descartada** | Preact (~3kb) fue evaluado, pero SolidJS ofrece mejor DX y performance de renders sin sacrificar tamaño. |

---

## Riesgo 2 — Aislamiento CSS Real del Widget

| Atributo | Detalle |
| :--- | :--- |
| **Riesgo** | CSS Modules solos no protegen contra estilos globales agresivos con `!important` o resets universales (`* { box-sizing: border-box; }`). El widget puede romperse visualmente en la web de cualquier cliente. |
| **Decisión** | **Shadow DOM** nativo del navegador para encapsular el widget. |
| **Justificación** | El Shadow DOM crea una barrera nativa de estilo que ninguna hoja de estilos externa puede atravesar. Es la única solución que garantiza que el diseño White-Label sea **100% idéntico e inmutable** en todas las instalaciones de clientes, independientemente de su stack (WordPress, Shopify, Elementor). |
| **Implementación** | SolidJS + `solid-element` (Web Components) para registrar el Custom Element con su Shadow Root. |

---

## Riesgo 3 — Resiliencia ante Inestabilidad de WhatsApp

| Atributo | Detalle |
| :--- | :--- |
| **Riesgo** | WAHA (WhatsApp HTTP API) o la API de WhatsApp pueden sufrir interrupciones, rate limits o baneos temporales, resultando en la pérdida del mensaje al vendedor (aunque el lead esté guardado). |
| **Decisión** | **Dead Letter Queue (DLQ)** implementada en el flujo de n8n. |
| **Justificación** | Si el envío falla, el Catch Node captura el error y programa reintentos automáticos (2min → 5min → 15min). Esto garantiza la entrega eventual sin intervención manual y sin que el usuario final perciba el error. El lead en `leads_vault` y el respaldo en Google Sheets actúan como safety nets independientes. |

---

## Riesgo 4 — Bypass de Seguridad por CORS Falsificado (Spam)

| Atributo | Detalle |
| :--- | :--- |
| **Riesgo** | El header `Origin` HTTP puede ser falsificado en requests server-side (cURL, Postman, bots), saltándose la validación de CORS y llenando `leads_vault` con spam. |
| **Decisión** | **Rate Limiting por IP** en la Edge Function + **campo Honeypot** en el SDK. |
| **Justificación** | - **Rate Limiting:** Si una IP envía más de X requests en 60s, se bloquea con `HTTP 429`. Defiende contra flood attacks. - **Honeypot:** Campo invisible para humanos, visible para bots. Si viene completado, el request se descarta silenciosamente. Doble capa de defensa sin afectar la UX del usuario real. |

---

## Decisión 5 — Capa de Persistencia como Safety Net Primario

| Atributo | Detalle |
| :--- | :--- |
| **Principio** | "El lead nunca se pierde." |
| **Decisión** | La Edge Function escribe en `leads_vault` **antes** de llamar al webhook de n8n. La operación de WhatsApp es siempre **asíncrona y opcional** para la respuesta al usuario. |
| **Justificación** | Si n8n o WAHA (WhatsApp HTTP API) caen, Supabase ya tiene el lead. El usuario recibe confirmación inmediata. El vendedor recibirá la notificación cuando el servicio se recupere. Esto desacopla la UX del usuario de la disponibilidad de terceros. |

---

## Registro de Alternativas Evaluadas y Descartadas

| Alternativa | Razón de Descarte |
| :--- | :--- |
| **React + ReactDOM** para el SDK | Tamaño base > 40kb solo de React, sin contar el código del widget. Riesgo alto de superar el límite de 50kb. |
| **iFrame** en lugar de Shadow DOM | Los iFrames tienen overhead de carga, problemas de comunicación cross-origin y no se adaptan fluidamente al flujo de la página host. |
| **Twilio / MessageBird** para WhatsApp | Costo por mensaje destruye el gross margin. A 50 clientes con volumen, el margen cae por debajo del 70%. |
| **Supabase Realtime para n8n trigger** | Introduce latencia adicional. El webhook directo desde la Edge Function es más determinístico para el SLA de < 5s. |
