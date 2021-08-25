from datetime import datetime
from models.food_carb import Food_Carb
from models.status import Status

import pytz
from datetime import time

class Common_Utils:
    
    def str_to_time(input_str: str):
        if isinstance(input_str, time):
            return input_str
        return time(hour=int(input_str[:2]), minute=int(input_str[3:5]), second=int(input_str[6:8]))
    
    def validate_time(time):
        try:
            timex = datetime.strptime(time, '%H:%M:%S')
        except ValueError:
            return False
        return True
    
    def get_utc_datetime(inputDateTime: datetime, timeZone: str):
        if timeZone == 'UTC':
            return inputDateTime
        else:
            local = pytz.timezone(timeZone)
            local_dt = local.localize(inputDateTime, is_dst=None)
            return inputDateTime.astimezone(pytz.utc)
        
    def get_utz_datetime(inputDateTime: datetime, timeZone: str):
        if timeZone == 'UTC':
            return inputDateTime
        else:
            return inputDateTime.astimezone(timeZone)
    
    def get_food_carb_count(food_carb: Food_Carb, food_qty: float):
        return (food_qty / food_carb[0].food_qty) * food_carb[0].carb_count