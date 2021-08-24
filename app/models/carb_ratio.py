from typing import Optional
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import validator, ValidationError
from enum import Enum
from services.common_utils import Common_Utils

class RatioType(str, Enum):
    time_based = 'time_range'
    same = 'same'

class Carb_Ratio(models.Model):
    id = fields.UUIDField(pk=True, auto_generated=True)
    client_id = fields.UUIDField()
    ratio_type = fields.CharEnumField(RatioType)
    carb_ratio = fields.DecimalField(max_digits=10, decimal_places=2)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    insulin_sensitivity = fields.DecimalField(max_digits=10, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)

    
Carb_Ratio_Pydantic = pydantic_model_creator(Carb_Ratio, name="Carb_Ratio")
Carb_Ratio_In_Pydantic = pydantic_model_creator(Carb_Ratio, name="Carb_Ratio_In", exclude=["id", "created_at"])