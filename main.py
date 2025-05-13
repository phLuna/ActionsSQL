from toolbox.db import adicionar_acao, buscar_acao, listar_acoes, excluir_acao

from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Configurações do banco de dados
DATABASE_URL = 'sqlite:///banco_acoes.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo
class Acao(Base):
    __tablename__ = 'acoes'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    data_adicao = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# App FastAPI
app = FastAPI()

# Rotas

from fastapi import FastAPI, HTTPException
from toolbox.db import adicionar_acao, buscar_acao, listar_acoes, excluir_acao

app = FastAPI()

@app.post("/acoes/")
def adicionar_acao_api(ticker: str):
    return adicionar_acao(ticker)

@app.get("/acoes/")
def listar_acoes_api():
    return listar_acoes()

@app.get("/acoes/{ticker}")
def buscar_acao_api(ticker: str):
    resultado = buscar_acao(ticker)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return resultado

@app.delete("/acoes/{ticker}")
def excluir_acao_api(ticker: str):
    sucesso = excluir_acao(ticker)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Ação não encontrada.")
    return {"mensagem": f"Ação '{ticker}' excluída com sucesso."}