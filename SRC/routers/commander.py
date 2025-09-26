from fastapi import HTTPException
from SRC.routers import general
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import *
from typing import List

def get_all_commanders() -> List[commander]:
    commanders = general.select_all("commander")
    return [commander(**c) for c in commanders]

def get_commander_by_id(id: int) -> commander:
    c = general.select_by_id("commander", id)
    if c:
        return commander(**c)
    else:
        raise HTTPException(status_code=404, detail="commander not found")

def delete_commander_by_id(id: int) -> dict:
    return general.delete_by_id("commander", id)

def create_commander(commander_name: str) -> commander:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO commander (commander)
            VALUES (%s)
            RETURNING *;
        """, (commander_name,))
        new_commander = cursor.fetchone()
        conn.commit()
        return commander(**new_commander)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)