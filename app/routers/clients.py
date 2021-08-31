from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime
from dynaconf import settings

from models.clients import Clients, ClientIn_Pydantic, Client_Pydantic
from models.status import Status
from routers.users import get_current_user

router = APIRouter()

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise


@router.get("/clients", response_model=List[Client_Pydantic], tags=["Clients"], dependencies=[Depends(get_current_user)])
async def get_clients():
    return await Client_Pydantic.from_queryset(Clients.all())

@router.post("/clients", response_model=Client_Pydantic, tags=["Clients"],
             dependencies=[Depends(get_current_user)])
async def create_client(client: ClientIn_Pydantic):
    existing_client = await Client_Pydantic.from_queryset(Clients.filter(client_name=client.client_name))
    if len(existing_client) > 0:
        raise HTTPException(status_code=409, detail="Client already exists")
    client_obj = await Clients.create(**client.dict(exclude_unset=True))
    return await Client_Pydantic.from_tortoise_orm(client_obj)


@router.get(
    "/client/{client_id}", tags=["Clients"], response_model=Client_Pydantic, responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)]
)
async def get_client(client_id: int):
    return await Client_Pydantic.from_queryset_single(Clients.get(id=client_id))


@router.put(
    "/client/{client_id}", tags=["Clients"], response_model=Client_Pydantic, responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)]
)
async def update_client(client_id: int, client: ClientIn_Pydantic):
    await Clients.filter(id=client_id).update(**client.dict(exclude_unset=True))
    return await Client_Pydantic.from_queryset_single(Clients.get(id=client_id))


@router.delete("/client/{client_id}", tags=["Clients"], response_model=Status, responses={404: {"model": HTTPNotFoundError}},
               dependencies=[Depends(get_current_user)])
async def delete_client(client_id: UUID):
    deleted_count = await Clients.filter(id=client_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {client_id} not found")
    return Status(message=f"Deleted client {client_id}")
