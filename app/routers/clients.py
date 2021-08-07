from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
import jwt
from datetime import timedelta, datetime
from models.clients import Clients, ClientIn_Pydantic, Client_Pydantic
from models.status import Status
from werkzeug.security import generate_password_hash, check_password_hash
from dynaconf import settings

router = APIRouter()

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise


@router.get("/clients", response_model=List[Client_Pydantic], tags=["Clients"])
async def get_clients():
    return await Client_Pydantic.from_queryset(Clients.all())

@router.post("/clients", response_model=Client_Pydantic, tags=["Clients"])
async def create_client(client: ClientIn_Pydantic):
    client = await Client_Pydantic.from_queryset(Clients.filter(client_name=client.client_name))
    if len(client) > 0:
        raise HTTPException(status_code=409, detail="Client already exists")
    client_obj = await Clients.create(**client.dict(exclude_unset=True))
    return await Client_Pydantic.from_tortoise_orm(client_obj)


@router.get(
    "/client/{client_id}", tags=["Clients"], response_model=Client_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_client(client_id: int):
    return await Client_Pydantic.from_queryset_single(Clients.get(id=client_id))


@router.put(
    "/client/{client_id}", tags=["Clients"], response_model=Client_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_client(client_id: int, client: ClientIn_Pydantic):
    await Clients.filter(id=client_id).update(**client.dict(exclude_unset=True))
    return await Client_Pydantic.from_queryset_single(Clients.get(id=client_id))


@router.delete("/client/{client_id}", tags=["Clients"], response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_client(client_id: UUID):
    deleted_count = await Clients.filter(id=client_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {client_id} not found")
    return Status(message=f"Deleted client {client_id}")
