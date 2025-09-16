from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date

from .models import *

from .client import *

from .routers.player import *
from .routers.commander import *
from .routers.partida import *
from .routers.player_commander import *

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

@app.get("/check", response_model=str)
def check():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de connexió a la base de dades")
    release_db_connection(conn) 
    return "DDBB operativa"

@app.get("/all_players", response_model=List[player])
def all_players():
    return get_all_players()

@app.get("/player/{id}", response_model=player)
def player_by_id(id: int):
    return get_player_by_id(id)

@app.post("/player/create", response_model=player)
def create_new_player(Auth: AuthRequest):
    return create_player(Auth.name, Auth.pwd)

@app.post("/player/authenticate/", response_model=player)
def authenticate(Auth: AuthRequest):
    return authenticate_player(Auth.name, Auth.pwd)

@app.put("/player/update", response_model=player)
def update_player(Auth: AuthRequest):
    return update_player_hash(Auth.name, Auth.pwd)

@app.delete("/player/delete", response_model=dict)
def delete_player(id: int):
    return delete_player_by_id(id)

@app.get("/all_commanders", response_model=List[commander])
def all_commanders():
    return get_all_commanders()

@app.get("/commander/{id}", response_model=commander)
def commander_by_id(id: int):
    return get_commander_by_id(id)

@app.post("/commander/create", response_model=commander)
def create_new_commander(commander: str):
    return create_commander(commander)

@app.delete("/commander/delete", response_model=dict)
def delete_commander(id: int):
    return delete_commander_by_id(id)   

@app.get("/all_partides", response_model=List[partida])
def all_partides():
    return get_all_partides()

@app.get("/partida/{id}", response_model=partida)
def partida_by_id(id: int):
    return get_partida_by_id(id)

@app.post("/partida/create", response_model=partida)
def create_new_partida(winner: int = None):
    return create_partida(winner)

@app.put("/partida/update_winner", response_model=partida)
def update_partida(id: int, winner: int):
    return update_partida_winner(id, winner)

@app.delete("/partida/delete", response_model=dict)
def delete_partida(id: int):
    return delete_partida_by_id(id)

@app.get("/all_player_commanders", response_model=List[player_commander])
def all_player_commanders():
    return get_all_player_commanders()  
@app.get("/player_commander/{id}", response_model=player_commander)
def player_commander_by_id(id: int):    
    return get_player_commander_by_id(id)
@app.post("/player_commander/create", response_model=player_commander)
def create_new_player_commander(id_player: int, id_commander: int, id_partida: int):
    return create_player_commander(id_player, id_commander, id_partida)
@app.delete("/player_commander/delete", response_model=dict)
def delete_player_commander(id: int):
    return delete_player_commander_by_id(id)   