from fastapi import HTTPException
from SRC.models.partida import *
from SRC.service import general
from typing import List

class PartidaService:
    async def  get_all_partides(self, partida:SelectAllPartida) -> List[Partida]:
        return [Partida(**p) for p in  general.select_all("partida",partida)]
    async def  get_partida_by_id(self, id: int) -> Partida:
        return Partida(**general.select_by_id("partida", id))
    async def  delete_partida_by_id(self, id: int) -> dict:
        return general.delete_by_id("partida", id)
    async def  create_partida(self, winner: int = None) -> Partida:
        return Partida(**general.create("partida",{"winner":winner}))
    async def  update_partida_winner(self, id: int, winner: int) -> Partida:
        return Partida(**general.update("partida",{"winner":winner},id))