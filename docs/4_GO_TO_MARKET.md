# DOC 4: Go-To-Market y Estrategia Comercial (v1.0)

## 1. El Posicionamiento (Framing Comercial)

No vendemos "Landing Pages" ni "Formularios". Vendemos **leads rescatados y velocidad de contacto**.

El mensaje de ventas se construye sobre el dolor real del Director Comercial: campañas de marketing que generan tráfico pero pierden prospectos por tiempos de respuesta lentos o formularios que no convierten.

---

## 2. Táctica de Outbound (Prospección B2B)

### Mensaje de Apertura para Directores Comerciales / CEOs:

> *"Noté que sus campañas dirigen tráfico a un sitio que tarda 4.2s en cargar en móvil (pierden 40% del tráfico antes de ver la oferta). Además, probé llenar su formulario y nadie me contactó en la primera hora.*
>
> *Implementamos infraestructuras para [Sector] que capturan en 0.5s y alertan a ventas en 5 segundos. ¿Tienen 15 minutos el martes?"*

### Por qué funciona:
- **Dato concreto** de velocidad (que el equipo puede medir con Lighthouse)
- **Prueba social implícita** (mostramos que probamos su producto antes de contactar)
- **Propuesta de valor cuantificada** (5 segundos, no "rápido")
- **CTA de baja fricción** (15 min, no una demo de 1 hora)

---

## 3. El Demostrador en Vivo — "El Simulador de Velocidad"

La herramienta de cierre de ventas definitiva: una landing page propia con el "Simulador de Latencia en Tiempo Real".

### Flujo:
1. El prospecto B2B ingresa su **número de teléfono** en el simulador.
2. El SDK procesa el dato → Edge Function → n8n → WAHA (WhatsApp HTTP API) → WhatsApp.
3. El prospecto recibe un **mensaje de WhatsApp antes de terminar de scrollear la página**.
4. Venta cerrada. El producto se vendió solo.

> **"Mide nuestra latencia en tiempo real."** — El titular es la demo.

### Por qué es poderoso:
- Es irrefutable. No hay presentación de PowerPoint. El producto habla.
- El lead queda registrado en nuestra base de datos (el simulador es también nuestro propio motor de captura).

---

## 4. Matriz de Manejo de Objeciones

| Objeción | Respuesta Táctica |
| :--- | :--- |
| **"Ya usamos WordPress / Elementor"** | *"Perfecto. No tocaremos tu web. Generaremos un script de 1 línea para inyectar nuestro Motor de Captura. Tu equipo de TI ni lo notará."* |
| **"¿Por qué el mantenimiento es tan caro?"** | *"No estás pagando hosting. Estás pagando la API de mensajería prioritaria, el motor lógico de enrutamiento 24/7 y la base de datos encriptada. ¿Cuánto te cuesta perder 5 leads calificados al mes por demoras del sistema actual?"* |
| **"¿Cómo sé que es escalable?"** | *"Esta arquitectura (Edge Functions + VPS Docker) es la misma base que soporta picos masivos de tráfico en campañas de grandes clientes de retail. Tenemos el mismo VPS corriendo 50 clientes en este momento."* |
| **"¿Y si WhatsApp falla?"** | *"El lead siempre queda guardado en nuestra base de datos primero. Aunque WhatsApp falle, la data nunca se pierde y el sistema reintenta automáticamente. Tu equipo de ventas también recibe el respaldo en Google Sheets."* |

---

## 5. Proceso de Onboarding y Time-to-Market

### Tier 1 (< 24 horas)
1. Alta del cliente en tabla `clients` y `clients_config` (Supabase Studio).
2. Generación del snippet `<script>` con el `clientId`.
3. El cliente pega el script en su web. Operativo.

### Tier 2 (< 5 días hábiles)
1. Día 1-2: Diseño y desarrollo de Landing Page en Astro.
2. Día 2-3: Configuración del flow n8n + WAHA (WhatsApp HTTP API) + Dead Letter Queue.
3. Día 4: QA completo (aislamiento CSS, stress test, fallback test).
4. Día 5: Deploy y entrega al cliente con métricas de latencia.
