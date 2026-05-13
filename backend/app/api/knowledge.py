from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.db import get_db

router = APIRouter()


class KnowledgeEntry(BaseModel):
    title: str
    content: str
    category: Optional[str] = "Genel"
    addedBy: Optional[str] = "API"


def _map_row(r: dict) -> dict:
    item = dict(r)
    if "addedAt" in item and hasattr(item["addedAt"], "isoformat"):
        item["addedAt"] = item["addedAt"].isoformat()
    if "added_at" in item and hasattr(item["added_at"], "isoformat"):
        item["added_at"] = item["added_at"].isoformat()
    return item


@router.get("/knowledge")
async def get_knowledge():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            id, title, content, category,
            added_by AS "addedBy",
            added_at AS "addedAt"
        FROM knowledge_base
        ORDER BY added_at DESC
        """
    )
    return [_map_row(r) for r in rows]


@router.post("/knowledge")
async def create_knowledge(req: KnowledgeEntry):
    db = await get_db()
    row = await db.execute_one(
        """
        INSERT INTO knowledge_base (title, content, category, added_by)
        VALUES ($1, $2, $3, $4)
        RETURNING
            id, title, content, category,
            added_by AS "addedBy",
            added_at AS "addedAt"
        """,
        req.title, req.content, req.category, req.addedBy
    )
    if not row:
        raise HTTPException(status_code=500, detail="Kayit olusturulamadi")
    print(f"[knowledge] Yeni kayit: {row['id']}")
    return {"ok": True, "entry": _map_row(row)}


@router.delete("/knowledge")
async def delete_knowledge(id: str = Query(...)):
    db = await get_db()
    existing = await db.query("SELECT id FROM knowledge_base WHERE id = $1", id)
    if not existing:
        raise HTTPException(status_code=404, detail="Kayit bulunamadi")
    await db.execute("DELETE FROM knowledge_base WHERE id = $1", id)
    print(f"[knowledge] Silindi: {id}")
    return {"ok": True, "deleted": id}
