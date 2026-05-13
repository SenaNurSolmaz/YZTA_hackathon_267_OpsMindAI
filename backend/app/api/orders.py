from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db import get_db

router = APIRouter()


class OrderCreate(BaseModel):
    name: str
    customer: str
    city: str
    totalTry: float
    paymentStatus: Optional[str] = "Beklemede"
    fulfillmentStatus: Optional[str] = "Hazirlaniyor"
    itemCount: Optional[int] = 1
    channel: Optional[str] = "Web"
    product: str


def _map_row(r: dict) -> dict:
    item = dict(r)
    if "totalTry" in item:
        item["totalTry"] = float(item["totalTry"]) if item["totalTry"] else 0.0
    if "createdAt" in item and hasattr(item["createdAt"], "isoformat"):
        item["createdAt"] = item["createdAt"].isoformat()
    return item


@router.get("/orders")
async def get_orders():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            id, name, customer, city,
            total_try          AS "totalTry",
            payment_status     AS "paymentStatus",
            fulfillment_status AS "fulfillmentStatus",
            item_count         AS "itemCount",
            channel, product,
            created_at         AS "createdAt"
        FROM orders
        ORDER BY created_at DESC
        """
    )
    return [_map_row(r) for r in rows]


@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            id, name, customer, city,
            total_try          AS "totalTry",
            payment_status     AS "paymentStatus",
            fulfillment_status AS "fulfillmentStatus",
            item_count         AS "itemCount",
            channel, product,
            created_at         AS "createdAt"
        FROM orders
        WHERE id = $1
        """,
        order_id
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Siparis bulunamadi")
    return _map_row(rows[0])
