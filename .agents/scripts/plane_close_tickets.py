import urllib.request
import json
import ssl

API_KEY = "plane_api_512377479beb4978a69cce11b70cac71"
WORKSPACE = "lead-flow"
PROJECT_ID = "ec68b235-edb3-4884-8d8f-6333fd34a2db"
BASE_URL = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}"
HECHO_STATE_ID = "bb66c97d-3080-4977-99fb-520ac125ccae"

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

# 1. Traer todos los tickets
print("Buscando tickets...")
issues_resp = request("GET", "/issues/?per_page=100")
issues = issues_resp.get("results", []) if issues_resp else []

tickets_to_close = ["LEADFLOW-01", "LEADFLOW-02"]

for issue in issues:
    for keyword in tickets_to_close:
        if keyword in issue.get("name", ""):
            issue_id = issue["id"]
            print(f"Marcando {keyword} como Hecho...")
            # En Plane, actualizamos el estado enviando el ID del estado en el payload
            request("PATCH", f"/issues/{issue_id}/", {"state": HECHO_STATE_ID})

print("Tickets actualizados a 'Hecho' exitosamente.")
