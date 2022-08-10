import logging
from fastapi import FastAPI
from mangum import Mangum
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api import signature

app = FastAPI(
    version='1.0.0',
    docs_url='/api/base64/docs',
    redoc_url='/api/base64/redoc',
    openapi_url='/api/base64/openapi.json',
)

origins = [
    "https://validate-stg.exkasan.com/",
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log = logging.getLogger("uvicorn")
handler = Mangum(app)

description = """
SERVICE ENCODING BASE64. 🚀

## APIs

You can **read items each API**.

You will be able to:

***prefix /api/base64**
"""

app.include_router(
    signature.router,
    prefix='/signature',
    tags=['SIGNATURE'],
)


@app.get('/', tags=['Index Base64'])
async def index():
    return HTMLResponse(
        """
        <h2>service encoding base64.
        """
    )


def custom_openapi():
    """
    docs description API
    :return:
        -> func
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SERVICE API BASE64",
        version="1.0.0",
        description=description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event("startup")
async def startup_event():
    """Start up event for FastAPI application."""
    log.info("Starting up server base64")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for FastAPI application."""
    with open("log.txt", mode="a") as create_log:
        create_log.write("Application shutdown server base64")
    log.info("Shutting down...")
