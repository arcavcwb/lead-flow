# DOC 2: Modelo de Negocio y Operaciones (v1.0)

## 1. Estructura de Tiers (Productized Service)

El modelo abandona la "venta por horas" y se centra en el **valor del lead rescatado**. Dos tiers productizados con precios y alcances definidos.

### Tier 1 — Motor Básico *(Para clientes con web propia)*
- **Qué incluye:** Inyección del SDK + Base de Datos Supabase + Respaldo en Google Sheets. Sin alertas WhatsApp.
- **Setup Fee:** Configuración de Supabase, diseño de campos en `clients_config` y snippet de instalación.
- **MRR:** Mantenimiento de servidor y base de datos.
- **Time-to-Market:** Cliente operando en **< 24 horas**.

### Tier 2 — Lead Flow PRO *(Ecosistema Completo)*
- **Qué incluye:** Landing Page en Astro + SDK + Automatización n8n + Alertas inmediatas por WhatsApp (WAHA (WhatsApp HTTP API)).
- **Setup Fee:** Alto ticket, incluye diseño frontend de alta conversión.
- **MRR:** Licencia del motor de automatización, WhatsApp y mantenimiento de VPS.
- **Time-to-Market:** Cliente operando en **< 5 días hábiles**.

---

## 2. Escalabilidad Operativa (SLA y Onboarding)

Para escalar a 50 clientes simultáneos sin contratar desarrolladores adicionales, el proceso de onboarding debe ser **completamente estandarizado y no-código**:

1. **Cero código a medida:** Cualquier campo personalizado (DNI, Código Postal, etc.) se registra en la tabla `clients_config`. El SDK lo renderiza dinámicamente sin tocar una línea de código.
2. **Instalación en 1 línea:** El equipo de TI del cliente solo pega un script tag. Nada más.
3. **Config centralizada:** Todos los cambios de configuración (colores, campos, webhooks) se gestionan directamente desde el panel de Supabase.

---

## 3. Unit Economics y Costos de Infraestructura

| Componente | Costo Estimado | Capacidad |
| :--- | :--- | :--- |
| VPS (Hetzner / DigitalOcean) | ~$20–40/mes | 50 clientes simultáneos vía Docker + Caddy |
| Supabase Pro | $25/mes | 100,000 ejecuciones de Edge Functions |
| Cloudflare R2 | ~$0 (escala inicial) | Cero costos de Egress en escala inicial |
| WAHA (WhatsApp HTTP API) | VPS propio (sin costo por mensaje) | Elimina costos de Twilio (~$0.005/msg) |

### Proyección de Gross Margin

> Una vez superados los **10 clientes activos**, el margen bruto mensual supera el **90%** al ser la infraestructura de costo fijo y no crecer linealmente con el número de clientes.

---

## 4. Ventaja Competitiva Económica (Moat)

Alojar **WAHA (WhatsApp HTTP API) en el VPS propio** e integrarlo con n8n vía API Key intra-servidor elimina el costo por mensaje de proveedores externos (Twilio, MessageBird). Esto es lo que sostiene el margen del ~90% y diferencia el modelo de cualquier solución basada en APIs de pago por uso.
