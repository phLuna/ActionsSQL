from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Define a base ORM
Base = declarative_base()

# Tabela de ações
class Acao(Base):
    __tablename__ = 'acoes'

    id = Column(Integer, primary_key=True)
    ticket = Column(String, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Acao(ticket='{self.ticket}', data='{self.data}')>"

# Conexão com o banco (SQLite local)
engine = create_engine('sqlite:///banco_acoes.db', echo=False)
Base.metadata.create_all(engine)

# Criar sessão
Session = sessionmaker(bind=engine)
session = Session()

# Função para adicionar uma ação
def adicionar_acao(ticket: str):
    acao = Acao(ticket=ticket)
    session.add(acao)
    session.commit()
    print(f"Ação '{ticket}' adicionada com sucesso!")

# Função para listar todas as ações
def listar_acoes():
    acoes = session.query(Acao).all()
    for acao in acoes:
        print(acao)

# Exemplo de uso
if __name__ == '__main__':
    adicionar_acao("PETR4")
    adicionar_acao("VALE3")
    listar_acoes()
