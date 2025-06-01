from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, func

from datetime import datetime
from typing import Optional

from toolbox.table import Acao, MetaAlocacao
from src.integrations.yahoof import YahooAPI


# Configurações do banco de dados
DATABASE_URL = 'sqlite:///banco_acoes.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
session = SessionLocal()

def inserir_acao(ticker:    str, 
                quantidade: int,  
                tipo:       Optional[str] = None,
                preco:      Optional[float] = None,
                data:       Optional[datetime] = None):
    """Insere uma ação ou FII. O tipo e o preço são opcionais."""

    ticker = ticker.upper()
    session = SessionLocal()

    # Obtém o preço atual se não fornecido
    if preco is None:
        preco = YahooAPI.preco_atual(ticker)
    if preco is None or preco <= 0:
        session.close()
        return f"Erro: preço da ação '{ticker}' não encontrado ou inválido."
    valor_investido = round(preco * quantidade, 2)

    # Define data atual se não fornecida
    if data is None:
        data = datetime.utcnow()

    # Define tipo automaticamente se não fornecido
    if tipo == 'string':
        tipo = "fii" if ticker.upper().endswith("11") else "acao"


    acao_existente = session.query(Acao).filter_by(ticker=ticker).first()
    if acao_existente:
        acao_existente.quantidade += quantidade
        acao_existente.investido += valor_investido
        response = f"{quantidade} unidade(s) adicionada(s) à ação '{ticker}' existente. Investido: R$ {valor_investido:.2f}"
    else:
        nova_acao = Acao(
            ticker      =   ticker,
            quantidade  =   quantidade,
            investido   =   valor_investido,
            tipo        =   tipo,
            data_adicao =   data
        )
        session.add(nova_acao)
        response = f"{quantidade} de '{ticker}' adicionada(s) com sucesso! Investido: R$ {valor_investido:.2f} (tipo: {tipo})"

    session.commit()
    session.close()
    return response

def ver_acoes():
    """Lista os tickers únicos com a quantidade de ocorrências,
    soma das quantidades, valor total investido
    e a data da última adição."""
    resultados = (
        session.query(
            Acao.ticker,
            func.sum(Acao.quantidade).label("quantidade_total"),
            func.sum(Acao.investido).label("investimento_total"),
            func.max(Acao.data_adicao).label("ultima_adicao")
        )
        .group_by(Acao.ticker)
        .order_by(func.max(Acao.data_adicao).desc())
        .all()
    )

    return [
        {
            "Ticker": ticker,
            "Quantidade": quantidade_total,
            "Total Investido": round(preco_total, 2) if preco_total is not None else 0.0,
            "Ultima Adicao": ultima_adicao.strftime('%Y-%m-%d %H:%M:%S')
        }
        for ticker, quantidade_total, preco_total, ultima_adicao in resultados
    ]

def procurar_acao(ticker: str):
    """Busca uma ação específica
    pelo ticker e retorna um
    dicionário com os dados."""

    acoes = session.query(Acao).filter_by(ticker=ticker).all()
    if not acoes:
        return None

    quantidade_total = sum(acao.quantidade for acao in acoes)
    investido_total = round(sum(acao.investido for acao in acoes), 2)
    preco_atual = YahooAPI.preco_atual(ticker)

    response = {
        "Ticker": ticker,
        "Quantidade": quantidade_total,
        "Investido": investido_total,
        "Preco da unidade": round(preco_atual, 2) if preco_atual else None,
        "Primeira adição": acoes[0].data_adicao.strftime('%Y-%m-%d %H:%M:%S')
    }
    return response

def deletar_acao(ticker: str, quantidade: int):
    """Exclui até `quantidade` ocorrências da ação com o ticker informado."""

    acoes = (
        session.query(Acao)
        .filter_by(ticker=ticker)
        .order_by(Acao.data_adicao.asc())
        .all()
    )

    if not acoes:
        return f"Ação '{ticker}' não encontrada no banco de dados."

    total_disponivel = sum(a.quantidade for a in acoes)

    # Ajusta a quantidade para o máximo possível
    excluir = min(total_disponivel, quantidade)

    restante = excluir
    for acao in acoes:
        if restante == 0:
            break

        if acao.quantidade <= restante:
            restante -= acao.quantidade
            session.delete(acao)
        else:
            acao.quantidade -= restante
            acao.investido = round(
                acao.investido * (acao.quantidade / (acao.quantidade + restante)), 2
            )
            restante = 0
            session.add(acao)

    session.commit()
    return f"{excluir} ação(ões) '{ticker}' excluída(s) com sucesso."

def deletar_meta(ticker: str) -> bool:
    """Exclui a meta de alocação pelo ticker.
    Retorna True se excluiu, False se não encontrou."""

    meta = session.query(MetaAlocacao).filter_by(ticker=ticker).first()
    if not meta:
        return False
    session.delete(meta)
    session.commit()
    return True

def adicionar_meta(ticker: str, porcentagem: float):
    acao = session.query(Acao).filter_by(ticker=ticker).first()
    if not acao:
        return f'Açao {ticker} não foi encontrada.'
    
    meta = session.query(MetaAlocacao).filter_by(ticker=ticker).first()
    if meta:
        meta.porcentagem_desejada = porcentagem
    else:
        nova_meta = MetaAlocacao(ticker = ticker, porcentagem_desejada = porcentagem)
        session.add(nova_meta)

    session.commit()
    return f'Meta de {porcentagem:.1f}% definida para {ticker}'

def comparar_alocacao():
    acoes = session.query(Acao).all()
    metas = {m.ticker: m.porcentagem_desejada for m in session.query(MetaAlocacao).all()}
    total_investido = sum(a.investido for a in acoes)

    relatorio = []
    for a in acoes:
        atual = (a.investido / total_investido) * 100 if total_investido else 0
        desejada = metas.get(a.ticker, 0)
        diferenca = round(atual - desejada, 2)
        relatorio.append({
            "Ticker": a.ticker,
            "Atual (%)": round(atual, 2),
            "Desejada (%)": round(desejada, 2),
            "Diferença (%)": diferenca,
            "Investido (R$)": round(a.investido, 2)
        })

    return relatorio