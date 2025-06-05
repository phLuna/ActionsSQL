from pydantic import BaseModel, EmailStr
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
    nome: str
    email: EmailStr
    senha: str

class UserLogin(BaseModel):
    email: EmailStr
    senha: str