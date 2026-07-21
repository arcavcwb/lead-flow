# SPEC-LEADFLOW-05: Backend Schema & Row Level Security (RLS)

## 1. Resumen de la Tarea
Diseñar y aplicar el esquema de la base de datos en Supabase para soportar la captura de leads multi-tenant (White-Label) y establecer políticas de seguridad estrictas (RLS) para evitar inyecciones, lecturas cruzadas y borrado de leads.

## 2. Requerimientos Técnicos

### Tablas a crear:
1. **`clients`**: Tabla principal de los dueños de los widgets (inquilinos).
2. **`clients_config`**: Tabla 1-to-1 con `clients` que almacena colores, logo, y dominios permitidos (CORS/Shadow DOM whitelisting).
3. **`leads_vault`**: La bóveda de leads. Almacena los prospectos capturados (nombre, email, teléfono, metadata) vinculados a un `client_id`.

### Reglas RLS (Row Level Security):
- **Lectura Pública (`SELECT`)**: 
  - `clients` y `clients_config`: Acceso anónimo solo de lectura (necesario para que el widget renderice).
  - `leads_vault`: **BLOQUEADO TOTALMENTE** para usuarios anónimos. Nadie puede leer los leads desde el cliente.
- **Escritura (`INSERT`)**:
  - `leads_vault`: Permitido para usuarios anónimos, **pero validando el origen** (el Honeypot de la Edge Function) o mediante inserción directa con clave pública.
- **Borrado (`DELETE`)**: **BLOQUEADO TOTALMENTE** para todos excepto `service_role`.

## 3. Estructura de Datos (Esquema SQL Propuesto)

```sql
-- clients
CREATE TABLE public.clients (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- clients_config
CREATE TABLE public.clients_config (
  client_id uuid REFERENCES public.clients(id) ON DELETE CASCADE PRIMARY KEY,
  allowed_domains text[] DEFAULT '{}'::text[],
  primary_color text DEFAULT '#000000',
  logo_url text,
  webhook_waha_url text -- Endpoint interno hacia n8n/WAHA
);

-- leads_vault
CREATE TABLE public.leads_vault (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  client_id uuid REFERENCES public.clients(id) ON DELETE CASCADE NOT NULL,
  full_name text NOT NULL,
  phone text NOT NULL,
  email text,
  status text DEFAULT 'new' CHECK (status IN ('new', 'processing', 'sent', 'failed')),
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);
```

## 4. Escenarios Gherkin (Criterios de Aceptación)

```gherkin
Escenario: El widget de un cliente consulta su configuración
  Dado un widget con el client_id "X" cargando en un dominio permitido
  Cuando solicita leer "clients_config"
  Entonces la base de datos debe retornar la configuración correctamente

Escenario: Un atacante intenta leer la bóveda de leads
  Dado un usuario anónimo externo
  Cuando envía un SELECT a la tabla "leads_vault"
  Entonces la base de datos debe rechazar la consulta (0 rows returned) por políticas RLS

Escenario: Inserción de un Lead
  Dado un payload válido desde la Edge Function
  Cuando se envía un INSERT a "leads_vault"
  Entonces el lead se guarda con status "new"
```

## 5. Notas de Implementación
- Se escribirá como un archivo de migración en `/supabase/migrations/`.
- No se habilitarán triggers SQL para notificaciones salientes; la captura se hará vía Webhook desde Supabase hacia n8n.
