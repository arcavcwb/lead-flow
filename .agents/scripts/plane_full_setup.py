import urllib.request
import json
import ssl
from datetime import datetime, timedelta

API_KEY = "plane_api_512377479beb4978a69cce11b70cac71"
WORKSPACE = "lead-flow"
PROJECT_ID = "ec68b235-edb3-4884-8d8f-6333fd34a2db"
BASE_URL = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
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
        print(f"Error {e.code} on {path}: {e.read().decode()}")
        return None

print("--- INICIANDO CONFIGURACIÓN PROFUNDA DE PLANE ---")

# 1. Traer los tickets existentes
print("Obteniendo tickets creados...")
issues_resp = request("GET", "/issues/?per_page=100")
issues = issues_resp.get("results", []) if issues_resp else []

def find_issue_id(keyword):
    for i in issues:
        if keyword in i.get("name", ""):
            return i["id"]
    return None

# 2. Crear Etiquetas (Labels) Operacionales
print("Creando etiquetas operacionales...")
labels_to_create = [
    {"name": "spec-listo", "color": "#8B5CF6"},
    {"name": "spec-aprobado", "color": "#10B981"},
    {"name": "aprobado-para-merge", "color": "#3B82F6"},
    {"name": "cambios-solicitados", "color": "#EF4444"},
    {"name": "bug", "color": "#DC2626"}
]
labels_data = {}
for l in labels_to_create:
    res = request("POST", "/labels/", l)
    if res and "id" in res:
        labels_data[l["name"]] = res["id"]
    else:
        # Quizás ya exista
        pass

# 3. Crear Módulos (Épicas)
print("Creando Módulos (Épicas)...")
modules_to_create = [
    {"name": "Módulo A: Infraestructura y DevOps", "description": "Configuraciones core, CI/CD, despliegues."},
    {"name": "Módulo B: SDK Frontend", "description": "Widget SolidJS inyectable inmune."},
    {"name": "Módulo C: Backend & Bóveda", "description": "Supabase y Edge Functions seguras."},
    {"name": "Módulo D: Automatización y Mensajería", "description": "n8n y WAHA (WhatsApp HTTP API)."}
]
modules_data = {}
for m in modules_to_create:
    res = request("POST", "/modules/", m)
    if res and "id" in res:
        modules_data[m["name"]] = res["id"]

# Mapeo Módulos -> Tickets
mod_map = {
    "Módulo A: Infraestructura y DevOps": ["LEADFLOW-01", "LEADFLOW-02", "LEADFLOW-03", "LEADFLOW-10"],
    "Módulo B: SDK Frontend": ["LEADFLOW-04", "LEADFLOW-07", "LEADFLOW-09"],
    "Módulo C: Backend & Bóveda": ["LEADFLOW-05", "LEADFLOW-06"],
    "Módulo D: Automatización y Mensajería": ["LEADFLOW-08"]
}

for mod_name, t_keywords in mod_map.items():
    mod_id = modules_data.get(mod_name)
    if mod_id:
        issue_ids = [find_issue_id(k) for k in t_keywords if find_issue_id(k)]
        if issue_ids:
            # En v1, vincular modulo a issues se hace haciendo post en /modules/{mod_id}/issues/
            request("POST", f"/modules/{mod_id}/module-issues/", {"issues": issue_ids})

# 4. Crear Cycles (Sprints)
print("Creando Cycles (Sprints)...")
now = datetime.utcnow()
cycles_to_create = [
    {"name": "Cycle 0: Setup Base", "project": PROJECT_ID, "start_date": now.strftime("%Y-%m-%d"), "end_date": (now + timedelta(days=7)).strftime("%Y-%m-%d")},
    {"name": "Cycle 1: Bóveda y Gatekeeper", "project": PROJECT_ID, "start_date": (now + timedelta(days=8)).strftime("%Y-%m-%d"), "end_date": (now + timedelta(days=15)).strftime("%Y-%m-%d")},
    {"name": "Cycle 2: Widget Inmune", "project": PROJECT_ID, "start_date": (now + timedelta(days=16)).strftime("%Y-%m-%d"), "end_date": (now + timedelta(days=23)).strftime("%Y-%m-%d")},
    {"name": "Cycle 3: Alertas Producción", "project": PROJECT_ID, "start_date": (now + timedelta(days=24)).strftime("%Y-%m-%d"), "end_date": (now + timedelta(days=31)).strftime("%Y-%m-%d")}
]
cycles_data = {}
for c in cycles_to_create:
    res = request("POST", "/cycles/", c)
    if res and "id" in res:
        cycles_data[c["name"]] = res["id"]

# Mapeo Cycles -> Tickets
cyc_map = {
    "Cycle 0: Setup Base": ["LEADFLOW-01", "LEADFLOW-02", "LEADFLOW-03"],
    "Cycle 1: Bóveda y Gatekeeper": ["LEADFLOW-05", "LEADFLOW-06"],
    "Cycle 2: Widget Inmune": ["LEADFLOW-04", "LEADFLOW-07", "LEADFLOW-09"],
    "Cycle 3: Alertas Producción": ["LEADFLOW-08", "LEADFLOW-10"]
}

for cyc_name, t_keywords in cyc_map.items():
    cyc_id = cycles_data.get(cyc_name)
    if cyc_id:
        issue_ids = [find_issue_id(k) for k in t_keywords if find_issue_id(k)]
        if issue_ids:
            request("POST", f"/cycles/{cyc_id}/cycle-issues/", {"issues": issue_ids})

print("--- CONFIGURACIÓN DE MÓDULOS, CYCLES Y ETIQUETAS COMPLETADA ---")
