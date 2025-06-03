from fastapi import APIRouter, HTTPException, Query
from functions import inserir_acao, ver_acoes, procurar_acao, deletar_acao
from src.integrations.yahoof import YahooAPI
from src.models.inputs import AcaoInput

router = APIRouter()

#Método para enviar ações.
@router.post('/acoes/', tags=['Ações'])
def adicionar_acao(entrada: AcaoInput):
    """Adiciona ações no DB."""

    ticker       =   entrada.ticker
    quantidade   =   entrada.quantidade
    tipo         =   entrada.tipo
    preco        =   entrada.preco
    data         =   entrada.data

    if not preco or preco <= 0:
        preco = YahooAPI.preco_atual(ticker)
    response = inserir_acao(ticker, quantidade, tipo, preco, data)
    return response

#Método para listar todas as ações do DB.
@router.get('/acoes/', tags=['Ações'])
def listar_acoes():
    """Exibe todas as ações no DB."""
    return ver_acoes()

#Método para pesquisar suas ações no DB.
@router.get('/acoes/{ticker}', tags=['Ações'])
def buscar_acao(ticker: str):
    """Busca uma ação específica no DB."""
    resultado = procurar_acao(ticker)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return resultado

#Método para pesquisar ações no Yahoo Finance.
@router.get('/pesquisar-acoes/', tags=['Ações'])
def pesquisar(nome: str = Query(..., description="Parte do nome da empresa ou ticker."), limite: int = 5):
    """Busca ações pelo nome ou parte
    do ticker no Yahoo Finance."""
    resultados = YahooAPI.pesquisar_acao(nome, limite)
    if not resultados:
        return {"mensagem": "Nenhum resultado encontrado"}
    return resultados

#Método para excluir ações do DB.
@router.delete('/acoes/{ticker}', tags=['Ações'])
def excluir_acao(ticker: str, quantidade: int):
    """Exclui uma ação no DB."""
    sucesso = deletar_acao(ticker, quantidade)
    if sucesso.startswith("Erro") or "não encontrada" in sucesso:
        raise HTTPException(status_code=404, detail=sucesso)
    return {"mensagem": sucesso}