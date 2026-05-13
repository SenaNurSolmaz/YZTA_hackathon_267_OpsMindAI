from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import PlainTextResponse
import io
import csv
from pydantic import BaseModel
from typing import Optional
from app.db import get_db, rows_to_camel, row_to_camel

router = APIRouter()


class ShippingUpdate(BaseModel):
    status: Optional[str] = None
    risk: Optional[str] = None


@router.get("/shipping")
async def get_shipping():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            s.order_id   AS "orderId",
            s.customer,
            s.provider,
            s.tracking_no AS "trackingNo",
            s.destination,
            s.status,
            s.last_event  AS "lastEvent",
            s.risk,
            s.sla_hours_left AS "slaHoursLeft",
            s.estimated_delivery AS "estimatedDelivery",
            s.product,
            s.updated_at  AS "updatedAt"
        FROM shipments s
        ORDER BY s.id
        """
    )
    result = []
    for r in rows:
        item = dict(r)
        if item.get("estimatedDelivery") and hasattr(item["estimatedDelivery"], "isoformat"):
            item["estimatedDelivery"] = item["estimatedDelivery"].isoformat()
        if item.get("updatedAt") and hasattr(item["updatedAt"], "isoformat"):
            item["updatedAt"] = item["updatedAt"].isoformat()
        result.append(item)
    return result


@router.get("/shipping/export")
async def export_shipping():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            order_id, customer, product, provider, tracking_no, destination,
            status, last_event, risk, sla_hours_left, estimated_delivery
        FROM shipments
        ORDER BY id
        """
    )
    
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
        "Siparis", "Musteri", "Urun", "Firma", "Takip No", 
        "Varis", "Durum", "Son Olay", "Risk", "SLA (saat)", "Tahmini Teslimat"
    ])
    
    for r in rows:
        est_del = r["estimated_delivery"].isoformat() if r["estimated_delivery"] and hasattr(r["estimated_delivery"], "isoformat") else str(r["estimated_delivery"])
        writer.writerow([
            r["order_id"], r["customer"], r["product"], r["provider"], r["tracking_no"],
            r["destination"], r["status"], r["last_event"], r["risk"], r["sla_hours_left"], est_del
        ])
        
    return Response(
        content="\ufeff" + output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=kargo-raporu.csv"}
    )



@router.put("/shipping/{order_id}")
async def update_shipping(order_id: str, req: ShippingUpdate):
    db = await get_db()

    # Mevcut kaydi kontrol et
    existing = await db.query(
        'SELECT id FROM shipments WHERE order_id = $1', order_id
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Kargo bulunamadi")

    # Guncelleme sorgusunu dinamik olarak olustur
    updates = []
    params = []
    idx = 1

    if req.status is not None:
        updates.append(f"status = ${idx}")
        params.append(req.status)
        idx += 1
    if req.risk is not None:
        updates.append(f"risk = ${idx}")
        params.append(req.risk)
        idx += 1

    if not updates:
        raise HTTPException(status_code=400, detail="Guncellenecek alan yok")

    updates.append("updated_at = now()")
    params.append(order_id)

    sql = f"UPDATE shipments SET {', '.join(updates)} WHERE order_id = ${idx} RETURNING *"
    row = await db.execute_one(sql, *params)
    if not row:
        raise HTTPException(status_code=500, detail="Guncelleme basarisiz")

    return {"ok": True, "entry": row_to_camel(row)}
