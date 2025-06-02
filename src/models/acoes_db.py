from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.models.base import Base  # importa o mesmo Base

class Acao(Base):
    __tablename__ = 'banco_acoes'

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    tipo = Column(String, nullable=True)
    quantidade = Column(Integer, nullable=False)
    investido = Column(Float, nullable=False)
    data_adicao = Column(DateTime, default=datetime.utcnow)

    meta = relationship('MetaAlocacao', back_populates='acao', uselist=False)

    def __repr__(self):
        return f"<Acao(ticker='{self.ticker}', data_adicao='{self.data_adicao}')>"
