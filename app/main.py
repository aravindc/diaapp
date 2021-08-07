# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.core.config import settings


# def get_application():
#     _app = FastAPI(title=settings.PROJECT_NAME)

#     _app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

#     return _app


# app = get_application()


from importlib import reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from core.db import DB_CONFIG
from routers import users, clients, food_carb
import uvicorn
from dynaconf import settings

settings.setenv('dev')

print(settings.DATABASE_URL)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=DB_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)

app.include_router(users.router)
app.include_router(clients.router)
app.include_router(food_carb.router)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, workers=5, reload=True)