# PRD Maestro: Lead Flow Engine (Motor de Captura B2B) v1.0

## 1. Resumen Ejecutivo y Visión

Lead Flow Engine es un ecosistema SaaS "White-Label" diseñado para eliminar la fricción tecnológica en la captura de leads B2B/B2C. El sistema desacopla la capa de presentación (Landing Pages) de la lógica de negocio mediante un enfoque de **Config-Driven UI** y microservicios.

Su propuesta de valor principal es reducir el **Costo Por Lead (CPL)** garantizando tiempos de carga ultrarrápidos y conectando prospectos con equipos de ventas a través de WhatsApp en **menos de 5 segundos**.

---

## 2. Público Objetivo (User Personas)

### 2.1. El Comprador (Director Comercial / CEO)
- **Dolor:** Alto gasto en marketing con baja conversión debido a tiempos de respuesta lentos y leads perdidos en bandejas de entrada.
- **Motivación:** ROI, velocidad de contacto y cierre de ventas. No le interesa la infraestructura subyacente, solo el resultado (el lead en el WhatsApp de su vendedor).
- **Fricción actual:** Sistemas heredados (WordPress/Elementor) lentos y desconectados.

### 2.2. El Usuario Final (Prospecto Móvil)
- **Contexto:** Representa el 80%+ del tráfico. Navega desde smartphones, frecuentemente bajo redes 4G inestables.
- **Comportamiento:** Baja paciencia. Abandonará el embudo ante cualquier fricción de UX (teclados incorrectos, auto-zoom accidental, tiempos de carga > 3 segundos).

---

## 3. Métricas de Éxito (KPIs y SLAs)

| Métrica | Objetivo | Justificación Técnica / Negocio |
| :--- | :--- | :--- |
| **Peso del SDK (Frontend)** | < 50kb (Gzip/Brotli) | Maximizar puntaje de Core Web Vitals y conversión en redes lentas. |
| **Tiempo de Carga SDK** | < 200ms | Evitar el abandono del usuario antes de que el formulario sea interactivo. |
| **Latencia de Entrega** | < 5.0 segundos | Desde el clic en "Enviar" hasta la vibración del WhatsApp del vendedor. |
| **Uptime de Infraestructura** | 99.9% | Garantizado mediante topología distribuida (Edge Functions + VPS). |
| **Time-to-Market (Setup)** | 24h (Tier 1) / 5 días (Tier 2) | Escalabilidad operativa sin horas de desarrollo a medida. |

---

## 4. Alcance (In Scope v1.0)
- **SDK Frontend (SolidJS):** Componente inyectable vía script estático. Config-Driven desde BD.
- **Gatekeeper API (Supabase Edge Functions):** Endpoint serverless para sanitización, rate limiting y enrutamiento seguro.
- **Motor de Automatización (VPS / n8n):** Flujos webhook-only para distribuir leads a CRMs.
- **Motor de Mensajería (WAHA (WhatsApp HTTP API)):** Alertas WhatsApp de baja latencia al vendedor.

## 5. Fuera de Alcance (Out of Scope v1.0)
- Dashboard web para que el cliente final edite sus propios formularios (la configuración la gestiona el equipo internamente en Supabase).
- Chatbots de IA conversacionales complejos (la primera notificación es una alerta estática de velocidad).

---

## 6. Modelo de Datos y Config-Driven UI

El sistema escala bajo la premisa de **"Cero Código a Medida"**. La UI del frontend se construye dinámicamente leyendo `clients_config`.

### Esquema Core (Supabase PostgreSQL)

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
- `payload` (JSONB — almacena nombre, teléfono y cualquier campo dinámico)
- `created_at` (Timestamp)
- `processed_by_n8n` (Boolean)

### Contrato de API (Payload SDK → Edge Function)

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

---

## 7. Requerimientos No Funcionales (Móvil Extremo y Seguridad)

Para garantizar la conversión móvil y la integridad del sistema, se imponen las siguientes reglas estrictas:

- **Anti-Zoom iOS (Obligatorio):** Todos los `<input>` dentro del Shadow DOM deben renderizar `font-size: 16px` mínimo para bloquear el zoom automático de Safari en iPhone.
- **Zonas Táctiles:** El `<button type="submit">` y los inputs deben tener `min-height: 48px` para cumplir estándares de accesibilidad táctil.
- **Teclados Contextuales:** Uso estricto de `type="tel"` e `inputMode="numeric"` para forzar el teclado numérico nativo al solicitar teléfonos.
- **Seguridad RLS:** Bloqueo a nivel de BD de cualquier inserción anónima a `leads_vault` que no provenga de un dominio autorizado firmado por la Edge Function.
