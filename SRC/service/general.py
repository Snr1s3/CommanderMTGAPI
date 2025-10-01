from fastapi import HTTPException
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from typing import List

ALLOWED_TABLES = {"commander", "usuari", "partida", "usuari_commander"}

def _validate_table_name(table_name: str):
    if not table_name:
        raise HTTPException(status_code=400, detail="Table name cannot be empty")
    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table_name}")

def _validate_id(id: int):
    if not isinstance(id, int):
        raise HTTPException(status_code=400, detail="ID must be an integer")
    if id <= 0:
        raise HTTPException(status_code=400, detail="ID must be a positive integer")

def select_all(database: str, params:dict=None) -> List[dict]:
    _validate_table_name(database)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        pag = None
        limit = None
        if params is None:
            params = {}
        elif hasattr(params, 'dict'): 
            params= params.dict(exclude_none=True)
        else:  
            params = params.copy()
        if "pag" in params: 
            pag = params.pop("pag")
        
        if "limit" in params: 
            limit= params.pop("limit")

        if limit is None:
            limit = 10
        filters = params
        query = f"SELECT * FROM {database}"
        values = []
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                values.append(value)
            where_clause = " AND ".join(conditions)
            query += f" WHERE {where_clause}"

        if pag is not None and pag >= 1:
            offset = (pag - 1) * limit
            query += f" LIMIT {limit} OFFSET {offset}"
        else:
            query += f" LIMIT {limit}"
        
        query +=";"
        print(query)
        cursor.execute(query, tuple(values) if values else None)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        release_db_connection(conn)

def select_by_id(database: str, id: int) -> dict:
    _validate_table_name(database)
    _validate_id(id)
    
    if not check_id(database, id):
        raise HTTPException(status_code=404, detail=f"Record with id {id} not found in {database}")
    
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
    
    if not check_duplicates(database, data):
        raise HTTPException(status_code=409, detail="Record with this data already exists")
    
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
        conn.rollback()
        if 'unique constraint' in str(e).lower():
            raise HTTPException(status_code=409, detail="Record with this data already exists")
        elif 'foreign key constraint' in str(e).lower():
            raise HTTPException(status_code=400, detail="Referenced record does not exist")
        else:
            raise HTTPException(status_code=500, detail="Failed to create record")
    finally:
        cursor.close()
        release_db_connection(conn)

def update(database: str, data: dict, id: int) -> dict:
    _validate_table_name(database)
    _validate_id(id)
    
    if not check_id(database, id):
        raise HTTPException(status_code=404, detail=f"Record with id {id} not found in {database}")
    
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
        conn.rollback()
        if 'unique constraint' in str(e).lower():
            raise HTTPException(status_code=409, detail="Updated data conflicts with existing record")
        elif 'foreign key constraint' in str(e).lower():
            raise HTTPException(status_code=400, detail="Referenced record does not exist")
        else:
            raise HTTPException(status_code=500, detail="Failed to update record")
    finally:
        cursor.close()
        release_db_connection(conn)

def delete_by_id(database: str, id: int) -> dict:
    _validate_table_name(database)
    _validate_id(id)
    
    if not check_id(database, id):
        raise HTTPException(status_code=404, detail=f"Record with id {id} not found in {database}")
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"DELETE FROM {database} WHERE id = %s;"
        cursor.execute(query, (id,))
        conn.commit()
        return {"message": f"Record with id {id} deleted from {database}."}
    except Exception as e:
        conn.rollback()
        if 'foreign key constraint' in str(e).lower():
            raise HTTPException(status_code=409, detail="Cannot delete: record is referenced by other records")
        else:
            raise HTTPException(status_code=500, detail="Failed to delete record")
    finally:
        cursor.close()
        release_db_connection(conn)

def check_id(database: str, id: int) -> bool:
    _validate_table_name(database)
    _validate_id(id)
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = f"SELECT 1 FROM {database} WHERE id = %s LIMIT 1;"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"Error checking ID {id} in {database}: {e}")
        return False
    finally:
        cursor.close()
        release_db_connection(conn)

def check_duplicates(database: str, data: dict) -> bool:
    _validate_table_name(database)
    
    if not data:
        return True  
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        conditions = []
        values = []
        
        for key, value in data.items():
            conditions.append(f"{key} = %s")
            values.append(value)
        
        where_clause = " OR ".join(conditions)
        query = f"SELECT 1 FROM {database} WHERE {where_clause} LIMIT 1;"
        
        cursor.execute(query, tuple(values))
        result = cursor.fetchone()
        
        return result is None 
    except Exception as e:
        print(f"Error checking duplicates in {database}: {e}")
        return False  
    finally:
        cursor.close()
        release_db_connection(conn)
