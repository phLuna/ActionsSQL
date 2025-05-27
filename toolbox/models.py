from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AcaoInput(BaseModel):
    ticker:     str
    quantidade: int
    tipo:       Optional[str]       = None
    preco:      Optional[float]     = None
    data:       Optional[datetime]  = None

class BuscarAcao(BaseModel):
    ticker: str

class MetaInput(BaseModel):
    ticker:     str
    porcentagem: float