from src.integrations.sqlalchemy import SQLAlchemy

Base = SQLAlchemy.Base
engine = SQLAlchemy.engine
session = SQLAlchemy.session
Base.metadata.create_all(bind=engine)