from typing import List

from fastapi import APIRouter
from SRC.models.usuari_commander import CreateUsuariCommander, UsuariCommander
from SRC.service.usuari_commander import create_usuari_commander, delete_usuari_commander_by_id, get_all_usuari_commanders, get_usuari_commander_by_id

router = APIRouter(
    prefix="/usuari_commander",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

#usuari_commander_service = UsuariCommanderService()
@router.get("/", response_model=List[UsuariCommander])
def all_usuari_commanders():
    return get_all_usuari_commanders()  

@router.get("/{id}", response_model=UsuariCommander)
def usuari_commander_by_id(id: int):    
    return get_usuari_commander_by_id(id)

@router.post("/{id}", response_model=UsuariCommander)
def create_new_usuari_commander(usuariCommander: CreateUsuariCommander):
    return create_usuari_commander(usuariCommander.id_player, usuariCommander.id_commander, usuariCommander.id_partida)

@router.delete("/{id}", response_model=dict)
def delete_usuari_commander(id: int):
    return delete_usuari_commander_by_id(id)   