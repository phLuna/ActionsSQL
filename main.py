from toolbox.db import inserir_acao, procurar_acao, ver_acoes, deletar_acao
from fastapi import FastAPI, HTTPException

# Rotas
app = FastAPI()

@app.post("/acoes/")
def adicionar_acao(ticker: str, quantidade: int):
    return inserir_acao(ticker, quantidade)

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