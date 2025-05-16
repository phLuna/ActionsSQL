from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
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

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_adicao = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Acao(ticker='{self.ticker}', data_adicao='{self.data_adicao}')>"
    
# Criar a tabela (depois de definir o modelo)
Base.metadata.create_all(bind=engine)


def inserir_acao(ticker: str, quantidade: int):
    session = SessionLocal()
    acao = Acao(ticker=ticker, quantidade=quantidade)
    session.add(acao)
    session.commit()
    session.close()
    response = f"{quantidade} de ações '{ticker}' adicionada(s) com sucesso!"
    return response


def ver_acoes():
    """Lista os tickers únicos com a quantidade de ocorrências e a data da última adição."""
    resultados = (
        session.query(
            Acao.ticker,
            func.count(Acao.id).label("quantidade"),
            func.max(Acao.data_adicao).label("ultima_adicao")
        )
        .group_by(Acao.ticker)
        .order_by(func.max(Acao.data_adicao).desc())
        .all()
    )

    return [
        {
            "ticker": ticker,
            "quantidade": quantidade,
            "ultima_adicao": ultima_adicao.strftime('%Y-%m-%d %H:%M:%S')
        }
        for ticker, quantidade, ultima_adicao in resultados
    ]


def procurar_acao(ticker: str):
    """Busca uma ação específica pelo ticker e retorna um dicionário com os dados."""
    acoes = session.query(Acao).filter_by(ticker=ticker).all()

    if not acoes:
        return None

    quantidade_total = sum(acao.quantidade for acao in acoes)

    response = {
        "ticker": ticker,
        "quantidade": quantidade_total,
        "primeira_adicao": acoes[0].data_adicao.strftime('%Y-%m-%d %H:%M:%S')
    }
    return response


def deletar_acao(ticker: str):
    """Exclui a primeira ocorrência de uma ação com o ticker informado."""
    acao = session.query(Acao).filter_by(ticker=ticker).first()

    if acao is None:
        print(f"Ação '{ticker}' não encontrada.")
        return False

    session.delete(acao)
    session.commit()
    print(f"Ação '{ticker}' excluída com sucesso.")
    return True
