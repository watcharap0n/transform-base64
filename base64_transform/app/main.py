import base64
from typing import Union
from fastapi import FastAPI, UploadFile, HTTPException, status
from mangum import Mangum
from fastapi.responses import HTMLResponse

app = FastAPI(
    version='1.0.0',
    docs_url='/base64/docs',
    redoc_url='/base64/redoc',
    openapi_url='/base64/openapi.json',
)

handler = Mangum(app)


@app.get('/')
async def index():
    return HTMLResponse(
        """
        <h2> Transform base64!
        """
    )


@app.post("/files/pdf/base64", summary='Response file to base64')
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