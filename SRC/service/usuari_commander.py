from fastapi import HTTPException
from SRC.models.usuari_commander import SelectAllUsuariCommander
from SRC.service import general
from ..models import UsuariCommander
from typing import List

class UsuariCommanderService:
    async def  get_all_usuari_commanders(self, usuari_commander: SelectAllUsuariCommander) -> List[UsuariCommander]:
        return [UsuariCommander(**c) for c in  general.select_all("usuari_commander",usuari_commander)]
    async def  get_usuari_commander_by_id(self, id: int) -> UsuariCommander:
        return UsuariCommander(**general.select_by_id("usuari_commander", id))
    async def  delete_usuari_commander_by_id(self, id: int) -> dict:
        return general.delete_by_id("usuari_commander", id)
    async def  create_usuari_commander(self, id_usuari: int, id_commander: int, id_partida: int) -> UsuariCommander:
        return UsuariCommander(**general.create("usuari_commander", {"id_usuari": id_usuari, "id_commander": id_commander, "id_partida": id_partida}))
    async def  update_usuari_commander(self, id: int, id_usuari: int = None, id_commander: int = None, id_partida: int = None) -> UsuariCommander:
        data = {}
        if id_usuari is not None:
            data["id_usuari"] = id_usuari
        if id_commander is not None:
            data["id_commander"] = id_commander
        if id_partida is not None:
            data["id_partida"] = id_partida
        return UsuariCommander(**general.update("usuari_commander", data, id))