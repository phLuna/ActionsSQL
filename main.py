from toolbox.db import inserir_acao, procurar_acao, ver_acoes, deletar_acao
from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime

from toolbox.models import AcaoInput
from toolbox.db import obter_preco_atual

# Rotas
app = FastAPI()

@app.post("/acoes/")
def adicionar_acao(entrada: AcaoInput):
    ticker       =   entrada.ticker
    quantidade   =   entrada.quantidade
    preco        =   entrada.preco
    data         =   entrada.data

    if preco == 0:
        preco = obter_preco_atual(ticker)
    return inserir_acao(ticker, quantidade, preco, data)

@app.get("/acoes/")
def listar_acoes():
    return ver_acoes()

@app.get("/acoes/{ticker}")
def buscar_acao(ticker: str):
    resultado = procurar_acao(ticker)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return resultado

@app.delete("/acoes/{ticker}")
def excluir_acao(ticker: str):
    sucesso = deletar_acao(ticker)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return {"mensagem": f"Ação '{ticker}' excluída com sucesso."}