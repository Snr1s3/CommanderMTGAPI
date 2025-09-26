from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class partida(BaseModel):
    id : int
    winner : Optional[int] = None

class commander(BaseModel):
    id : int
    commander : str

class usuari_commander(BaseModel):
    id : int
    id_player : int
    id_commander : int
    id_partida : int

class User(BaseModel):
    id : int
    name : str
    mail : str
    pwd : str


class AuthRequest(BaseModel):
    name: str
    pwd: str

class UpdateUsuari(BaseModel):
    id: int
    name: Optional[str] = None
    mail: Optional[str] = None
    pwd: Optional[str] = None