from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AcaoInput(BaseModel):
    ticker: str
    quantidade: int
    preco: Optional[float] = None
    data: Optional[datetime] = None

class BuscarAcao(BaseModel):
    ticker: str