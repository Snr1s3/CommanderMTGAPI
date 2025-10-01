from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Partida(BaseModel):
    id: int = Field(..., description="Unique identifier for the game")
    winner: Optional[int] = Field(None, description="ID of the winner")

class CreatePartida(BaseModel):
    winner: Optional[int] = Field(None, description="ID of the winner")

class UpdatePartida(BaseModel):
    winner: Optional[int] = Field(None, description="Winner ID")
    
class SelectAllPartida(BaseModel):
    pag: Optional[int] = Field(None,description="Offset")
    limit: Optional[int] = Field(None,description="Limit")
    winner: Optional[int] = Field(None, description="ID of the winner")