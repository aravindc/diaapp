from typing import Optional
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import validator, ValidationError
from enum import Enum

class FoodType(str, Enum):
    breakfast = 'breakfast'
    lunch = 'lunch'
    dinner = 'dinner'
    snack = 'snack'
    
class Food_Log(models.Model):
    id = fields.UUIDField(auto_generated=True, pk=True)
    entry_datetime = fields.DatetimeField()
    food_type = fields.CharEnumField(FoodType)
    food_carb_id = fields.UUIDField()
    user_id = fields.UUIDField()
    client_id = fields.UUIDField()
    food_qty = fields.DecimalField(max_digits=10, decimal_places=2)
    carb_count = fields.DecimalField(max_digits=10, decimal_places=2, Optional=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = 'food_log'
    
Food_Log_Pydantic = pydantic_model_creator(Food_Log, name="Food_Log")
Food_Log_In_Pydantic = pydantic_model_creator(Food_Log, name="Food_Log_In", exclude=['id', 'created_at'])
