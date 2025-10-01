from typing import List

from fastapi import APIRouter, Depends
from SRC.models.partida import *
from SRC.service.partida import PartidaService

def get_partida_service():
    return PartidaService()

router = APIRouter(
    prefix="/partides",
    tags=["partides"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[Partida])
async def  all_partides(
        partida:SelectAllPartida=Depends(),
        partida_service: PartidaService = Depends(get_partida_service)
    ):
    return await partida_service.get_all_partides(partida)

@router.get("/{id}", response_model=Partida)
async def  partida_by_id(
        id: int,
        partida_service: PartidaService = Depends(get_partida_service)
    ):
    return await partida_service.get_partida_by_id(id)

@router.post("/", response_model=Partida)
async def  create_new_partida(
        partida: CreatePartida,
        partida_service: PartidaService = Depends(get_partida_service)
    ):
    return await partida_service.create_partida(partida.winner)

@router.put("/{id}", response_model=Partida)
async def  update_partida(
        id: int,
        partida: UpdatePartida,
        partida_service: PartidaService = Depends(get_partida_service)
    ):
    return await partida_service.update_partida_winner(id, partida.winner)

@router.delete("/{id}", response_model=dict)
async def  delete_partida(
        id: int,
        partida_service: PartidaService = Depends(get_partida_service)
    ):
    return await partida_service.delete_partida_by_id(id)