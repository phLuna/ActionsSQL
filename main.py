from fastapi import FastAPI

from src.integrations.sqlalchemy import SQLAlchemy
from src.models.base import Base

from src.rotes.acoes import router as acoes_router
from src.rotes.metas import router as metas_router

engine = SQLAlchemy.engine  # aqui apenas referencia o engine já criado
Base.metadata.create_all(bind=engine)

# Rotas
app = FastAPI()

#Método para incluir as rotas de src.rotes.acoes
app.include_router(acoes_router)
app.include_router(metas_router)