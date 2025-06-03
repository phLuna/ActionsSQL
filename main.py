from fastapi import FastAPI, HTTPException

from toolbox.functions import adicionar_meta, comparar_alocacao, deletar_meta

from src.models.base import Base
from src.models.inputs import MetaInput
from src.integrations.sqlalchemy import SQLAlchemy

from src.rotes.acoes import router as acoes_router

engine = SQLAlchemy.engine  # aqui apenas referencia o engine já criado
Base.metadata.create_all(bind=engine)

# Rotas
app = FastAPI()

#Método para incluir as rotas de src.rotes.acoes
app.include_router(acoes_router)

#Método para definir metas para as ações no DB.
@app.post("/metas/")
def definir_meta(entrada: MetaInput):
    """Adiciona uma meta de quantia de tal ação na carteira."""

    ticker = entrada.ticker
    porcentagem = entrada.porcentagem

    response = adicionar_meta(ticker, porcentagem)
    return response

#Método para excluir a meta de uma ação no DB.
@app.delete("/meta-alocacao/{ticker}")
def excluir_meta(ticker: str):
    sucesso = deletar_meta(ticker)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Meta de alocação não encontrada.")
    return {"mensagem": f"Meta de alocação para '{ticker}' excluída com sucesso."}

#Método para ver todas as metas e compará-las no DB.
@app.get("/metas/")
def comparar_metas():
    response = comparar_alocacao()
    return response