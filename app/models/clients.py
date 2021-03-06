from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum

class DiabetesType(str, Enum):
    type1 = 'type1'
    type2 = 'type2'

class BgReadingType(str, Enum):
    mmolbyl = 'mmol/l'
    mgbydl = 'mg/dl'

class Clients(models.Model):
    id = fields.UUIDField(auto_generate=True, pk=True)
    client_name = fields.CharField(max_length=50)
    first_name = fields.TextField()
    last_name = fields.TextField()
    date_of_birth = fields.DateField()
    diabetes_type = fields.CharEnumField(DiabetesType)
    bg_reading_type = fields.CharEnumField(BgReadingType)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def get_client_by_name(self, client_name):
        return Clients.filter(client_name=client_name).first()
    
Client_Pydantic = pydantic_model_creator(Clients, name="Client")
ClientIn_Pydantic = pydantic_model_creator(Clients, name="ClientIn", exclude=["id", "created_at"])
