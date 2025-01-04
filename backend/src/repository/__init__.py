from typing import Optional

from sqlalchemy import Row

async def get_row(session, stmt) -> Optional[int]:
    res = await session.execute(stmt)
    row: Optional[Row[tuple[int]]] = res.first()
    return int(row[0]) if row else None

async def get_item_from_stmt(session, search_stmt, stmt) -> int:
    search_row = await get_row(session, search_stmt)
    if not search_row:
        row = await get_row(session, stmt)
        if row is None: raise ValueError("No ID returned")
        return row
    return search_row