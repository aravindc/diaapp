from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from models.bg_log import BG_Log, BG_Log_Pydantic, BG_Log_In_Pydantic
from models.clients import Clients, Client_Pydantic
from models.users import Users, User_Pydantic
from models.status import Status
from routers.users import get_current_user

router = APIRouter()

@router.get("/bglog", response_model=List[BG_Log_Pydantic], tags=["BG Log"],
            dependencies=[Depends(get_current_user)])
async def get_bg_logs():
    return await BG_Log_Pydantic.from_queryset(BG_Log.all())

@router.post("/bglog", response_model=BG_Log_Pydantic, tags=["BG Log"],
             dependencies=[Depends(get_current_user)])
async def create_bg_log(bg_log: BG_Log_In_Pydantic):
    
    # user = await User_Pydantic.from_queryset(Users.filter(id=bg_log.user_id))
    user = await User_Pydantic.from_queryset_single(Users.get(id=bg_log.user_id))
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    client = await Client_Pydantic.from_queryset(Clients.filter(id=bg_log.client_id))
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    bglog_obj = await BG_Log.create(**bg_log.dict(exclude_unset=True))
    return await BG_Log_Pydantic.from_tortoise_orm(bglog_obj)