from services.common_utils import Common_Utils
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException
from datetime import timedelta, datetime, time
from models.clients import Clients, Client_Pydantic
from models.carb_ratio import Carb_Ratio, Carb_Ratio_Pydantic, Carb_Ratio_In_Pydantic
from models.status import Status

router = APIRouter()

@router.get("/carbratio", response_model=List[Carb_Ratio_Pydantic], tags=["Carb Ratio"])
async def get_carb_ratios():
    # return await Carb_Ratio.all()
    return await Carb_Ratio_Pydantic.from_queryset(Carb_Ratio.all())

@router.post("/carbratio", response_model=Carb_Ratio_Pydantic, tags=["Carb Ratio"])
async def create_carb_ratio(carbratio: Carb_Ratio_In_Pydantic):
    client = await Client_Pydantic.from_queryset(Clients.filter(id=carbratio.client_id))
    if len(client) == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    if not (Common_Utils.validate_time(carbratio.start_time)):
        raise HTTPException(status_code=422, detail="Invalid Start time")
    if not (Common_Utils.validate_time(carbratio.end_time)):
        raise HTTPException(status_code=422, detail="Invalid End time")
    carbratio_obj = await Carb_Ratio.create(**carbratio.dict(exclude_unset=True))
    return await Carb_Ratio_Pydantic.from_tortoise_orm(carbratio_obj)
