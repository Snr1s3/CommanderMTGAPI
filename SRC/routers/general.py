from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from typing import List


def select_all(database : str) -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(f"SELECT * FROM {database};")
        results = cursor.fetchall()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def select_by_id(database : str, id : int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(f"SELECT * FROM {database} WHERE id = {id};")
        results = cursor.fetchone()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def create(database : str, data : dict) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{v}'" for v in data.values()])
        cursor.execute(f"INSERT INTO {database} ({columns}) VALUES ({values}) RETURNING *;")
        conn.commit()
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def update(database : str, data : dict) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        set_clause = ', '.join([f"{k} = '{v}'" for k, v in data.items()])
        cursor.execute(f"UPDATE {database} SET {set_clause} WHERE id = {id} RETURNING *;")
        conn.commit()
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def delete_by_id(database : str, id : int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(f"DELETE FROM {database} WHERE id = {id};")
        conn.commit()
        return {"message": f"Record with id {id} deleted from {database}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def check_id(database: str, id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(f"SELECT * FROM {database} WHERE id = {id};")
        conn.commit()
        return cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def check_duplicates(database: str, data: dict):
    