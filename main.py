from fastapi import FastAPI

from src.integrations.sqlalchemy import SQLAlchemy
from src.models.base import Base

from src.rotes.acoes import router as acoes_router
from src.rotes.metas import router as metas_router
from src.rotes.auth import router as auth_router

engine = SQLAlchemy.engine  # aqui apenas referencia o engine já criado
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Carteira de Ações.",
    description="API para controle de ações, metas de alocação e integração com Yahoo Finance.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

#Método para incluir as rotas de src.rotes
app.include_router(auth_router)
app.include_router(acoes_router)
app.include_router(metas_router)