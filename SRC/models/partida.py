from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Partida(BaseModel):
    id: int = Field(..., description="Unique identifier for the game")
    winner: Optional[int] = Field(None, description="ID of the winner")
    created_at: Optional[datetime] = Field(None, description="When the game was created")
    finished_at: Optional[datetime] = Field(None, description="When the game finished")

class CreatePartida(BaseModel):
    winner: Optional[int] = Field(None, description="ID of the winner")
