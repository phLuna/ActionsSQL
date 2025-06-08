from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class AcaoInput(BaseModel):
    ticker:     str
    quantidade: int
    tipo:       Optional[str]       = None
    preco:      Optional[float]     = None
    data:       Optional[datetime]  = None

class BuscarAcaoInput(BaseModel):
    ticker: str

class MetaInput(BaseModel):
    ticker:     str
    porcentagem: float

class CreateUser(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=6, max_length=128)