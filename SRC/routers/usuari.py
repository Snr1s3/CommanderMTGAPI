from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from ..models import *
from typing import List
import requests

url = 'http://localhost:8443'
def get_all_players() -> List[Usuari]:
    try:
        response = requests.get(f'{url}/all_users')
        if response.status_code == 200:
            users_data = response.json()
            return [Usuari(**u) for u in users_data]
        else:
            print(f"Error: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch users")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Login service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    

def get_player_by_id(id: int) -> Usuari:
    try:
        response = requests.get(f'{url}/user/{id}')
        if response.status_code == 200:
            users_data = response.json()
            return Usuari(**users_data)
        else:
            print(f"Error: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch users")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Login service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

def player_create(Create: CreateUser) -> Usuari:
    try:
        response = requests.post(f'{url}/user/create', json=Create.model_dump())
        if response.status_code == 200:
            users_data = response.json()
            return Usuari(**users_data)
        else:
            print(f"Error: {response.status_code}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch users")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Login service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

def player_authenticate(Auth: AuthRequest) -> Usuari:
    try:
        response = requests.post(f'{url}/user/authenticate/', json=Auth.model_dump())
        if response.status_code == 200:
            users_data = response.json()
            return Usuari(**users_data)
        else:
            print(f"Error: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch users")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Login service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

def player_update(Update: UpdateUsuari) -> Usuari:
    try:
        response = requests.put(f'{url}/user/update', json=Update.model_dump())
        if response.status_code == 200:
            users_data = response.json()
            return Usuari(**users_data)
        else:
            print(f"Error: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch users")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Login service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

def player_delete(id: int) -> dict:
    try:
        response = requests.delete(f'{url}/user/delete?id={id}')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch users")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Login service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")