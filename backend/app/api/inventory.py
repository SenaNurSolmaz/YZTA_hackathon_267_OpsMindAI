from fastapi import APIRouter, HTTPException, Response
import io
import csv
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from app.db import get_db, row_to_camel

router = APIRouter()


class StockUpdate(BaseModel):
    stock: int
    reorder_point: Optional[int] = None
    weekly_velocity: Optional[int] = None
    supplier_lead_days: Optional[int] = None

class OrderRequest(BaseModel):
    sku: str
    quantity: Optional[int] = 20


def _map_row(r: dict) -> dict:
    item = dict(r)
    for key in ("unitPrice", "unit_price"):
        if key in item and isinstance(item[key], Decimal):
            item[key] = float(item[key])
    if "updatedAt" in item and hasattr(item["updatedAt"], "isoformat"):
        item["updatedAt"] = item["updatedAt"].isoformat()
    if "updated_at" in item and hasattr(item["updated_at"], "isoformat"):
        item["updated_at"] = item["updated_at"].isoformat()
    return item


@router.get("/inventory")
async def get_inventory():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            sku,
            product,
            category,
            stock,
            reorder_point     AS "reorderPoint",
            weekly_velocity   AS "weeklyVelocity",
            depletion_days    AS "depletionDays",
            recommendation,
            supplier_lead_days AS "supplierLeadDays",
            unit_price        AS "unitPrice",
            updated_at        AS "updatedAt"
        FROM inventory
        ORDER BY sku
        """
    )
    return [_map_row(r) for r in rows]

@router.get("/inventory/export")
async def export_inventory():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            sku, product, category, stock, reorder_point,
            weekly_velocity, depletion_days, recommendation,
            supplier_lead_days, unit_price
        FROM inventory
        ORDER BY sku
        """
    )
    
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
        "SKU", "Urun", "Kategori", "Stok", "Reorder Point", 
        "Haftalik Satis", "Tukenme Sure (Gun)", "Tedarik (Gun)", "Birim Fiyat", "AI Oneri"
    ])
    
    for r in rows:
        writer.writerow([
            r["sku"], r["product"], r["category"], r["stock"], r["reorder_point"],
            r["weekly_velocity"], r["depletion_days"], r["supplier_lead_days"], 
            r["unit_price"], r["recommendation"]
        ])
        
    return Response(
        content="\ufeff" + output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=stok-raporu.csv"}
    )



@router.put("/inventory/{sku}")
async def update_inventory(sku: str, req: StockUpdate):
    db = await get_db()

    existing = await db.query("SELECT sku, weekly_velocity FROM inventory WHERE sku = $1", sku)
    if not existing:
        raise HTTPException(status_code=404, detail="SKU bulunamadi")

    weekly_velocity = req.weekly_velocity if req.weekly_velocity is not None else existing[0]["weekly_velocity"]
    daily = weekly_velocity / 7
    depletion_days = max(1, round(req.stock / daily)) if daily > 0 else 999

    updates = ["stock = $1", "depletion_days = $2"]
    params = [req.stock, depletion_days]
    idx = 3
    
    if req.reorder_point is not None:
        updates.append(f"reorder_point = ${idx}")
        params.append(req.reorder_point)
        idx += 1
    if req.weekly_velocity is not None:
        updates.append(f"weekly_velocity = ${idx}")
        params.append(req.weekly_velocity)
        idx += 1
    if req.supplier_lead_days is not None:
        updates.append(f"supplier_lead_days = ${idx}")
        params.append(req.supplier_lead_days)
        idx += 1
        
    updates.append("updated_at = now()")
    params.append(sku)
    
    sql = f"""
        UPDATE inventory
        SET {', '.join(updates)}
        WHERE sku = ${idx}
        RETURNING
            sku, product, category, stock,
            reorder_point     AS "reorderPoint",
            weekly_velocity   AS "weeklyVelocity",
            depletion_days    AS "depletionDays",
            recommendation,
            supplier_lead_days AS "supplierLeadDays",
            unit_price        AS "unitPrice",
            updated_at        AS "updatedAt"
    """
    row = await db.execute_one(sql, *params)
    if not row:
        raise HTTPException(status_code=500, detail="Guncelleme basarisiz")

    return {"ok": True, "entry": _map_row(row)}


@router.post("/inventory/order")
async def order_inventory(req: OrderRequest):
    db = await get_db()

    existing = await db.query(
        "SELECT sku, stock, weekly_velocity FROM inventory WHERE sku = $1", req.sku
    )
    if not existing:
        raise HTTPException(status_code=404, detail="SKU bulunamadi")

    current_stock = existing[0]["stock"]
    weekly_velocity = existing[0]["weekly_velocity"]
    new_stock = current_stock + req.quantity
    daily = weekly_velocity / 7
    depletion_days = max(1, round(new_stock / daily)) if daily > 0 else 999

    row = await db.execute_one(
        """
        UPDATE inventory
        SET stock = $1, depletion_days = $2, updated_at = now()
        WHERE sku = $3
        RETURNING
            sku, product, category, stock,
            reorder_point     AS "reorderPoint",
            weekly_velocity   AS "weeklyVelocity",
            depletion_days    AS "depletionDays",
            recommendation,
            supplier_lead_days AS "supplierLeadDays",
            unit_price        AS "unitPrice",
            updated_at        AS "updatedAt"
        """,
        new_stock, depletion_days, req.sku
    )
    if not row:
        raise HTTPException(status_code=500, detail="Siparis islenemedi")

    return {"ok": True, "entry": _map_row(row)}
