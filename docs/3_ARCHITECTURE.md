# Arquitectura — Lead Flow v2.0

> Estado: **BORRADOR PARA GATE 0**
> Objetivo: arquitectura mínima que conserva leads, permite reemplazar proveedores y genera evidencia de extremo a extremo.

## 1. Principios

1. **Persistir antes de integrar:** ninguna respuesta exitosa se emite sin lead y evento de entrega durables.
2. **Browser sin acceso a tablas:** el widget solo consume Edge Functions; no consulta ni escribe tablas por Data API.
3. **Entrega reintentable:** un webhook best-effort no constituye una cola.
4. **Idempotencia de extremo a extremo:** un retry no crea otro lead ni otra alerta.
5. **Mínimo dato necesario:** PII y metadatos tienen contrato, tamaño y retención definidos.
6. **Integraciones reemplazables:** n8n y Evolution API son decisiones actuales, pero viven detrás de interfaces explícitas.
7. **Evidencia antes de promesa:** rendimiento, uptime, escala y margen se miden antes de convertirse en SLA.
8. **Local primero:** schema y funciones se validan localmente; las mutaciones remotas requieren gate humano.

## 2. Flujo objetivo

```text
[Sitio del cliente]
        │ carga script + client_id
        ▼
[SDK / Shadow DOM]
        │ GET config / POST capture
        ▼
[Supabase Edge Functions]
  ├─ valida tenant, origen, esquema, consentimiento y abuso
  ├─ transacción: INSERT lead + INSERT delivery_outbox
  ├─ responde con lead_id + correlation_id
  └─ intenta disparo inmediato, sin borrar la obligación durable
        │
        ├──────────────┐
        ▼              ▼
[Dispatcher]      [Retry worker]
        │              │ reclama pendientes con backoff
        └──────┬───────┘
               ▼
     [Automation adapter]
       n8n existente
               │
               ▼
      [Messaging provider]
       Evolution API existente
               │
               ▼
           [Vendedor]
```

## 3. Componentes y responsabilidades

### SDK

- Registra un único Custom Element.
- Usa Preact únicamente como motor interno de renderizado; no lo expone en la API pública.
- Usa Shadow DOM para aislamiento.
- Expone integración mediante atributos, propiedades y eventos DOM documentados.
- Obtiene configuración por endpoint, no desde tablas.
- Renderiza solo tipos de campo admitidos por el esquema actual.
- Genera una idempotency key por intento intencional del usuario.
- No contiene claves secretas ni lógica de autorización.
- Muestra éxito cuando la captura quedó persistida, no cuando WhatsApp confirmó entrega.
- No incorpora router, estado global ni `preact/compat` salvo necesidad demostrada y aprobada en el SPEC.

### Config API

- Recibe `client_id` y observa `Origin` como señal de navegador.
- Verifica cliente activo y dominio permitido.
- Devuelve una proyección allowlist: tema, campos, textos, versión y URL de privacidad.
- Nunca devuelve webhooks, claves, IDs internos del proveedor ni configuración privada.
- Puede usar cache con invalidación por `config_version`.

### Capture API

- Acepta solo `POST` con tamaño máximo documentado.
- Valida content type, esquema versionado, cliente, dominio y consentimiento.
- Aplica honeypot y rate limit durable.
- Normaliza teléfono y metadatos permitidos.
- Inserta lead y outbox en una sola operación atómica.
- Devuelve `202` con IDs opacos después de persistir.
- No espera a Google Sheets ni a la entrega final para responder.

### Dispatcher y retry worker

- Reclaman eventos pendientes de manera segura para evitar doble procesamiento.
- Usan una clave idempotente al invocar downstream.
- Registran intento, proveedor, duración, código normalizado y error sanitizado.
- Implementan backoff y límite de intentos configurables.
- En agotamiento pasan a `dead_letter` y disparan alerta operacional.
- Un operador puede reencolar con trazabilidad.

`EdgeRuntime.waitUntil` puede acelerar el primer intento, pero no sustituye el outbox: una tarea en background sigue sujeta al ciclo de vida y límites de la función.

### Automation adapter — n8n

