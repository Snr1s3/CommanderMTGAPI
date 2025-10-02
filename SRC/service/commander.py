from fastapi import HTTPException
from SRC.service import general
from ..models.commander import Commander, SelectAllCommander
from typing import List

class CommanderService:
    def get_all_commanders(self, commander:SelectAllCommander) -> List[Commander]:
        return [Commander(**c) for c in general.select_all("commander",commander)]
    def get_commander_by_id(self, id: int) -> Commander:
        return Commander(**general.select_by_id("commander", id))
    def delete_commander_by_id(self, id: int) -> dict:
        return general.delete_by_id("commander", id)
    def  update_commander(self, id: int, commander: str = None) -> Commander:
        return Commander(**general.update("commander",{"commander":commander},id))
    def create_commander(self, commander_name: str) -> Commander:
        return Commander(**general.create("commander", {"commander": commander_name}))