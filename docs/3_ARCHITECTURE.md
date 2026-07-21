# DOC 3: Arquitectura Técnica del Sistema (v1.0)

El sistema utiliza una **arquitectura orientada a eventos**, diseñada para resiliencia extrema y procesamiento asíncrono en 4 capas desacopladas.

---

## Las 4 Capas del Sistema

### Capa 1 — Frente de Captura *(Red del Cliente)*

| Item | Detalle |
| :--- | :--- |
| **Tecnología** | SolidJS encapsulado en Shadow DOM + Vite |
| **Implementación** | Inyección vía `<script>` estático (1 línea) compatible con cualquier CMS |
| **Compatibilidad** | WordPress, Astro, HTML estático, Shopify |

**Defensa Arquitectónica:**
- El **Shadow DOM** garantiza aislamiento absoluto de CSS. Ningún estilo externo (WordPress, Bootstrap, Tailwind con `!important`) puede mutar el diseño del widget.
- **SolidJS** (sin Virtual DOM) garantiza el cumplimiento del límite de **< 50kb** y **< 200ms TTI** al ser reactivo a nivel de compilador.

---

### Capa 2 — Gatekeeper y Bóveda *(Supabase)*

| Item | Detalle |
| :--- | :--- |
| **Tecnología** | Supabase Edge Functions (Deno / TypeScript) + PostgreSQL |
| **Función** | Validación de CORS, Rate Limiting por IP, inserción en `leads_vault` |

**Defensa Arquitectónica:**
- El payload viaja primero a la **red global Edge** de Supabase (distribuida), no al VPS directamente.
- Si el VPS (Capa 3) sufre una caída total, **el lead queda resguardado en PostgreSQL**. Cero pérdida de datos garantizada.

---

### Capa 3 — Motor Operativo *(VPS Propio)*

| Item | Detalle |
| :--- | :--- |
| **Tecnología** | VPS (Hetzner/DigitalOcean) + Caddy (Reverse Proxy) + Docker + n8n |
| **Función** | Routing lógico de eventos en modo webhook-only |

**Defensa Arquitectónica:**
- n8n opera en **modo webhook-only** (huella mínima de CPU).
- Ejecuta **sub-procesos en paralelo**: respaldo a Google Sheets (4a) + alerta WhatsApp (4b) simultáneamente.
- Esto evita que la latencia de un tercero (ej. API de Google) afecte el KPI de **< 5 segundos** de entrega.
- **Dead Letter Queue (DLQ):** Si WAHA (WhatsApp HTTP API) falla, el Catch Node programa reintentos automáticos a los 2, 5 y 15 minutos. El usuario final nunca ve un error.

---

### Capa 4 — Impacto Móvil *(Motor de Mensajería)*

| Item | Detalle |
| :--- | :--- |
| **Tecnología** | WAHA (WhatsApp HTTP API) (WhatsApp Engine) + Cloudflare R2 |
| **Función** | Alertas instantáneas al vendedor y mensaje de bienvenida al prospecto |

**Defensa Arquitectónica:**
- Alojado en el VPS propio, integrado con n8n vía **API Key intra-servidor**.
- Elimina el costo por mensaje de proveedores externos (Twilio), sosteniendo el **Gross Margin del ~90%**.
- Cloudflare R2 gestiona adjuntos con **cero costos de Egress** a escala inicial.

---

## Flujo de Datos Completo

```
[Prospecto Mobile]
      │  POST payload
      ▼
[Capa 1: SolidJS SDK / Shadow DOM]
      │  JSON + clientId + metadata
      ▼
[Capa 2: Supabase Edge Function]
  ├── Valida CORS (dominio_autorizado)
  ├── Rate Limiting por IP + Honeypot
  ├── Inserta en leads_vault (PostgreSQL) ← Bóveda permanente
  └── Llama webhook n8n (async)
      │
      ▼
[Capa 3: n8n VPS - Modo Webhook]
  ├── Respaldo → Google Sheets (paralelo)
  └── Dispara → WAHA (WhatsApp HTTP API)
          │
          ▼
[Capa 4: WAHA (WhatsApp HTTP API)]
      └── WhatsApp alert → Vendedor (< 5s total)
```

---

## Infraestructura de Red (VPS)

- **Caddy (Reverse Proxy):** Terminador SSL automático y enrutamiento interno de la red Docker.
- **n8n:** Modo webhook-only para minimizar carga de CPU. Catch Node global para errores de WAHA (WhatsApp HTTP API).
- **WAHA (WhatsApp HTTP API):** Integrado con Cloudflare R2 para adjuntos. Modo `apikey` global para comunicación segura intra-servidor.

---

## Esquema de Base de Datos (Supabase PostgreSQL)

**Tabla: `clients`**
- `id` (UUID, PK)
- `empresa_nombre` (Text)
- `dominio_autorizado` (Text — para validación CORS)
- `activo` (Boolean)

**Tabla: `clients_config` (Config-Driven UI)**
- `client_id` (UUID, FK → clients)
- `theme_color` (String, Hex)
- `require_age` (Boolean)
- `legal_disclaimer` (Text)
- `webhook_n8n_url` (String, Encriptado)

**Tabla: `leads_vault`**
- `id` (UUID, PK)
- `client_id` (UUID, FK → clients)
- `payload` (JSONB — almacena nombre, teléfono y campos dinámicos)
- `created_at` (Timestamp)
- `processed_by_n8n` (Boolean)

---

## Contrato de API (Payload SDK → Edge Function)

```json
{
  "clientId": "uuid-del-cliente",
  "data": {
    "nombre": "Juan Pérez",
    "telefono": "551199999999",
    "edad": 35
  },
  "metadata": {
    "utm_source": "facebook",
    "device": "mobile"
  }
}
```
