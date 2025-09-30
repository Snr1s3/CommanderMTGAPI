from pydantic import BaseModel, Field


class UsuariCommander(BaseModel):
    id: int = Field(..., description="Unique identifier for the relationship")
    id_player: int = Field(..., description="Player ID")
    id_commander: int = Field(..., description="Commander ID")
    id_partida: int = Field(..., description="Game ID")


class CreateUsuariCommander(BaseModel):
    id_player: int = Field(..., description="Player ID")
    id_commander: int = Field(..., description="Commander ID")
    id_partida: int = Field(..., description="Game ID")
