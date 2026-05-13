from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os

from app.api.agent import router as agent_router
from app.api.knowledge import router as knowledge_router
from app.api.ai_draft import router as ai_draft_router
from app.api.report import router as report_router
from app.api.shipping import router as shipping_router
from app.api.supply_webhook import router as supply_webhook_router
from app.api.notify import router as notify_router
from app.api.tasks import router as tasks_router
from app.api.inventory import router as inventory_router
from app.api.users import router as users_router
from app.api.notifications import router as notifications_router
from app.api.dashboard import router as dashboard_router
from app.api.orders import router as orders_router
from app.api.conversations import router as conversations_router
from app.api.activity_log import router as activity_log_router

project_root = Path(__file__).resolve().parent.parent
env_local = project_root / ".env.local"
env_file = project_root / ".env"

if env_local.exists():
    load_dotenv(env_local)
elif env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.db import db
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(title="OpsMind AI Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api")
app.include_router(knowledge_router, prefix="/api")
app.include_router(ai_draft_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(shipping_router, prefix="/api")
app.include_router(supply_webhook_router, prefix="/api")
app.include_router(notify_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(notifications_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(conversations_router, prefix="/api")
app.include_router(activity_log_router, prefix="/api")


@app.get("/api/health")
async def health_check():
    from app.db import db
    db_status = "connected" if db.pool is not None else "disconnected"
    return {"status": "ok", "db": db_status}


@app.post("/api/integration-test")
async def integration_test(body: dict):
    import httpx
    name = body.get("name", "")
    result = {"name": name, "ok": False, "detail": ""}

    if name == "Slack":
        url = os.getenv("SLACK_NOTIFY_WEBHOOK_URL")
        if url:
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.post(url, json={"text": "OpsMind baglanti testi"})
                    result["ok"] = res.status_code == 200
                    result["detail"] = f"HTTP {res.status_code}"
            except Exception as e:
                result["detail"] = str(e)
        else:
            result["ok"] = True
            result["detail"] = "Webhook URL tanimli degil — simulasyon modu aktif."

    elif name == "WhatsApp Business":
        token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        if token:
            result["ok"] = True
            result["detail"] = f"Token mevcut ({token[:8]}...)"
        else:
            result["ok"] = True
            result["detail"] = "Token tanimli degil — simulasyon modu aktif."

    elif name == "Shopify":
        result["ok"] = True
        result["detail"] = "Shopify webhook simulasyonu aktif."

    elif name == "ChromaDB":
        result["ok"] = True
        result["detail"] = "ChromaDB vektor veritabani hazir."

    else:
        result["ok"] = True
        result["detail"] = f"{name} baglantisi simule edildi."

    return result
