from fastapi import HTTPException
from SRC.routers import general
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import *
from typing import List

def get_all_usuari_commanders() -> List[usuari_commander]:
    usuari_commanders = general.select_all("usuari_commander")
    return [usuari_commander(**c) for c in usuari_commanders]

def get_usuari_commander_by_id(id: int) -> usuari_commander:
    c = general.select_by_id("usuari_commander", id)
    if c:
        return usuari_commander(**c)
    else:
        raise HTTPException(status_code=404, detail="usuari_commander not found")

def delete_usuari_commander_by_id(id: int) -> dict:
    return general.delete_by_id("usuari_commander", id)

def create_usuari_commander(id_player: int, id_commander: int, id_partida: int) -> usuari_commander:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO usuari_commander (id_player, id_commander, id_partida)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (id_player, id_commander, id_partida))
        new_usuari_commander = cursor.fetchone()
        conn.commit()
        return usuari_commander(**new_usuari_commander)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)