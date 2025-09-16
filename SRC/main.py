from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date

from .models import *

from .client import *

from .routers.player import *
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

@app.delete("/player/{id}", response_model=dict)
def delete_player(id: int):
    return delete_player_by_id(id)
@app.post("/player/", response_model=player)
def create_new_player(p_name: str, pwd : str):
    return create_player(p_name, pwd)
@app.post("/player/authenticate/", response_model=player)
def authenticate(name: str, pwd: str):
    return authenticate_player(name, pwd)