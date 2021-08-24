from datetime import datetime
from models.food_carb import Food_Carb
from models.status import Status

import pytz

class Common_Utils:
    def valdate_time(time):
        try:
            print(time)
            timex = datetime.strptime(time, '%H:%M:%S')
            return time
        except ValueError:
            return Status(message=f"Invalid Time {time} entered")
    
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