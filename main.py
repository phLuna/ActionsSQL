from toolbox.db import inserir_acao, buscar_acao, listar_acoes, excluir_acao

from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Rotas
app = FastAPI()

@app.post("/acoes/")
def adicionar_acao(ticker: str, quantidade: int):
    return inserir_acao(ticker, quantidade)

@app.get("/acoes/")
def listar_acoes():
    return listar_acoes()

@app.get("/acoes/{ticker}")
def buscar_acao(ticker: str):
    resultado = buscar_acao(ticker)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return resultado

@app.delete("/acoes/{ticker}")
def excluir_acao(ticker: str):
    sucesso = excluir_acao(ticker)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return {"mensagem": f"Ação '{ticker}' excluída com sucesso."}