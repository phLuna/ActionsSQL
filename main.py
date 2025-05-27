from toolbox.functions import inserir_acao, procurar_acao, ver_acoes, deletar_acao
from fastapi import FastAPI, HTTPException, Query

from toolbox.models import AcaoInput, MetaInput
from toolbox.functions import obter_preco_atual, pesquisar_acao, adicionar_meta, comparar_alocacao, deletar_meta

# Rotas
app = FastAPI()

#Método para enviar ações.
@app.post("/acoes/")
def adicionar_acao(entrada: AcaoInput):
    """Adiciona ações no DB."""

    ticker       =   entrada.ticker
    quantidade   =   entrada.quantidade
    tipo         =   entrada.tipo
    preco        =   entrada.preco
    data         =   entrada.data

    if not preco or preco <= 0:
        preco = obter_preco_atual(ticker)
    response = inserir_acao(ticker, quantidade, tipo, preco, data)
    return response

#Método para definir metas para as ações no DB.
@app.post("/metas/")
def definir_meta(entrada: MetaInput):
    """Adiciona uma meta de quantia de tal ação na carteira."""

    ticker = entrada.ticker
    porcentagem = entrada.porcentagem

    response = adicionar_meta(ticker, porcentagem)
    return response

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

#Método para ver todas as metas e compará-las no DB.
@app.get("/metas/")
def comparar_metas():
    response = comparar_alocacao()
    return response

#Método para pesquisar ações no Yahoo Finance.
@app.get("/pesquisar-acoes/")
def pesquisar(nome: str = Query(..., description="Parte do nome da empresa ou ticker."), limite: int = 5):
    """Busca ações pelo nome ou parte
    do ticker no Yahoo Finance."""
    resultados = pesquisar_acao(nome, limite)
    if not resultados:
        return {"mensagem": "Nenhum resultado encontrado"}
    return resultados

#Método para excluir ações do DB.
@app.delete("/acoes/{ticker}")
def excluir_acao(ticker: str, quantidade: int):
    """Exclui uma ação no DB."""
    sucesso = deletar_acao(ticker, quantidade)
    if sucesso.startswith("Erro") or "não encontrada" in sucesso:
        raise HTTPException(status_code=404, detail=sucesso)
    return {"mensagem": sucesso}

#Método para excluir a meta de uma ação no DB.
@app.delete("/meta-alocacao/{ticker}")
def excluir_meta(ticker: str):
    sucesso = deletar_meta(ticker)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Meta de alocação não encontrada.")
    return {"mensagem": f"Meta de alocação para '{ticker}' excluída com sucesso."}