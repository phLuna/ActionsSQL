from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base  # importa o mesmo Base

class MetaAlocacao(Base):
    __tablename__ = 'metas'

    id = Column(Integer, primary_key=True)
    id_acao = Column(Integer, ForeignKey('acoes.id'), nullable=False)
    percentual = Column(Float, nullable=False)

    acao = relationship('Acao', back_populates='meta')

    def __repr__(self):
        return f"<MetaAlocacao(id_acao={self.id_acao}, percentual={self.percentual})>"