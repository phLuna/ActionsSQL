from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.models.base import Base  # importa o mesmo Base

class Acao(Base):
    __tablename__ = 'acoes'

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    ticker = Column(String, nullable=False)
    tipo = Column(String, nullable=True)
    quantidade = Column(Integer, nullable=False)
    total_pago = Column(Float, nullable=False)
    ultima_adicao = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("User", back_populates="acoes")
    meta = relationship('MetaAlocacao', back_populates='acao', uselist=False)

    def __repr__(self):
        return f"<Acao(ticker='{self.ticker}', ultima_adicao='{self.ultima_adicao}')>"