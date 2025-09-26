from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Partida(BaseModel):
    id : int
    winner : Optional[int] = None

class Commander(BaseModel):
    id : int
    commander : str

class UsuariCommander(BaseModel):
    id : int
    id_player : int
    id_commander : int
    id_partida : int

class Usuari(BaseModel):
    id : int
    name : str
    mail : str
    hash : str

class CreateUser(BaseModel):
    name : str
    mail : str
    hash : str

class AuthRequest(BaseModel):
    name: str
    hash: str

class UpdateUsuari(BaseModel):
    id: int
    name: Optional[str] = None
    mail: Optional[str] = None
    hash: Optional[str] = None