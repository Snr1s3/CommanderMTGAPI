from typing import List

from fastapi import APIRouter, Depends, HTTPException
from SRC.models.commander import *
from SRC.service.commander import CommanderService

def get_commander_service():
    return CommanderService()

router = APIRouter(
    prefix="/commanders",
    tags=["commanders"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[Commander])
async def  all_commanders(
        commander:SelectAllCommander=Depends(),
        commander_service: CommanderService = Depends(get_commander_service)
    ):
    return commander_service.get_all_commanders(commander)

@router.get("/{id}", response_model=Commander)
async def  commander_by_id(
        id: int,
        commander_service: CommanderService = Depends(get_commander_service)
    ):
    return commander_service.get_commander_by_id(id)

@router.post("/", response_model=Commander)
async def  create_new_commander(
        commander: CreateCommander,
        commander_service: CommanderService = Depends(get_commander_service)
    ):
        return commander_service.create_commander(commander.commander)
    
@router.put("/{id}", response_model=Commander)
async def update_commander(
        id: int,
        commander: UpdateCommander,
        commander_service: CommanderService = Depends(get_commander_service)
    ):
    return commander_service.update_commander(id, commander.commander)
@router.delete("/{id}", response_model=dict)
async def  delete_commander(
        id: int,
        commander_service: CommanderService = Depends(get_commander_service)
    ):
    return commander_service.delete_commander_by_id(id)  