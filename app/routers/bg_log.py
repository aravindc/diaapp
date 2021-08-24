from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from models.bg_log import BG_Log, BG_Log_Pydantic
from models.clients import Clients, Client_Pydantic
from models.users import Users, User_Pydantic
from models.status import Status

router = APIRouter()

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

@router.get("/bglog", response_model=List[BG_Log_Pydantic], tags=["BG Log"])
async def get_bg_logs():
    return await BG_Log_Pydantic.from_queryset(BG_Log.all())

@router.post("/bglog", response_model=BG_Log_Pydantic, tags=["BG Log"])
async def create_bg_log(bg_log: BG_Log_Pydantic):
    u = Users()
    c = Clients()
    user_obj = u.get_user_by_id(bg_log.user_id)
    if not user_obj:
        raise HTTPNotFoundError(status_code=404, detail="User does not exists")
    client_obj = c.get_client_by_id(bg_log.client_id)
    if not client_obj:
        raise HTTPNotFoundError(status_code=404, detail="Client does not exists")
    bglog_obj = await BG_Log.create(**bg_log.dict(exclude_unset=True))
    return await BG_Log_Pydantic.from_tortoise_orm(bglog_obj)