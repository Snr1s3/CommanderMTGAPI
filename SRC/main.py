from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date
from .client import *
'''
from .routers.emparellaments import *
from .routers.estadistiques import *
from .routers.formats import *
from .routers.puntuacions import *
from .routers.rangs import *
from .routers.resultats import *
from .routers.rols import *
from .routers.rondes import *
from .routers.subscripcions import *
from .routers.tornejos import *
from .routers.usuaris import *
'''
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