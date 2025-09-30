from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from typing import List

# Whitelist of allowed table names
ALLOWED_TABLES = {"commander", "usuari", "partida", "usuari_commander"}

def _validate_table_name(table_name: str):
    """Validate that the table name is in the allowed list"""
    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table_name}")

def select_all(database: str) -> List[dict]:
    _validate_table_name(database)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"SELECT * FROM {database};"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def select_by_id(database: str, id: int) -> dict:
    _validate_table_name(database)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"SELECT * FROM {database} WHERE id = %s;"
        cursor.execute(query, (id,))
        results = cursor.fetchone()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def create(database: str, data: dict) -> dict:
    _validate_table_name(database)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {database} ({columns}) VALUES ({placeholders}) RETURNING *;"
        cursor.execute(query, list(data.values()))
        conn.commit()
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def update(database: str, data: dict, id: int) -> dict:
    _validate_table_name(database)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {database} SET {set_clause} WHERE id = %s RETURNING *;"
        cursor.execute(query, list(data.values()) + [id])
        conn.commit()
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def delete_by_id(database: str, id: int) -> dict:
    _validate_table_name(database)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"DELETE FROM {database} WHERE id = %s;"
        cursor.execute(query, (id,))
        conn.commit()
        return {"message": f"Record with id {id} deleted from {database}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def check_id(database: str, id: int):
    _validate_table_name(database)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"SELECT * FROM {database} WHERE id = %s;"
        cursor.execute(query, (id,))
        return cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def check_duplicates(database: str, data: dict):
    _validate_table_name(database)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        conditions = []
        values = []
        
        for key, value in data.items():
            conditions.append(f"{key} = %s")
            values.append(value)
        
        where_clause = " OR ".join(conditions)
        query = f"SELECT * FROM {database} WHERE {where_clause};"
        
        cursor.execute(query, tuple(values))
        result = cursor.fetchone()
        return result is None  # Returns True if no duplicates (safe to create), False if duplicates exist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)
