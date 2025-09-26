from fastapi import HTTPException
from SRC.routers import general
from ..client import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from ..models import *
from typing import List

def get_all_commanders() -> List[Commander]:
    commanders = general.select_all("commander")
    return [Commander(**c) for c in commanders]

def get_commander_by_id(id: int) -> Commander:
    if general.check_id("commander", id):
        return Commander(**general.select_by_id("commander", id))
    else:
        return {"message": "Id not found"}

def delete_commander_by_id(id: int) -> dict:
    if general.check_id("commander", id):
        return general.delete_by_id("commander", id)
    else:
        return {"message": "Id not found"}

def create_commander(commander_name: str) -> Commander:
    return Commander(**general.create("commander", {"commander_name": commander_name}))