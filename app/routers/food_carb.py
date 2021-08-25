from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime
from models.food_carb import Food_Carb, Food_Carb_Pydantic, Food_Carb_In_Pydantic
from models.users import Users, User_Pydantic
from models.status import Status
from dynaconf import settings

router = APIRouter()

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

def generate_name(input_str: str) -> str:
    temp_str = input_str.split(' ')
    output_str = ''
    for x in temp_str:
        output_str += x[:4].lower() + ' '
    output_str = output_str.strip().replace(' ','-')
    return output_str


@router.get("/foodcarb", response_model=List[Food_Carb_Pydantic], tags=["Food Carb"])
async def get_food_carbs():
    return await Food_Carb_Pydantic.from_queryset(Food_Carb.all())

@router.post("/foodcarb", response_model=Food_Carb_Pydantic, tags=["Food Carb"])
async def create_food_carb(foodcarb: Food_Carb_In_Pydantic):
    user = await User_Pydantic.from_queryset(Users.filter(id=foodcarb.user_id))
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    foodcarb.food_name_id = generate_name(foodcarb.food_name)
    foodcarb_id = await Food_Carb_Pydantic.from_queryset(Food_Carb.filter(food_name_id=foodcarb.food_name_id))
    if len(foodcarb_id) > 0:
        raise HTTPException(status_code=409, detail="Food name already exists")
    foodcarb_obj = await Food_Carb.create(**foodcarb.dict(exclude_unset=True))
    return await Food_Carb_Pydantic.from_tortoise_orm(foodcarb_obj)

@router.delete("/foodcarb/{foodcarb_id}", tags=["Food Carb"], response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_food_carb(foodcarb_id: UUID):
    deleted_count = await Food_Carb.filter(id=foodcarb_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Food Carb {foodcarb_id} not found")
    return Status(message=f"Deleted food carb {foodcarb_id}")
