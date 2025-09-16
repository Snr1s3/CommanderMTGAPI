from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class partida(BaseModel):
    id : int
    winner : Optional[int] = None

class player(BaseModel):
    id : int
    name : str
    hash : str

class commander(BaseModel):
    id : int
    commander : str

class player_commander(BaseModel):
    id : int
    id_player : int
    id_commander : int
    id_partida : int

class AuthRequest(BaseModel):
    name: str
    pwd: str