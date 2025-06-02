from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Defina Base apenas uma vez!
Base = declarative_base()

# Configurações do banco de dados
engine = create_engine("sqlite:///banco_acoes.db")
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = SessionLocal()

# Criar a tabela (depois de definir o modelo)
Base.metadata.create_all(bind=engine)