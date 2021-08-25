from typing import Optional
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import validator, ValidationError
from enum import Enum

class InsulinType(str, Enum):
    rapid_insulin_food = "rapid_insulin_food"
    rapid_insulin_correction = "rapid_insulin_correction"
    long_acting_insulin = "long_acting_insulin"
    
class BG_Log(models.Model):
    id = fields.UUIDField(pk=True, auto_generated=True)
    user_id = fields.UUIDField(required=True)
    client_id = fields.UUIDField(required=True)
    entry_datetime = fields.DatetimeField(required=True)
    bg_level = fields.DecimalField(required=True, max_digits=10, decimal_places=2)
    insulin_qty = fields.DecimalField(required=True, max_digits=10, decimal_places=2)
    insulin_type = fields.CharEnumField(InsulinType, required=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
BG_Log_Pydantic = pydantic_model_creator(BG_Log, name="BG_Log")
BG_Log_In_Pydantic = pydantic_model_creator(BG_Log, name="BG_Log_In", exclude=["id", "created_at"])