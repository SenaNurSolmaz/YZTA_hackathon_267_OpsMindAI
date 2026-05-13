from fastapi import APIRouter
from pydantic import BaseModel
from app.db import get_db

router = APIRouter()


class ActivityCreate(BaseModel):
    text: str


@router.get("/activity-log")
async def get_activity_log():
    db = await get_db()
    rows = await db.query(
        """
        SELECT
            id,
            to_char(event_time AT TIME ZONE 'Europe/Istanbul', 'HH24:MI') AS time,
            event_time AS "eventTime",
            text
        FROM activity_log
        ORDER BY event_time DESC
        LIMIT 50
        """
    )
    result = []
    for r in rows:
        item = dict(r)
        if "eventTime" in item and hasattr(item["eventTime"], "isoformat"):
            item["eventTime"] = item["eventTime"].isoformat()
        result.append(item)
    return result


@router.post("/activity-log")
async def create_activity(req: ActivityCreate):
    db = await get_db()
    row = await db.execute_one(
        """
        INSERT INTO activity_log (text)
        VALUES ($1)
        RETURNING id, to_char(event_time AT TIME ZONE 'Europe/Istanbul', 'HH24:MI') AS time, text
        """,
        req.text
    )
    return {"ok": True, "entry": dict(row) if row else {}}