- Define un contrato estable frente a la instancia n8n existente.
- n8n hace routing e integraciones; la obligación durable permanece en Supabase.
- Google Sheets es una exportación operacional, no un backup autoritativo.
- El primer paso es inventariar en modo lectura versión, workflows relacionados, webhook esperado, credenciales lógicas y política de errores. No se leen valores secretos.
- Los workflows existentes se preservan; Lead Flow obtiene uno dedicado o cambios explícitamente aprobados.

### Messaging adapter — Evolution API

Contrato mínimo:

```ts
type SendResult = {
  providerMessageId?: string;
  acceptedAt: string;
  status: 'accepted' | 'retryable_error' | 'permanent_error';
  errorCode?: string;
};
```

- El adaptador encapsula autenticación, instance name, payload y errores de Evolution API.
- Antes de implementar, un inventario read-only confirma versión, healthcheck, instancia asignada, estado, modo `Baileys` o `WhatsApp Cloud API`, autenticación y webhooks activos.
- La API de Evolution no se llama desde el navegador ni expone su `apikey`; n8n usa credenciales administradas y alcance mínimo.
- No se modifica la instancia compartida, sus webhooks ni su conexión durante desarrollo sin GATE 2 y rollback.
- Los callbacks de estado, si se usan, deben validar autenticidad/firma conforme a la versión instalada y correlacionarse por ID de mensaje.

## 4. Modelo de datos lógico

Los nombres finales se fijan en `SPEC-LEADFLOW-05`; esta es la frontera contractual.

### `clients`

- `id uuid PK`
- `name text`
- `status enum/dominio: active | suspended`
- `created_at`, `updated_at`

### `client_domains`

- `id uuid PK`
- `client_id uuid FK`
- `origin text`
- `active boolean`
- índice único por cliente/origen normalizado

### `form_configs`

- `client_id uuid FK`
- `version integer`
- `schema jsonb`
- `theme jsonb`
- `messages jsonb`
- `privacy_policy_url text`
- `consent_version text`
- `active boolean`

El JSON se valida contra un esquema de aplicación versionado. JSONB aporta configuración, no permiso para aceptar estructuras arbitrarias.

### `integration_configs`

- Metadatos privados y referencias lógicas de integración.
- No contiene secretos públicos ni se expone a `anon`.
- Los secretos viven en Supabase Secrets/Vault o en el gestor aprobado.

### `leads`

- `id uuid PK`
- `client_id uuid FK`
- `idempotency_key_hash text`
- `payload jsonb`
- `source_url text`
- `consent_version text`
- `consented_at timestamptz`
- `received_at`, `persisted_at`
- restricción única por tenant + hash de idempotencia

### `delivery_outbox`

- `id uuid PK`
- `lead_id uuid FK`
- `client_id uuid FK`
- `channel text`
- `provider text`
- `status: pending | processing | accepted | retry_scheduled | dead_letter`
- `attempt_count integer`
- `next_attempt_at timestamptz`
- `locked_at`, `locked_by`
- `provider_message_id`
- `last_error_code`
- timestamps de estado

### `delivery_attempts`

- Registro append-only de cada intento.
- No guarda payload completo ni secretos.
- Permite calcular latencias y depurar sin consultar PII innecesaria.

## 5. API pública

### `GET /config?client_id=<uuid>`

Respuesta exitosa orientativa:

```json
{
  "clientId": "uuid",
  "configVersion": 3,
  "fields": [],
  "theme": {},
  "messages": {},
  "privacyPolicyUrl": "https://example.com/privacy",
  "consentVersion": "2026-10"
}
```

### `POST /capture`

Headers mínimos:

```text
Content-Type: application/json
Idempotency-Key: <valor opaco generado por el SDK>
```

Payload orientativo:

```json
{
  "clientId": "uuid",
  "configVersion": 3,
  "data": {
    "name": "Ejemplo",
    "phone": "+5511999999999"
  },
  "consent": {
    "version": "2026-10",
    "accepted": true
  },
  "metadata": {
    "utmSource": "campaign"
  },
  "website": ""
}
```

Respuesta persistida:

```json
{
  "leadId": "uuid",
  "correlationId": "uuid",
  "status": "accepted"
}
```

