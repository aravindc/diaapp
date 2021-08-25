from typing import List, Union
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import timedelta, datetime
from models.users import Users, User_Pydantic, UserIn_Pydantic, UserOut_Pydantic, UserLogin_Pydantic
from models.status import Status
from werkzeug.security import generate_password_hash, check_password_hash
from dynaconf import settings

router = APIRouter()

from tortoise.contrib.fastapi import HTTPNotFoundError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        u = Users().get_user_by_email(payload.get('sub'))
        db_user = await UserOut_Pydantic.from_queryset_single(u)
    except JWTError:
        raise credentials_exception
    return db_user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """Method to create a JWT access token

    Args:
        data (dict): [description]
        expires_delta (timedelta, optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    secret_key = settings.SECRET_KEY
    algorithm = settings.TOKEN_ALGORITHM
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

@router.get("/users", response_model=List[UserOut_Pydantic], tags=["Users"], dependencies=[Depends(get_current_user)])
async def get_users():
    """List of all users

    Returns:
        List[UserOut_Pydantic]: Array of users
    """
    return await UserOut_Pydantic.from_queryset(Users.all())


@router.get("/users/me", response_model=UserOut_Pydantic, tags=["Users"])
async def get_user(user: UserIn_Pydantic = Depends(get_current_user)):
    return user

@router.get(
    "/users/active", tags=["Users"], response_model=Union[List[UserOut_Pydantic], Status], responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)]
)
async def get_active_users():
    """List of active users

    Returns:
        List[UserOut_Pydantic]: Array of Active users
    """
    u = Users()
    users_obj = await u.get_active_users()
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
    existing_user = await User_Pydantic.from_queryset(Users.filter(email=user.email))
    if len(existing_user) > 0:
        raise HTTPException(status_code=404, detail="User already exists")
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await UserOut_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/user/{user_id}", tags=["Users"], response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)]
)
async def get_user(user_id: UUID):
    return await User_Pydantic.from_queryset_single(Users.get_user_by_id(user_id))


@router.put(
    "/user/{user_id}", tags=["Users"], response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)]
)
async def update_user(user_id: UUID, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.delete("/user/{user_id}", tags=["Users"], response_model=Status, responses={404: {"model": HTTPNotFoundError}},
               dependencies=[Depends(get_current_user)]
               )
async def delete_user(user_id: UUID):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")

@router.post('/token', tags=["Users"])
async def token(user: OAuth2PasswordRequestForm = Depends()):
    u = Users().get_user_by_email(user.username)
    db_user = await User_Pydantic.from_queryset_single(u)
    if not db_user:
        raise HTTPException(status_code=400, detail='Username or password incorrect', headers={"WWW-Authenticate": "Bearer"},)
    if not check_password_hash(db_user.hashed_password, user.password):
        raise HTTPException(status_code=400, detail='Username or password incorrect', headers={"WWW-Authenticate": "Bearer"},) 
    access_token_expires = timedelta(minutes=settings.TOKEN_EXPIRATION)
    access_token = create_access_token(
        data={"sub": db_user.email, "id": str(db_user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}

# @router.post('/login', tags=["Users"])
# async def login_user(user: UserLogin_Pydantic = Depends()):
#     u = Users()
#     db_user = await User_Pydantic.from_queryset_single(u.get_user_by_email(user.email))
#     if not db_user:
#         raise HTTPException(status_code=400, detail='Username or password incorrect')
#     if not check_password_hash(db_user.hashed_password, user.hashed_password):
#         raise HTTPException(status_code=400, detail='Username or password incorrect') 
#     access_token_expires = timedelta(minutes=15)
#     access_token = create_access_token(
#         data={"sub": user.email, "id": str(db_user.id)}, expires_delta=access_token_expires
#     )
#     # return Status(message=f"Login Successful")
#     return {"access_token": access_token, "token_type": "Bearer"}