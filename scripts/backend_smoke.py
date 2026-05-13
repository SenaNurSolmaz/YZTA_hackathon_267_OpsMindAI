import os
import sys

from fastapi.testclient import TestClient


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_ROOT = os.path.join(PROJECT_ROOT, "backend")
sys.path.insert(0, BACKEND_ROOT)

for name in (
    "GEMINI_API_KEY",
    "SLACK_SUPPLY_WEBHOOK_URL",
    "SLACK_NOTIFY_WEBHOOK_URL",
    "WHATSAPP_ACCESS_TOKEN",
    "WHATSAPP_PHONE_NUMBER_ID",
    "WHATSAPP_NOTIFY_NUMBER",
):
    os.environ[name] = ""

from main import app  # noqa: E402


client = TestClient(app)


def check(name: str, method: str, path: str, **kwargs):
    response = getattr(client, method)(path, **kwargs)
    ok = 200 <= response.status_code < 300
    if not ok:
      print(f"FAIL {name} {response.status_code} {response.text[:300]}")
      raise SystemExit(1)
    print(f"PASS {name} {response.status_code}")
    return response


def main():
    check("health", "get", "/api/health")
    check("dashboard:list", "get", "/api/dashboard")

    check("tasks:list", "get", "/api/tasks")
    task = check(
        "tasks:create",
        "post",
        "/api/tasks",
        json={"title": "Smoke task", "owner": "Ops", "due": "Bugün", "reason": "test"},
    ).json()["entry"]
    check("tasks:update", "put", f"/api/tasks/{task['id']}", json={"status": "Tamamlandi"})
    check("tasks:delete", "delete", f"/api/tasks/{task['id']}")

    check("inventory:list", "get", "/api/inventory")
    check("inventory:update", "put", "/api/inventory/SKU-SGR-01", json={"stock": 12})
    check("inventory:order", "post", "/api/inventory/order", json={"sku": "SKU-SGR-01", "quantity": 1})

    check("shipping:list", "get", "/api/shipping")

    check("users:list", "get", "/api/users")
    user = check(
        "users:create",
        "post",
        "/api/users",
        json={"name": "Smoke User", "email": "smoke@example.local", "role": "Destek", "department": "QA"},
    ).json()["entry"]
    check("users:update", "put", f"/api/users/{user['id']}", json={"active": False})

    check("notifications:list", "get", "/api/notifications")
    check(
        "notifications:update",
        "put",
        "/api/notifications",
        json={"items": [{"key": "cargo_high", "label": "Yüksek riskli kargo uyarısı", "target": "WhatsApp", "enabled": True}]},
    )

    check("knowledge:list", "get", "/api/knowledge")
    kb = check(
        "knowledge:create",
        "post",
        "/api/knowledge",
        json={"title": "Smoke KB", "content": "Smoke content", "category": "QA", "addedBy": "Test"},
    ).json()["entry"]
    check("knowledge:delete", "delete", f"/api/knowledge?id={kb['id']}")

    check("supply-webhook:simulation", "post", "/api/supply-webhook", json={"text": "Smoke supply"})
    check("notify:simulation", "post", "/api/notify", json={"slackText": "Smoke slack", "wpText": "Smoke whatsapp"})
    check("integration-test:slack", "post", "/api/integration-test", json={"name": "Slack"})

    ai_response = client.post(
        "/api/ai-draft",
        json={"customer": "Test", "topic": "Kargo", "channel": "WhatsApp", "message": "Merhaba", "orderRef": "#1"},
    )
    if ai_response.status_code != 500 or "Gemini API anahtarı" not in ai_response.text:
        print(f"FAIL ai-draft:no-key-error {ai_response.status_code} {ai_response.text[:300]}")
        raise SystemExit(1)
    print("PASS ai-draft:no-key-error 500")


if __name__ == "__main__":
    main()
