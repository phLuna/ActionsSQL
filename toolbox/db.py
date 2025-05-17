import yfinance as yf
from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Define a base ORM
Base = declarative_base()

# Configurações do banco de dados
DATABASE_URL = 'sqlite:///banco_acoes.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
session = SessionLocal()

#Modelo da tabela.
class Acao(Base):
    __tablename__ = 'acoes'

    id = Column(Integer, primary_key = True)
    ticker = Column(String, nullable = False)
    quantidade = Column(Integer, nullable = False)
    investido = Column(Float, nullable = False)
    data_adicao = Column(DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"<Acao(ticker='{self.ticker}', data_adicao='{self.data_adicao}')>"
    
# Criar a tabela (depois de definir o modelo)
Base.metadata.create_all(bind=engine)


def formatar_ticker(ticker: str) -> str:
    """Formata os tickers das ações
    para o formato brasileiro, caso forem."""
    if ticker.endswith(".SA"):
        return ticker
    if ticker.isalnum():
        return ticker + ".SA"
    return ticker

def obter_preco_atual(ticker: str) -> float:
    """Consulta na API do Yahoo o
    preço atual da ação."""
    try:
        ticker_formatado = formatar_ticker(ticker)
        acao = yf.Ticker(ticker_formatado)
        preco = acao.history(period="1d")["Close"].iloc[-1]
        return preco
    except Exception as e:
        return 0.1


def inserir_acao(ticker: str, quantidade: int):
    session = SessionLocal()
    preco = obter_preco_atual(ticker)
    valor_investido = round(preco * quantidade, 2)

    acao_existente = session.query(Acao).filter_by(ticker=ticker).first()
    if acao_existente:
        acao_existente.quantidade += quantidade
        acao_existente.investido += valor_investido
        response = f"{quantidade} unidade(s) adicionada(s) à ação '{ticker}' existente. Investido: R$ {valor_investido:.2f}"
    else:
        nova_acao = Acao(
            ticker=ticker,
            quantidade=quantidade,
            investido=valor_investido
        )
        session.add(nova_acao)
        response = f"{quantidade} de ações '{ticker}' adicionada(s) com sucesso! Investido: R$ {valor_investido:.2f}"

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
            func.sum(Acao.quantidade * Acao.investido).label("investimento_total"),
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
    """Exclui a primeira ocorrência
    de uma ação com o ticker informado."""
    acao = session.query(Acao).filter_by(ticker=ticker).first()
    if acao is None:
        print(f"Ação '{ticker}' não encontrada.")
        return False
    for acao in range(quantidade):
        session.delete(acao)
    session.commit()
    response = (f"Ação '{ticker}' excluída com sucesso.")
    return response