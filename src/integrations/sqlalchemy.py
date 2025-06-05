from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

class SQLAlchemy:
    DATABASE_URL = 'sqlite:///banco_acoes.db'
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base = declarative_base()
    session = SessionLocal()
    Func = func

def get_db():
    db = SQLAlchemy.SessionLocal()
    try:
        yield db
    finally:
        db.close()