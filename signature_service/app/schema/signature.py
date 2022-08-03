from typing import Union
from pydantic import BaseModel


class Transaction(BaseModel):
    pdfPassword: Union[str, None] = None
    pdf: Union[str, None] = None
    reqRefNo: str
    signature: Union[str] = None

    class Config:
        schema_extra = {
            'example': {
                'pdfPassword': None,
                'pdf': '',
                'reqRefNo': '1659405914',
                'signature': None
            }
        }
