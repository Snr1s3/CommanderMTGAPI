from fastapi import HTTPException
from SRC.routers import general
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import Partida
from typing import List

def get_all_partides() -> List[Partida]:
    partides = general.select_all("partida")
    return [Partida(**p) for p in partides]

def get_partida_by_id(id: int) -> Partida:
    p = general.select_by_id("partida", id)
    if p:
        return Partida(**p)
    else:
        raise HTTPException(status_code=404, detail="Partida not found")

def delete_partida_by_id(id: int) -> dict:
    return general.delete_by_id("partida", id)

def create_partida(winner: int = None) -> Partida:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO partida (winner)
            VALUES (%s)
            RETURNING *;
        """, (winner,))
        new_partida = cursor.fetchone()
        conn.commit()
        return Partida(**new_partida)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def update_partida_winner(id: int, winner: int) -> Partida:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            UPDATE partida
            SET winner = %s
            WHERE id = %s
            RETURNING *;
        """, (winner, id))
        updated_partida = cursor.fetchone()
        conn.commit()
        if updated_partida:
            return Partida(**updated_partida)
        else:
            raise HTTPException(status_code=404, detail="Partida not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)