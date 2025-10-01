from typing import Optional
from pydantic import BaseModel, Field


class UsuariCommander(BaseModel):
    id: int = Field(..., description="Unique identifier for the relationship")
    id_usuari: int = Field(..., description="Player ID")
    id_commander: int = Field(..., description="Commander ID")
    id_partida: int = Field(..., description="Game ID")


class CreateUsuariCommander(BaseModel):
    id_usuari: int = Field(..., description="Player ID")
    id_commander: int = Field(..., description="Commander ID")
    id_partida: int = Field(..., description="Game ID")

class UpdateUsuariCommander(BaseModel):
    id_usuari: Optional[int] = Field(None, description="Player ID")
    id_commander: Optional[int] = Field(None, description="Commander ID")
    id_partida: Optional[int] = Field(None, description="Game ID")
    
class SelectAllUsuariCommander(BaseModel):
    
    pag: Optional[int] = Field(None,description="Offset")
    limit: Optional[int] = Field(None,description="Limit")
    id_usuari: Optional[int] = Field(None, description="Player ID")
    id_commander: Optional[int] = Field(None, description="Commander ID")
    id_partida: Optional[int] = Field(None, description="Game ID")