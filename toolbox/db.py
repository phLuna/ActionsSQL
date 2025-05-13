from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Define a base ORM
Base = declarative_base()

#Modelo da tabela.
class Acao(Base):
    __tablename__ = 'acoes'

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    data_adicao = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Acao(ticker='{self.ticker}', data_adicao='{self.data_adicao}')>"

#Conectar ao banco.
engine = create_engine('sqlite:///banco_acoes.db', echo=False)
Base.metadata.create_all(engine)

#Interagir com o banco.
Session = sessionmaker(bind=engine)
session = Session()


def adicionar_acao(ticker: str):
    acao = Acao(ticker=ticker)
    session.add(acao)
    session.commit()
    print(f"Ação '{ticker}' adicionada com sucesso!")


def buscar_acao(ticker: str):
    """Busca uma ação específica pelo ticker e retorna um dicionário com os dados."""
    acao = session.query(Acao).filter_by(ticker=ticker).first()

    if acao is None:
        return None

    return {
        "ticker": acao.ticker,
        "data_adicao": acao.data_adicao.strftime('%Y-%m-%d %H:%M:%S')
    }


def listar_acoes():
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



def excluir_acao(ticker: str):
    """Exclui a primeira ocorrência de uma ação com o ticker informado."""
    acao = session.query(Acao).filter_by(ticker=ticker).first()

    if acao is None:
        print(f"Ação '{ticker}' não encontrada.")
        return False

    session.delete(acao)
    session.commit()
    print(f"Ação '{ticker}' excluída com sucesso.")
    return True
