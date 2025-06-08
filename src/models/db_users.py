from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base

class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    acoes = relationship("Acao", back_populates="usuario")

    def __repr__(self):
        return f"<User(nome='{self.nome}', email='{self.email}')>"