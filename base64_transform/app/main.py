import httpx
import os
import random
import hashlib
import hmac
import base64
from typing import Union, Optional
from fastapi import FastAPI, UploadFile, HTTPException, status, Body
from mangum import Mangum
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    version='1.0.0',
    docs_url='/base64/docs',
    redoc_url='/base64/redoc',
    openapi_url='/base64/openapi.json',
)

origins = [
    "http://localhost:80",
    "http://localhost:3000",
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


@app.get('/')
async def index():
    return HTMLResponse(
        """
        <h2> Transform base64!
        """
    )


@app.post(
    "/files/pdf/base64",
    summary='Encode base64',
    description='encode file any to base64.',
)
async def create_file(
        file: Union[UploadFile, None] = None
):
    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='please upload your file.')
    encoded_string = base64.b64encode(file.file.read())
    return {
        'file_name': f'{file.filename}',
        "file_size": f'{file.spool_max_size}',
        "fileb_content_type": file.content_type,
        'base64': encoded_string
    }


def random_string(num: int):
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    texts = ""
    for i in range(num):
        text = random.choice(possible)
        texts += text
    return texts


def sign_string(key_b64, to_sign):
    key = base64.b64decode(key_b64)
    signed_hmac_sha256 = hmac.HMAC(key, to_sign.encode(), hashlib.sha256)
    digest = signed_hmac_sha256.digest()
    return base64.b64encode(digest).decode()


@app.post('/executed/exkasan')
async def executed_exkasan(payload: Optional[dict] = Body(None)):
    signature = payload.get('signature')
    url = "https://stamp-kong.exkasan.com/jds-rest/pdf/verify/all"
    payload = {
        "pdfPassword": None,
        "pdf": "",
        "reqRefNo": "1659405914"
    }
    headers = {
        'X-Signature': signature,
        'apikey': 'kGTptzcT#W5h9VQW',
        'Content-Type': 'application/json',
    }
    async with httpx.AsyncClient() as client:
        tasks = await client.post(url=url, json=payload, headers=headers)
    return tasks.json()
