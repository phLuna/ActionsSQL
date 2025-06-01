import requests
from typing import Optional, List

import yfinance as yf
from bs4 import BeautifulSoup

class YahooAPI:
    @staticmethod
    def formatar_ticker(ticker: str) -> str:
        """Adequa o ticker fornecido para os demais mercados genéricos do mundo."""
        ticker = ticker.upper().strip()
        mercados_internacionais = ['.NS', '.TO', '.L', '.OQ', '.NY', '.HK', '.PA', '.F', '.SS']

        if any(ticker.endswith(sufixo) for sufixo in mercados_internacionais):
            return ticker
        if ticker.endswith('.SA'):
            return ticker
        if ticker.isalnum():
            if 1 <= len(ticker) <= 5:
                if any(c.isdigit() for c in ticker):
                    return ticker + '.SA'
                else:
                    return ticker
        if ticker.endswith('.SS') or ticker.endswith('.SZ'):
            return ticker
        return ticker

    @staticmethod
    def preco_atual(ticker: str) -> Optional[float]:
        """Consulta o preço atual da ação na API do Yahoo Finance."""
        try:
            ticker_formatado = YahooAPI.formatar_ticker(ticker)
            acao = yf.Ticker(ticker_formatado)
            historico = acao.history(period="1d")
            if historico.empty:
                return None  # Não encontrou dados
            preco = historico["Close"].iloc[-1]
            return round(preco, 2)
        except Exception:
            return None

    @staticmethod
    def pesquisar_acao(nome: str, limite: int = 5) -> List[dict]:
        """Busca ações por nome no Yahoo Finance via scraping HTML"""
        url = f"https://finance.yahoo.com/lookup?s={nome}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            resultados = []
            linhas = soup.select("table tbody tr")

            for linha in linhas[:limite]:
                colunas = linha.find_all("td")
                if len(colunas) >= 2:
                    ticker = colunas[0].text.strip()
                    nome_empresa = colunas[1].text.strip()

                    if ticker.endswith("11"):
                        tipo = "fii"
                    elif ticker.endswith(".SA") or ticker.endswith(".NS") or ticker.endswith(".BO") or "." in ticker:
                        tipo = "acao"
                    else:
                        tipo = "outro"

                    resultados.append({
                        "ticker": ticker,
                        "nome": nome_empresa,
                        "tipo": tipo
                    })

            return resultados
        except Exception:
            return []