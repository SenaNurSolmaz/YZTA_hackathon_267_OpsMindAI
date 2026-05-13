from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.db import get_db

router = APIRouter()


class NotificationUpdate(BaseModel):
    key: str
    enabled: Optional[bool] = None
    target: Optional[str] = None


class NotificationBulkUpdate(BaseModel):
    items: List[NotificationUpdate]


def _map_row(r: dict) -> dict:
    item = dict(r)
    if "updatedAt" in item and hasattr(item["updatedAt"], "isoformat"):
        item["updatedAt"] = item["updatedAt"].isoformat()
    if "updated_at" in item and hasattr(item["updated_at"], "isoformat"):
        item["updated_at"] = item["updated_at"].isoformat()
    return item


@router.get("/notifications")
async def get_notifications():
    db = await get_db()
    rows = await db.query(
        """
        SELECT key, label, target, enabled, updated_at AS "updatedAt"
        FROM notification_preferences
        ORDER BY key
        """
    )
    return [_map_row(r) for r in rows]


@router.put("/notifications")
async def update_notifications(req: NotificationBulkUpdate):
    db = await get_db()

    for update in req.items:
        updates = []
        params = []
        idx = 1

        if update.enabled is not None:
            updates.append(f"enabled = ${idx}")
            params.append(update.enabled)
            idx += 1
        if update.target is not None:
            updates.append(f"target = ${idx}")
            params.append(update.target)
            idx += 1

        if not updates:
            continue

        updates.append("updated_at = now()")
        params.append(update.key)
        sql = f"UPDATE notification_preferences SET {', '.join(updates)} WHERE key = ${idx}"
        await db.execute(sql, *params)

    rows = await db.query(
        "SELECT key, label, target, enabled, updated_at AS \"updatedAt\" FROM notification_preferences ORDER BY key"
    )
    return {"ok": True, "items": [_map_row(r) for r in rows]}
