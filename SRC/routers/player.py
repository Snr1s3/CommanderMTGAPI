from fastapi import HTTPException
from routers import general
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import player
from typing import List
import bcrypt

def get_all_players() -> List[player]:
    players = general.select_all("player")
    return [player(**p) for p in players]

def get_player_by_id(id: int) -> player:
    p = general.select_by_id("player", id)
    if p:
        return player(**p)
    else:
        raise HTTPException(status_code=404, detail="Player not found")

def delete_player_by_id(id: int) -> dict:
    return general.delete_by_id("player", id)

def create_player(name: str, pwd : str) -> player:
    if not check_unique_name(name):
        raise HTTPException(status_code=400, detail="Player name already exists")
    hash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            INSERT INTO player (name, hash)
            VALUES (%s, %s)
            RETURNING *;
        """, (name,hash))
        new_player = cursor.fetchone()
        conn.commit()
        return player(**new_player)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def check_unique_name(name: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM player WHERE name = %s;", (name,))
        existing_player = cursor.fetchone()
        return existing_player is None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def authenticate_player(name: str, pwd: str) -> player:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM player WHERE name = %s;", (name,))
        results = cursor.fetchone()
        if bcrypt.checkpw(pwd.encode('utf-8'), results['hash'].encode('utf-8')):
            return player(**results)
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def update_player_hash(name: str, pwd: str) -> player:
    if not check_unique_name(name):
        raise HTTPException(status_code=400, detail="Player name already exists")
    hash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            UPDATE player
            SET hash = %s
            WHERE name = %s
            RETURNING *;
        """, (hash, name))
        updated_player = cursor.fetchone()
        conn.commit()
        if updated_player:
            return player(**updated_player)
        else:
            raise HTTPException(status_code=404, detail="Player not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)
        