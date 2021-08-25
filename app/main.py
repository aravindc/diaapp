from importlib import reload
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html,)
from fastapi.openapi.utils import get_openapi
from tortoise.contrib.fastapi import register_tortoise
from core.db import DB_CONFIG
from routers import users, clients, food_carb, food_log, carb_ratio, bg_log
import uvicorn
from dynaconf import settings

settings.setenv('dev')

tags_metadata = [
    {
        "name": "Users",
        "description": "Admin users of DiaDiary"
    },
    {
        "name": "DiabUsers",
        "description": "Diabetes users of DiaDiary"
    }
]

# app = FastAPI(title=settings.APP_NAME)
app = FastAPI(docs_url=None, redoc_url=None, openapi_tags=tags_metadata, title='DiaDiary', description='Diabetes Diary', version='0.0.1')

app.add_middleware(
    HTTPSRedirectMiddleware,
    )
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["localhost"],
    )
app.add_middleware(
    GZipMiddleware, minimum_size=1000,
    )

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


"""Mount static files from /static folder."""
app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Load swagger js and css from local webserver."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/css/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """Load redoc.js from local webserver."""
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/js/redoc.standalone.js",
    )


def custom_openapi():
    """Customize OpenAPI for this project."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="DiaDiary APIs",
        version="1.0.0",
        description="Custom OpenAPI schema for DiaDiary",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/img/diadiary.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, workers=5, reload=True)