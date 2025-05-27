from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Defina Base apenas uma vez!
Base = declarative_base()

# Modelo da tabela de ações.
class Acao(Base):
    __tablename__ = 'banco_acoes'

    id          = Column(Integer, primary_key=True)
    ticker      = Column(String, nullable=False)
    tipo        = Column(String, nullable=True)
    quantidade  = Column(Integer, nullable=False)
    investido   = Column(Float, nullable=False)
    data_adicao = Column(DateTime, default=datetime.utcnow)
    meta = relationship('MetaAlocacao', uselist=False, back_populates = 'acao')

    def __repr__(self):
        return f"<Acao(ticker='{self.ticker}', data_adicao='{self.data_adicao}')>"
    
# Modelo da tabela de porcentagem pretendida.
class MetaAlocacao(Base):
    __tablename__ = 'meta_alocacao'

    ticker = Column(String, ForeignKey("banco_acoes.ticker"), primary_key=True)
    porcentagem_desejada = Column(Float, nullable=False)

    acao = relationship('Acao', back_populates = 'meta')

# Configurações do banco de dados
engine = create_engine("sqlite:///banco_acoes.db")
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = SessionLocal()

# Criar a tabela (depois de definir o modelo)
Base.metadata.create_all(bind=engine)