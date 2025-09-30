from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date
import requests

from .models.commander import *
from .models.usuari_commander import *
from .models.partida import *


from .client import *

from .routers.commander import *
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


@app.get("/", tags=["root"])
async def root():
    return {"message": "Commander MTG API"}

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}


@app.get("/", response_model=str)
def root():
    return "API de Turnonauta operativa"
