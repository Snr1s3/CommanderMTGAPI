from typing import List

from fastapi import APIRouter, HTTPException
from SRC.models.commander import Commander, CreateCommander
from SRC.service.commander import create_commander, delete_commander_by_id, get_all_commanders, get_commander_by_id

router = APIRouter(
    prefix="/commanders",
    tags=["commanders"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[Commander])
def all_commanders():
    return get_all_commanders()

@router.get("/{id}", response_model=Commander)
def commander_by_id(id: int):
    return get_commander_by_id(id)

@router.post("/{id}", response_model=Commander)
def create_new_commander(commander: CreateCommander):
    try:
        return create_commander(commander.commander)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("{id}", response_model=dict)
def delete_commander(id: int):
    return delete_commander_by_id(id)  