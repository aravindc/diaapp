from typing import Optional
from tortoise import fields, models
from werkzeug.security import generate_password_hash, check_password_hash
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum
from .users import Users

class FoodQtyType(str, Enum):
    g = 'g'
    kg = 'kg'
    l = 'l'
    ml = 'ml'
    nos = 'nos'

class Food_Carb(models.Model):
    id = fields.UUIDField(auto_generate=True, pk=True)
    food_name_id = fields.CharField(max_length=50, index=True, Optional=True)
    user_id = fields.UUIDField(required=True)
    food_name = fields.CharField(max_length=255)
    food_image_url = fields.CharField(max_length=1024)
    food_qty_type = fields.CharEnumField(FoodQtyType)
    food_qty = fields.DecimalField(max_digits=10, decimal_places=2)
    carb_count = fields.DecimalField(max_digits=10, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)

Food_Carb_Pydantic = pydantic_model_creator(Food_Carb, name="Food_Carb")
Food_Carb_In_Pydantic = pydantic_model_creator(Food_Carb, name="Food_Carb_In", exclude=["id", "created_at"])