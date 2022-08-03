from fastapi import FastAPI
from mangum import Mangum
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api import signature

app = FastAPI(
    version='1.0.0',
    docs_url='/v1/api/base64/docs',
    redoc_url='/v1/api/base64/redoc',
    openapi_url='/v1/api/base64/openapi.json',
)

origins = [
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
