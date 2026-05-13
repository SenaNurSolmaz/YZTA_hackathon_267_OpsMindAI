from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db import get_db

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: str
    role: Optional[str] = "Destek"
    department: Optional[str] = ""


class UserUpdate(BaseModel):
    role: Optional[str] = None
    active: Optional[bool] = None
    department: Optional[str] = None


def _map_row(r: dict) -> dict:
    item = dict(r)
    if "createdAt" in item and hasattr(item["createdAt"], "isoformat"):
        item["createdAt"] = item["createdAt"].isoformat()
    if "created_at" in item and hasattr(item["created_at"], "isoformat"):
        item["created_at"] = item["created_at"].isoformat()
    return item


@router.get("/users")
async def get_users():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            id, name, email, role, department, active,
            created_at AS "createdAt"
        FROM users
        ORDER BY name
        """
    )
    return [_map_row(r) for r in rows]


@router.post("/users")
async def create_user(req: UserCreate):
    db = await get_db()

    existing = await db.query("SELECT id FROM users WHERE email = $1", req.email)
    if existing:
        raise HTTPException(status_code=409, detail="Bu e-posta zaten kayitli")

    row = await db.execute_one(
        """
        INSERT INTO users (name, email, role, department, active)
        VALUES ($1, $2, $3, $4, true)
        RETURNING id, name, email, role, department, active, created_at AS "createdAt"
        """,
        req.name, req.email, req.role, req.department
    )
    if not row:
        raise HTTPException(status_code=500, detail="Kullanici olusturulamadi")
    return {"ok": True, "entry": _map_row(row)}


@router.put("/users/{user_id}")
async def update_user(user_id: str, req: UserUpdate):
    db = await get_db()

    existing = await db.query("SELECT id FROM users WHERE id = $1", user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")

    updates = []
    params = []
    idx = 1

    for field, col in [("role", "role"), ("active", "active"), ("department", "department")]:
        val = getattr(req, field)
        if val is not None:
            updates.append(f"{col} = ${idx}")
            params.append(val)
            idx += 1

    if not updates:
        raise HTTPException(status_code=400, detail="Guncellenecek alan yok")

    params.append(user_id)
    sql = f"""
        UPDATE users SET {', '.join(updates)}
        WHERE id = ${idx}
        RETURNING id, name, email, role, department, active, created_at AS "createdAt"
    """
    row = await db.execute_one(sql, *params)
    if not row:
        raise HTTPException(status_code=500, detail="Guncelleme basarisiz")
    return {"ok": True, "entry": _map_row(row)}
