from typing import List, Union
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
import jwt
from datetime import timedelta, datetime
from models.users import Users, User_Pydantic, UserIn_Pydantic, UserOut_Pydantic, UserLogin_Pydantic
from models.status import Status
from werkzeug.security import generate_password_hash, check_password_hash
from dynaconf import settings

router = APIRouter()

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """Method to create a JWT access token

    Args:
        data (dict): [description]
        expires_delta (timedelta, optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    secret_key = settings.SECRET_KEY
    algorithm = "HS256"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

@router.get("/users", response_model=List[UserOut_Pydantic], tags=["Users"])
async def get_users():
    """List of all users

    Returns:
        List[UserOut_Pydantic]: Array of users
    """
    return await UserOut_Pydantic.from_queryset(Users.all())


@router.get(
    "/users/active", tags=["Users"], response_model=Union[List[UserOut_Pydantic], Status], responses={404: {"model": HTTPNotFoundError}}
)
async def get_active_users():
    """List of active users

    Returns:
        List[UserOut_Pydantic]: Array of Active users
    """
    print('get_active_users')
    users_obj = await Users.filter(is_active=True)
    if len(users_obj) == 0:
        return Status(message="No active users")
    return await UserOut_Pydantic.from_queryset(Users.filter(is_active=True))


@router.post("/users", response_model=UserOut_Pydantic, tags=["Users"])
async def create_user(user: UserIn_Pydantic):
    """Create a new user

    Args:
        user (UserIn_Pydantic): UserIn_Pydantic object

    Returns:
        [UserOut_Pydantic]: UserOut_Pydantic object
    """
    user.hashed_password = generate_password_hash(user.hashed_password)
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await UserOut_Pydantic.from_queryset(user_obj)


@router.get(
    "/user/{user_id}", tags=["Users"], response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.put(
    "/user/{user_id}", tags=["Users"], response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.delete("/user/{user_id}", tags=["Users"], response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: UUID):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")

@router.post('/login/', tags=["Users"])
async def login_user(user: UserLogin_Pydantic):
    db_user = await User_Pydantic.from_queryset_single(Users.get(email=user.email))
    if not db_user:
        raise HTTPException(status_code=400, detail='Username or password incorrect')
    if not check_password_hash(db_user.hashed_password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Username or password incorrect') 
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # return Status(message=f"Login Successful")
    return {"access_token": access_token, "token_type": "Bearer"}