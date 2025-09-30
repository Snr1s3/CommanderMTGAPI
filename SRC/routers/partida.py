from typing import List

from fastapi import APIRouter
from SRC.models.partida import CreatePartida, Partida
from SRC.service.partida import create_partida, delete_partida_by_id, get_all_partides, get_partida_by_id, update_partida_winner

router = APIRouter(
    prefix="/partidas",
    tags=["partidas"],
    responses={404: {"description": "Not found"}}
)

#partida_service = PartidaService()
@router.get("/", response_model=List[Partida])
def all_partides():
    return get_all_partides()

@router.get("/{id}", response_model=Partida)
def partida_by_id(id: int):
    return get_partida_by_id(id)

@router.post("/{id}", response_model=Partida)
def create_new_partida(partida: CreatePartida):
    return create_partida(partida.winner)

@router.put("/{id}", response_model=Partida)
def update_partida(partida: Partida):
    return update_partida_winner(partida.id, partida.winner)

@router.delete("/{id}", response_model=dict)
def delete_partida(id: int):
    return delete_partida_by_id(id)