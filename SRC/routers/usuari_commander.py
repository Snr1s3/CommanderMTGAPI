from typing import List

from fastapi import APIRouter, Depends
from SRC.models.usuari_commander import *
from SRC.service.usuari_commander import UsuariCommanderService

def get_usuari_commander_service():
    return UsuariCommanderService()
router = APIRouter(
    prefix="/usuaris_commanders",
    tags=["usuaris_commanders"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[UsuariCommander])
async def  all_usuari_commanders(
        usuari_commander:SelectAllUsuariCommander=Depends(),
        usuari_commander_service:UsuariCommanderService = Depends(get_usuari_commander_service)
    ):
    return await usuari_commander_service.get_all_usuari_commanders(usuari_commander)  

@router.get("/{id}", response_model=UsuariCommander)
async def  usuari_commander_by_id(
        id: int,
        usuari_commander_service:UsuariCommanderService = Depends(get_usuari_commander_service)
    ):   
    return await usuari_commander_service.get_usuari_commander_by_id(id)

@router.post("/", response_model=UsuariCommander)
async def  create_new_usuari_commander(
        usuariCommander: CreateUsuariCommander,
        usuari_commander_service:UsuariCommanderService = Depends(get_usuari_commander_service)
    ):
    return await usuari_commander_service.create_usuari_commander(usuariCommander.id_usuari, usuariCommander.id_commander, usuariCommander.id_partida)

@router.put("/{id}", response_model=UsuariCommander)
async def update_usuari_commander(
        id: int,
        usuari_commander: CreateUsuariCommander,
        usuari_commander_service: UsuariCommanderService = Depends(get_usuari_commander_service)
    ):
    return await usuari_commander_service.update_usuari_commander(id, 
usuari_commander.id_usuari, 
usuari_commander.id_commander, 
usuari_commander.id_partida
    )

@router.delete("/{id}", response_model=dict)
async def  delete_usuari_commander(
        id: int,
        usuari_commander_service:UsuariCommanderService = Depends(get_usuari_commander_service)
    ):
    return await usuari_commander_service.delete_usuari_commander_by_id(id)   