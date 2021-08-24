from importlib import reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from core.db import DB_CONFIG
from routers import users, clients, food_carb, food_log, carb_ratio, bg_log
import uvicorn
from dynaconf import settings

settings.setenv('dev')

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
app.include_router(food_log.router)
app.include_router(carb_ratio.router)
app.include_router(bg_log.router)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, workers=5, reload=True)