import os
import asyncpg
from typing import List, Dict, Any, Optional


def _to_camel(snake: str) -> str:
    """snake_case -> camelCase donusturucu."""
    parts = snake.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def row_to_camel(row: Dict[str, Any]) -> Dict[str, Any]:
    """Veritabanindan gelen snake_case dict'i frontend icin camelCase'e cevirir."""
    result = {}
    for k, v in row.items():
        camel_key = _to_camel(k)

        if hasattr(v, "__float__"):
            result[camel_key] = float(v)
        elif hasattr(v, "isoformat"):
            result[camel_key] = v.isoformat()
        else:
            result[camel_key] = v
    return result


def rows_to_camel(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [row_to_camel(r) for r in rows]


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if self.pool is not None:
            return

        connection_string = os.getenv("DATABASE_URL")
        if not connection_string:
            print("[db] DATABASE_URL tanimli degil, DB olmadan calisiliyor.")
            return

        is_local = "localhost" in connection_string or "127.0.0.1" in connection_string

        try:
            if not is_local:
                import ssl
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                self.pool = await asyncpg.create_pool(connection_string, ssl=ctx, min_size=1, max_size=10)
            else:
                self.pool = await asyncpg.create_pool(connection_string, min_size=1, max_size=10)
            print("[db] PostgreSQL baglantisi basarili.")
        except Exception as e:
            print(f"[db] Veritabani baglantisi basarisiz: {e}")

    async def disconnect(self):
        if self.pool is not None:
            await self.pool.close()
            print("[db] PostgreSQL baglantisi kapatildi.")

    async def query(self, text: str, *params) -> List[Dict[str, Any]]:
        """SELECT sorgulari icin - List[Dict] dondurur."""
        if not self.pool:
            return []
        async with self.pool.acquire() as conn:
            records = await conn.fetch(text, *params)
            return [dict(r) for r in records]

    async def execute(self, text: str, *params) -> str:
        """INSERT/UPDATE/DELETE sorgulari icin - status string dondurur."""
        if not self.pool:
            return ""
        async with self.pool.acquire() as conn:
            return await conn.execute(text, *params)

    async def execute_one(self, text: str, *params) -> Optional[Dict[str, Any]]:
        """RETURNING ile tek satir dondurmesi beklenen sorgular icin."""
        if not self.pool:
            return None
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(text, *params)
            return dict(record) if record else None


db = Database()


async def get_db() -> Database:
    if db.pool is None:
        await db.connect()
    return db
