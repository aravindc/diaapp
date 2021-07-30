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


from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config.db import DB_CONFIG
from config.settings import Settings
import uvicorn

settings = Settings()
app = FastAPI(title=settings.APP_NAME)

print(DB_CONFIG)

register_tortoise(
    app,
    config=DB_CONFIG,
    generate_schemas=False,
)


if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)