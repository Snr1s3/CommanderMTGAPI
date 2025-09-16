from fastapi import HTTPException
from routers import general
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import *
from typing import List

def get_all_player_commanders() -> List[player_commander]:
    player_commanders = general.select_all("player_commander")
    return [player_commander(**c) for c in player_commanders]

def get_player_commander_by_id(id: int) -> player_commander:
    c = general.select_by_id("player_commander", id)
    if c:
        return player_commander(**c)
    else:
        raise HTTPException(status_code=404, detail="Player_commander not found")

def delete_player_commander_by_id(id: int) -> dict:
    return general.delete_by_id("player_commander", id)

def create_player_commander(id_player: int, id_commander: int, id_partida: int) -> player_commander:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO player_commander (id_player, id_commander, id_partida)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (id_player, id_commander, id_partida))
        new_player_commander = cursor.fetchone()
        conn.commit()
        return player_commander(**new_player_commander)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)