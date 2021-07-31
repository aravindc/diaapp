from tortoise import fields, models
from werkzeug.security import generate_password_hash, check_password_hash
from tortoise.contrib.pydantic import pydantic_model_creator

class Users(models.Model):
    id = fields.UUIDField(auto_generate=True, pk=True)
    email = fields.TextField()
    hashed_password = fields.CharField(max_length=128, null=True)
    is_active = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
        
User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude=["id", "created_at"])
UserOut_Pydantic = pydantic_model_creator(Users, name="UserOut", exclude=["hashed_password"])
UserLogin_Pydantic = pydantic_model_creator(Users, name="UserLogin", exclude=["id", "created_at", "is_active"])