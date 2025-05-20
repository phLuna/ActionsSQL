from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

from datetime import datetime


# Define a base ORM
Base = declarative_base()


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
    
# Define a base ORM
Base = declarative_base()

# Configurações do banco de dados
DATABASE_URL = 'sqlite:///banco_acoes.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
session = SessionLocal()

# Criar a tabela (depois de definir o modelo)
Base.metadata.create_all(bind=engine)