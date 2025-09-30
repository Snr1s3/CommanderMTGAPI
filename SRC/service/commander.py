from fastapi import HTTPException
from SRC.service import general
from ..models.commander import Commander
from typing import List

def get_all_commanders() -> List[Commander]:
    commanders = general.select_all("commander")
    return [Commander(**c) for c in commanders]

def get_commander_by_id(id: int) -> Commander:
    if general.check_id("commander", id):
        return Commander(**general.select_by_id("commander", id))
    else:
        raise HTTPException(status_code=404, detail="Commander not found")

def delete_commander_by_id(id: int) -> dict:
    if general.check_id("commander", id):
        return general.delete_by_id("commander", id)
    else:
        raise HTTPException(status_code=404, detail="Commander not found")

def create_commander(commander_name: str) -> Commander:
    if general.check_duplicates("commander", {"commander": commander_name}):
        return Commander(**general.create("commander", {"commander": commander_name}))
    else:
        raise HTTPException(status_code=404, detail="Commander Duplicated")