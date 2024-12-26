# Passo 1 - Importar as bibliotecas
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
plt.style.use("cyberpunk")

# Passo 2 - Pegar dados de cotação do Yahoo Finance
def fetch_yahoo_data(ticker, startTime, endTime):
    data = yf.download(ticker, startTime, endTime)
    data = data.droplevel(1, axis = 1)
    return data

# Passo 3 - Calcular indicadores pro modelo
def get_returned_metrics(data):
    data["retorno"] = data["Adj Close"].pct_change()
    return data["retorno"]

def get_metrics(data):
    data["media_maxima"] = data["High"].rolling(window = 20).mean()
    data["media_minima"] = data["Low"].rolling(window = 20).mean()
    return data

# Passo 4 - Gerar sinais de compra
def generate_buy_signals(data):
    data["sinal_compra"] = 0
    data["sinal_compra"] = (data["Close"] > data["media_maxima"]).astype(int)
    return data

# Passo 5 - Gerar sinais de venda
def generate_sell_signals(data):
    data["sinal_venda"] = 0
    data["sinal_venda"] = (data["Close"] < data["media_minima"]).astype(int)
    return data

# Passo 6 - Gerar operações
def generate_position(data):
    data["posicao"] = 0

    for i in range(1, len(data)):
        if data["sinal_compra"].iloc[i] == 1:
            data["posicao"].iloc[i] = 1

        elif data["sinal_venda"].iloc[i] == 1:
            data["posicao"].iloc[i] = 0

        else:
            if (data["posicao"].iloc[i - 1] == 1) and (data["signal"].iloc[i] == 0):
                data["posicao"].iloc[i] = 1

            else:
                data["posicao"].iloc[i] = 0

    data["posicao"] = data["posicao"].shift()
    return data

# Passo 7 - Criar um ID para todos os trades históricos na tabela
def generate_id(data):
    data["trades"] = (data["posicao"] != data["posicao"].shift()).cumsum()
    data["trades"] = data["trades"].where(data["posicao"] == 1)
    data = data.dropna(subset = "trades")
    return data

# Passo 8 - Calcular retornos de todos os trades
def calculate_cumulative_return(data):
    value = (1 + data["retorno"]).cumprod() - 1
    return value

def get_equity_curve(returned_metrics):
    value = (1 + returned_metrics).cumprod() - 1
    return value

# Passo 9 - Gráfico de retornos
def show_graphics(cumulative_return, equity_curve):
    cumulative_return.plot(label = "Modelo")
    equity_curve.plot(label = tickerSymbo)
    plt.legend()

    plt.show()


# Passo 2 - Pegar dados de cotação do Yahoo Finance
tickerSymbo = "BTC-USD"
dados = fetch_yahoo_data(tickerSymbo, "2000-01-01", "2024-11-30")
print(dados)

# Passo 3 - Calcular indicadores pro modelo
dados_retornos_completos = get_returned_metrics(dados)
dados = get_metrics(dados)

# Passo 4 - Gerar sinais de compra
dados = generate_buy_signals(dados)

# Passo 5 - Gerar sinais de venda
dados = generate_sell_signals(dados)

# Passo 6 - Gerar operações
dados = generate_position(dados)

# Passo 7 - Criar um ID para todos os trades históricos na tabela
dados = generate_id(dados)

# Passo 8 - Calcular retornos de todos os trades
df_retorno_acumulado = calculate_cumulative_return(dados)
dados_retornos_completos_acum = get_equity_curve(dados_retornos_completos)

# Passo 9 - Gráfico de retornos
show_graphics(df_retorno_acumulado, dados_retornos_completos_acum)