Los detalles exactos, límites y códigos se fijan en el SPEC del endpoint.

## 6. Seguridad

### Postgres y Data API

- Declarar `REVOKE`/`GRANT` explícitos; RLS y privileges son capas distintas.
- `anon` y `authenticated` no reciben acceso directo a tablas internas del MVP.
- Habilitar RLS como defensa en profundidad en toda tabla de esquema expuesto.
- No crear políticas `WITH CHECK (true)` para insertar leads públicos.
- No resolver permisos agregando `SECURITY DEFINER` sin un ADR y revisión específica.
- Toda vista expuesta debe ser `security_invoker` cuando la versión de Postgres lo permita, o permanecer fuera del esquema expuesto.

### Edge Functions

- La clave secreta/`service_role` solo existe en entorno servidor.
- Los nombres de secretos y su ubicación se documentan; sus valores nunca.
- CORS controla navegadores, no autentica bots ni requests server-side.
- Rate limiting no puede depender de memoria de un isolate.
- La IP se trata como dato operacional con retención limitada y, cuando sea viable, hash/sal rotativa.
- Errores públicos no revelan existencia de clientes, reglas internas ni SQL.

### PII

- No registrar payloads completos en logs.
- Enmascarar teléfono/email en evidencia.
- Separar acceso de operador, soporte y servicio.
- Auditar exportaciones y borrados.
- Definir retención antes de producción.

## 7. Estados e idempotencia

Un lead aceptado y su entrega son entidades distintas. La respuesta al prospecto depende de persistencia, no del estado final del proveedor.

```text
capture: received → persisted
delivery: pending → processing → accepted
                         └────→ retry_scheduled → processing
                                      └────────→ dead_letter
```

- La misma `Idempotency-Key` dentro del mismo tenant devuelve el resultado original.
- Un evento `accepted` no se reenvía automáticamente.
- Locks vencidos pueden recuperarse de forma segura.
- Los errores se clasifican como retryable o permanentes.

## 8. Observabilidad

Cada recorrido usa `correlation_id` y registra al menos:

- `submission_received_at`
- `lead_persisted_at`
- `dispatch_started_at`
- `provider_accepted_at`
- `delivery_failed_at`
- `attempt_count`
- `provider`
- `error_code` sanitizado

Métricas mínimas:

- Capturas válidas/rechazadas por causa.
- Persistencia fallida.
- Pendientes por edad.
- Tasa de aceptación del proveedor.
- Latencia p50/p95/p99.
- Dead letters.
- Duplicados evitados.

## 9. Entornos y despliegue

| Entorno | Datos | Permisos | Uso |
| --- | --- | --- | --- |
| Local | Sintéticos | Sin acceso cloud requerido | Migraciones, funciones y tests |
| Staging | Sintéticos o consentidos | Credenciales separadas | Integración y resiliencia |
| Producción/piloto | Reales mínimos | Acceso restringido + GATE 2 | Piloto aprobado |

- Migraciones se crean y prueban localmente.
- `supabase db push --dry-run` precede cualquier push remoto.
- `supabase db reset --linked` está prohibido en producción.
- Staging y producción no reutilizan credenciales, instancia o número de Evolution sin aprobación explícita.
- El primer remoto puede ser un proyecto Supabase Free de MVP/piloto; no se promete SLA y se vigilan tamaño, egress e invocaciones conforme a `docs/SUPABASE-FREE-TIER-READINESS.md`.
- Storage, Realtime, Vector y Auth no forman parte del MVP técnico mientras un SPEC aprobado no los justifique.

## 10. Referencias verificadas

- Seguridad Data API, grants y RLS: <https://supabase.com/docs/guides/api/securing-your-api>
- Flujo local y migraciones: <https://supabase.com/docs/guides/local-development/cli-workflows>
- Background tasks: <https://supabase.com/docs/guides/functions/background-tasks>
- Secrets de Edge Functions: <https://supabase.com/docs/guides/functions/secrets>
- Evolution API, tipos de conexión, autenticación y eventos: <https://github.com/evolution-foundation/evolution-api>

Última verificación documental: 2026-10-02.
