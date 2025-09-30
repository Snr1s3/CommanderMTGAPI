from fastapi import HTTPException
from SRC.service import general
from ..models import UsuariCommander
from typing import List

def get_all_usuari_commanders() -> List[UsuariCommander]:
    usuari_commanders = general.select_all("usuari_commander")
    return [UsuariCommander(**c) for c in usuari_commanders]

def get_usuari_commander_by_id(id: int) -> UsuariCommander:
    c = general.select_by_id("usuari_commander", id)
    if c:
        return UsuariCommander(**c)
    else:
        raise HTTPException(status_code=404, detail="usuari_commander not found")

def delete_usuari_commander_by_id(id: int) -> dict:
    return general.delete_by_id("usuari_commander", id)

def create_usuari_commander(id_player: int, id_commander: int, id_partida: int) -> UsuariCommander:
    return UsuariCommander(**general.create("usuari_commander", {"id_player": id_player, "id_commander": id_commander, "id_partida": id_partida}))

def update_usuari_commander(id: int, id_player: int = None, id_commander: int = None, id_partida: int = None) -> UsuariCommander:
    data = {"id": id}
    if id_player is not None:
        data["id_player"] = id_player
    if id_commander is not None:
        data["id_commander"] = id_commander
    if id_partida is not None:
        data["id_partida"] = id_partida
    return UsuariCommander(**general.update("usuari_commander", data))