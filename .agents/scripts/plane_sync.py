import urllib.request
import json
import ssl

API_KEY = "plane_api_512377479beb4978a69cce11b70cac71"
WORKSPACE = "lead-flow"
PROJECT_ID = "ec68b235-edb3-4884-8d8f-6333fd34a2db"
BASE_URL = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def request(method, path, data=None):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode("utf-8")
    
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")
        return None

# 1. Traer estados actuales
print("Obteniendo estados actuales...")
states_response = request("GET", "/states/")
states = states_response.get("results", [])
state_ids = {s["name"]: s["id"] for s in states}

# 2. Configurar nuestros estados de workflow
workflow_states = [
    {"name": "Refinado", "color": "#8B5CF6", "group": "unstarted", "description": "Con SPEC listo y esperando GATE 1"},
    {"name": "En desarrollo", "color": "#3B82F6", "group": "started", "description": "Implementador trabajando"},
    {"name": "En pruebas", "color": "#F59E0B", "group": "started", "description": "Tester ejecutando Gherkin"},
    {"name": "En revisión", "color": "#EC4899", "group": "started", "description": "Revisor auditando PR vs SPEC"}
]

for ws in workflow_states:
    if ws["name"] not in state_ids:
        print(f"Creando estado: {ws['name']}...")
        new_state = request("POST", "/states/", ws)
        if new_state:
            state_ids[ws["name"]] = new_state["id"]

# Actualizar estado 'Todo' a 'Refinado' si se quiere, o simplemente ignorarlo (usar los creados).
# También actualizar 'Done' a 'Hecho'
if "Done" in state_ids:
    request("PATCH", f"/states/{state_ids['Done']}/", {"name": "Hecho"})
    state_ids["Hecho"] = state_ids["Done"]

backlog_id = state_ids.get("Backlog")

# 3. Crear el Backlog de Tickets
tickets = [
    {"name": "LEADFLOW-01: Configuración Git, remoto y documentación", "state_id": backlog_id, "description_html": "<p>Setup de repositorio y trazabilidad base.</p>"},
    {"name": "LEADFLOW-02: Setup Monorepo (pnpm workspaces)", "state_id": backlog_id, "description_html": "<p>Crear apps/sdk y supabase/</p>"},
    {"name": "LEADFLOW-03: Reglas de Calidad (Prettier, ESLint)", "state_id": backlog_id, "description_html": "<p>Linting global y auto-check.</p>"},
    {"name": "LEADFLOW-04: SDK Scaffold SolidJS + Vite + Shadow DOM", "state_id": backlog_id, "description_html": "<p>Setup base del SDK inyectable.</p>"},
    {"name": "LEADFLOW-05: Backend Schema + RLS + Edge stub", "state_id": backlog_id, "description_html": "<p>Tablas clients, clients_config, leads_vault.</p>"},
    {"name": "LEADFLOW-06: Gatekeeper CORS, Rate Limiting, Honeypot", "state_id": backlog_id, "description_html": "<p>Seguridad en Edge Functions.</p>"},
    {"name": "LEADFLOW-07: Lead Form Component", "state_id": backlog_id, "description_html": "<p>UI mobile-first, inputs semánticos, theme dinámico.</p>"},
    {"name": "LEADFLOW-08: Workflow n8n -> WAHA (WhatsApp HTTP API)", "state_id": backlog_id, "description_html": "<p>Webhook a Sheets y WhatsApp con DLQ.</p>"},
    {"name": "LEADFLOW-09: QA Playwright E2E", "state_id": backlog_id, "description_html": "<p>Stress test y shadow dom check.</p>"},
    {"name": "LEADFLOW-10: Deploy Prod (VPS, Docker, Caddy)", "state_id": backlog_id, "description_html": "<p>Pase a producción de la infraestructura.</p>"}
]

print("Creando 10 tickets del Backlog...")
for t in tickets:
    res = request("POST", "/issues/", t)
    if res:
        print(f"Ticket creado: {res.get('sequence_id')} - {t['name']}")

print("Sincronización con Plane completada exitosamente.")
