from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date
import requests
from .models import *

from .client import *

from .routers.commander import *
from .routers.usuari import *
from .routers.partida import *
from .routers.usuari_commander import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/", response_model=str)
def root():
    return "API de Turnonauta operativa"


@app.get("/all_players", response_model=List[Usuari])
def all_players():
    return get_all_players()

@app.get("/player/{id}", response_model=Usuari)
def player_by_id(id: int):
    return get_player_by_id(id)

@app.post("/player/create", response_model=Usuari)
def create_new_player(Create: CreateUser):
    return player_create(Create)

@app.post("/player/authenticate/", response_model=Usuari)
def authenticate(Auth: AuthRequest):
    return player_authenticate(Auth)

@app.put("/player/update", response_model=Usuari)
def update_player(Update: UpdateUsuari):
    return player_update(Update)

@app.delete("/player/delete", response_model=dict)
def delete_player(id: int):
    return player_delete(id)

@app.get("/all_commanders", response_model=List[Commander])
def all_commanders():
    return get_all_commanders()

@app.get("/commander/{id}", response_model=Commander)
def commander_by_id(id: int):
    return get_commander_by_id(id)

@app.post("/commander/create", response_model=Commander)
def create_new_commander(commander: str):
    return create_commander(commander)

@app.delete("/commander/delete", response_model=dict)
def delete_commander(id: int):
    return delete_commander_by_id(id)   

@app.get("/all_partides", response_model=List[Partida])
def all_partides():
    return get_all_partides()

@app.get("/partida/{id}", response_model=Partida)
def partida_by_id(id: int):
    return get_partida_by_id(id)

@app.post("/partida/create", response_model=Partida)
def create_new_partida(winner: int = None):
    return create_partida(winner)

@app.put("/partida/update_winner", response_model=Partida)
def update_partida(id: int, winner: int):
    return update_partida_winner(id, winner)

@app.delete("/partida/delete", response_model=dict)
def delete_partida(id: int):
    return delete_partida_by_id(id)

@app.get("/all_usuari_commanders", response_model=List[UsuariCommander])
def all_usuari_commanders():
    return get_all_usuari_commanders()  
@app.get("/usuari_commander/{id}", response_model=UsuariCommander)
def usuari_commander_by_id(id: int):    
    return get_usuari_commander_by_id(id)
@app.post("/usuari_commander/create", response_model=UsuariCommander)
def create_new_usuari_commander(id_player: int, id_commander: int, id_partida: int):
    return create_usuari_commander(id_player, id_commander, id_partida)
@app.delete("/usuari_commander/delete", response_model=dict)
def delete_usuari_commander(id: int):
    return delete_usuari_commander_by_id(id)   