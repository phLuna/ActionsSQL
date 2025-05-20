from toolbox.functions import inserir_acao, procurar_acao, ver_acoes, deletar_acao
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from datetime import datetime

from toolbox.models import AcaoInput
from toolbox.functions import obter_preco_atual, pesquisar_acao

# Rotas
app = FastAPI()

#Método para enviar ações.
@app.post("/acoes/")
def adicionar_acao(entrada: AcaoInput):
    """Adiciona ações no DB."""
    ticker       =   entrada.ticker
    quantidade   =   entrada.quantidade
    preco        =   entrada.preco
    data         =   entrada.data

    if preco == 0:
        preco = obter_preco_atual(ticker)
    return inserir_acao(ticker, quantidade, preco, data)

#Método para listar todas as ações do DB.
@app.get("/acoes/")
def listar_acoes():
    """Exibe todas as ações no DB."""
    return ver_acoes()

#Método para pesquisar suas ações no DB.
@app.get("/acoes/{ticker}")
def buscar_acao(ticker: str):
    """Busca uma ação específica no DB."""
    resultado = procurar_acao(ticker)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return resultado

#Método para excluir ações do DB.
@app.delete("/acoes/{ticker}")
def excluir_acao(ticker: str):
    """Exclui uma ação no DB."""
    sucesso = deletar_acao(ticker)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return {"mensagem": f"Ação '{ticker}' excluída com sucesso."}

@app.get("/pesquisar-acoes/")
def pesquisar(nome: str = Query(..., description="Parte do nome da empresa ou ticker."), limite: int = 5):
    """Busca ações pelo nome ou parte
    do ticker no Yahoo Finance."""
    resultados = pesquisar_acao(nome, limite)
    if not resultados:
        return {"mensagem": "Nenhum resultado encontrado"}
    return resultados