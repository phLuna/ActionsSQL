from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, func

class SQLAlchemy:
    DATABASE_URL = 'sqlite:///banco_acoes.db'
    engine       = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base         = declarative_base()

