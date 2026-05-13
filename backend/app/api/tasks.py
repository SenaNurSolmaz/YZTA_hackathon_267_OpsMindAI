from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db import get_db

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    owner: str
    due: str
    reason: Optional[str] = ""


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None
    owner: Optional[str] = None
    due: Optional[str] = None
    reason: Optional[str] = None


def _map_row(r: dict) -> dict:
    item = dict(r)
    if "createdAt" in item and hasattr(item["createdAt"], "isoformat"):
        item["createdAt"] = item["createdAt"].isoformat()
    if "created_at" in item and hasattr(item["created_at"], "isoformat"):
        item["created_at"] = item["created_at"].isoformat()
    return item


@router.get("/tasks")
async def get_tasks():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            id, title, owner, due, reason, status,
            created_at AS "createdAt"
        FROM tasks
        ORDER BY created_at DESC
        """
    )
    return [_map_row(r) for r in rows]


@router.post("/tasks")
async def create_task(req: TaskCreate):
    db = await get_db()
    row = await db.execute_one(
        """
        INSERT INTO tasks (title, owner, due, reason, status)
        VALUES ($1, $2, $3, $4, 'Acik')
        RETURNING id, title, owner, due, reason, status, created_at AS "createdAt"
        """,
        req.title, req.owner, req.due, req.reason or ""
    )
    if not row:
        raise HTTPException(status_code=500, detail="Gorev olusturulamadi")
    return {"ok": True, "entry": _map_row(row)}


@router.put("/tasks/{task_id}")
async def update_task(task_id: str, req: TaskUpdate):
    db = await get_db()

    existing = await db.query("SELECT id FROM tasks WHERE id = $1", task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Gorev bulunamadi")

    updates = []
    params = []
    idx = 1

    for field, col in [
        ("status", "status"), ("title", "title"),
        ("owner", "owner"), ("due", "due"), ("reason", "reason")
    ]:
        val = getattr(req, field)
        if val is not None:
            updates.append(f"{col} = ${idx}")
            params.append(val)
            idx += 1

    if not updates:
        raise HTTPException(status_code=400, detail="Guncellenecek alan yok")

    params.append(task_id)
    sql = f"""
        UPDATE tasks SET {', '.join(updates)}
        WHERE id = ${idx}
        RETURNING id, title, owner, due, reason, status, created_at AS "createdAt"
    """
    row = await db.execute_one(sql, *params)
    if not row:
        raise HTTPException(status_code=500, detail="Guncelleme basarisiz")
    return {"ok": True, "entry": _map_row(row)}


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    db = await get_db()
    existing = await db.query("SELECT id FROM tasks WHERE id = $1", task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Gorev bulunamadi")
    await db.execute("DELETE FROM tasks WHERE id = $1", task_id)
    return {"ok": True, "deleted": task_id}
