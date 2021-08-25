from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException
from datetime import timedelta, datetime
from models.food_log import Food_Log, Food_Log_Pydantic, Food_Log_In_Pydantic
from models.users import Users, User_Pydantic
from models.clients import Clients, Client_Pydantic
from models.food_carb import Food_Carb, Food_Carb_Pydantic
from models.status import Status
from services.common_utils import Common_Utils
import pytz

router = APIRouter()

@router.get("/foodlog", response_model=List[Food_Log_Pydantic], tags=["Food Log"])
async def get_food_logs():
    return await Food_Log_Pydantic.from_queryset(Food_Log.all())

@router.post("/foodlog", response_model=Food_Log_Pydantic, tags=["Food Log"])
async def create_food_log(food_log: Food_Log_In_Pydantic):
    user = await User_Pydantic.from_queryset(Users.filter(id=food_log.user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    client = await Client_Pydantic.from_queryset(Clients.filter(id=food_log.client_id))
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    food_carb = await Food_Carb_Pydantic.from_queryset(Food_Carb.filter(id=food_log.food_carb_id))
    if food_carb is None:
        raise HTTPException(status_code=404, detail="Food Carb not found")
    food_log.entry_datetime = Common_Utils.get_utc_datetime(food_log.entry_datetime, user[0].user_tz)
    food_log.carb_count = Common_Utils.get_food_carb_count(food_carb, food_log.food_qty)
    foodlog_obj = await Food_Log.create(**food_log.dict(exclude_unset=True))
    return await Food_Log_Pydantic.from_tortoise_orm(foodlog_obj)