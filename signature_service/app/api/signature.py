import os
import hashlib
import hmac
import random
import httpx
import base64
from typing import Union
from fastapi import APIRouter, UploadFile, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from app.schema.signature import Transaction

router = APIRouter()


async def random_string(num: int):
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(possible) for i in range(num))


async def gen_x_signature(message, secret):
    signature_hash = hmac.new(bytes(secret, 'utf-8'), bytes(message, 'utf-8'), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(signature_hash)
    return signature.decode('ascii')


async def gen_x_signature_variable(payload: Transaction):
    cu = os.getenv('CU')
    sc = os.getenv('SC')
    nonce = await random_string(32)
    xs = await gen_x_signature(cu + nonce, sc)
    signature = f'{cu} {nonce} {xs}'
    if payload.signature is None or payload.signature == '':
        item_model = jsonable_encoder(payload)
        item_model['signature'] = signature
        item_store = Transaction(**item_model)
        return item_store


@router.post(
    '/file/pdf/base64',
    summary='Encode base64',
    description='encode file any to base64.',
    status_code=status.HTTP_200_OK
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
        'file_content_type': file.content_type,
        'base64_enc': encoded_string
    }


@router.post('/verify/exkasan', status_code=status.HTTP_200_OK)
async def verify_exkasan(payload: Transaction = Depends(gen_x_signature_variable)):
    headers = {
        'X-Signature': payload.signature,
        'apikey': os.getenv('APIKEY'),
        'Content-Type': 'application/json',
    }
    payload_etc = jsonable_encoder(payload)
    url = "https://stamp-kong.exkasan.com/jds-rest/pdf/verify/all"
    async with httpx.AsyncClient() as client:
        tasks = await client.post(url=url, json=payload_etc, headers=headers)
    return tasks.json()
