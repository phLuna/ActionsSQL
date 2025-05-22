import yfinance as yf
import requests
from bs4 import BeautifulSoup

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, func

from datetime import datetime
from typing import Optional

from toolbox.table import Acao


# Configurações do banco de dados
DATABASE_URL = 'sqlite:///banco_acoes.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
session = SessionLocal()


def formatar_ticker(ticker: str) -> str:
    """Adequa o ticker fornecido para os
    demais mercados genéricos do mundo."""
    ticker = ticker.upper().strip()
    mercados_internacionais = ['.NS', '.TO', '.L', '.OQ', '.NY', '.HK', '.PA', '.F', '.SS']

    if any(ticker.endswith(sufixo) for sufixo in mercados_internacionais):
        return ticker
    if ticker.endswith('.SA'):
        return ticker
    if ticker.isalnum():
        if 1 <= len(ticker) <= 5:
            if any(c.isdigit() for c in ticker):
                return ticker + '.SA'
            else:
                return ticker
    if ticker.endswith('.SS') or ticker.endswith('.SZ'):
        return ticker
    return ticker

def obter_preco_atual(ticker: str) -> Optional[float]:
    """Consulta o preço atual da ação na API do Yahoo Finance."""
    try:
        ticker_formatado = formatar_ticker(ticker)
        acao = yf.Ticker(ticker_formatado)
        historico = acao.history(period="1d")
        if historico.empty:
            return None  # Não encontrou dados
        preco = historico["Close"].iloc[-1]
        return round(preco, 2)
    except Exception as e:
        return None

def inserir_acao(ticker:    str, 
                quantidade: int,  
                tipo:       Optional[str] = None,
                preco:      Optional[float] = None,
                data:       Optional[datetime] = None):
    """Insere uma ação ou FII. O tipo e o preço são opcionais."""

    ticker = ticker.upper()
    session = SessionLocal()

    # Obtém o preço atual se não fornecido
    if preco is None:
        preco = obter_preco_atual(ticker)
    if preco is None or preco <= 0:
        session.close()
        return f"Erro: preço da ação '{ticker}' não encontrado ou inválido."
    valor_investido = round(preco * quantidade, 2)

    # Define data atual se não fornecida
    if data is None:
        data = datetime.utcnow()

    # Define tipo automaticamente se não fornecido
    if tipo == 'string':
        tipo = "fii" if ticker.upper().endswith("11") else "acao"


    acao_existente = session.query(Acao).filter_by(ticker=ticker).first()
    if acao_existente:
        acao_existente.quantidade += quantidade
        acao_existente.investido += valor_investido
        response = f"{quantidade} unidade(s) adicionada(s) à ação '{ticker}' existente. Investido: R$ {valor_investido:.2f}"
    else:
        nova_acao = Acao(
            ticker      =   ticker,
            quantidade  =   quantidade,
            investido   =   valor_investido,
            tipo        =   tipo,
            data_adicao =   data
        )
        session.add(nova_acao)
        response = f"{quantidade} de '{ticker}' adicionada(s) com sucesso! Investido: R$ {valor_investido:.2f} (tipo: {tipo})"

    session.commit()
    session.close()
    return response

def ver_acoes():
    """Lista os tickers únicos com a quantidade de ocorrências,
    soma das quantidades, valor total investido
    e a data da última adição."""
    resultados = (
        session.query(
            Acao.ticker,
            func.sum(Acao.quantidade).label("quantidade_total"),
            func.sum(Acao.investido).label("investimento_total"),
            func.max(Acao.data_adicao).label("ultima_adicao")
        )
        .group_by(Acao.ticker)
        .order_by(func.max(Acao.data_adicao).desc())
        .all()
    )

    return [
        {
            "Ticker": ticker,
            "Quantidade": quantidade_total,
            "Total Investido": round(preco_total, 2) if preco_total is not None else 0.0,
            "Ultima Adicao": ultima_adicao.strftime('%Y-%m-%d %H:%M:%S')
        }
        for ticker, quantidade_total, preco_total, ultima_adicao in resultados
    ]

def procurar_acao(ticker: str):
    """Busca uma ação específica
    pelo ticker e retorna um
    dicionário com os dados."""

    acoes = session.query(Acao).filter_by(ticker=ticker).all()
    if not acoes:
        return None
    quantidade_total = sum(acao.quantidade for acao in acoes)
    response = {
        "Ticker": ticker,
        "Quantidade": quantidade_total,
        "Preco da unidade": round(obter_preco_atual(ticker), 2),
        "Primeira adição": acoes[0].data_adicao.strftime('%Y-%m-%d %H:%M:%S')
    }
    return response

def deletar_acao(ticker: str, quantidade: int):
    """Exclui até `quantidade` ocorrências da ação com o ticker informado."""

    acoes = (
        session.query(Acao)
        .filter_by(ticker=ticker)
        .order_by(Acao.data_adicao.asc())
        .all()
    )

    if not acoes:
        return f"Ação '{ticker}' não encontrada no banco de dados."

    total_disponivel = sum(a.quantidade for a in acoes)

    # Ajusta a quantidade para o máximo possível
    excluir = min(total_disponivel, quantidade)

    restante = excluir
    for acao in acoes:
        if restante == 0:
            break

        if acao.quantidade <= restante:
            restante -= acao.quantidade
            session.delete(acao)
        else:
            acao.quantidade -= restante
            acao.investido = round(
                acao.investido * (acao.quantidade / (acao.quantidade + restante)), 2
            )
            restante = 0
            session.add(acao)

    session.commit()
    return f"{excluir} ação(ões) '{ticker}' excluída(s) com sucesso."


def pesquisar_acao(nome: str, limite: int = 5):
    """Busca ações por nome no Yahoo Finance"""
    url = f"https://finance.yahoo.com/lookup?s={nome}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    resultados = []
    linhas = soup.select("table tbody tr")

    for linha in linhas[:limite]:
        colunas = linha.find_all("td")
        if len(colunas) >= 2:
            ticker = colunas[0].text.strip()
            nome_empresa = colunas[1].text.strip()
            resultados.append({"ticker": ticker, "nome": nome_empresa})
    
    return resultados