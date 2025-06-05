from fastapi import APIRouter, HTTPException

from functions import adicionar_meta, deletar_meta, comparar_alocacao

from src.models.schemas import MetaInput

router = APIRouter(prefix='/metas', tags=['Metas'])

#Método para definir metas para as ações no DB.
@router.post("")
def definir_meta(entrada: MetaInput):
    """Adiciona uma meta de quantia de tal ação na carteira."""

    ticker = entrada.ticker
    porcentagem = entrada.porcentagem

    response = adicionar_meta(ticker, porcentagem)
    return response

#Método para excluir a meta de uma ação no DB.
@router.delete("/{ticker}")
def excluir_meta(ticker: str):
    sucesso = deletar_meta(ticker)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Meta de alocação não encontrada.")
    return {"mensagem": f"Meta de alocação para '{ticker}' excluída com sucesso."}

#Método para ver todas as metas e compará-las no DB.
@router.get("")
def comparar_metas():
    response = comparar_alocacao()
    return response