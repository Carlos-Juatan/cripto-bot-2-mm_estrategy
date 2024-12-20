import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
plt.style.use("cyberpunk")


ticker = "BTC-USD"
dados = yf.download(ticker, start = "2000-01-01", end = "2024-11-30")
dados = dados.droplevel(1, axis = 1)


dados["retorno"] = dados["Adj Close"].pct_change()
dados_retornos_completos = dados["retorno"]
dados["media_maxima"] = dados["High"].rolling(window = 20).mean()
dados["media_minima"] = dados["Low"].rolling(window = 20).mean()


dados["sinal_compra"] = 0
dados["sinal_compra"] = (dados["Close"] > dados["media_maxima"]).astype(int)


dados["sinal_venda"] = 0
dados["sinal_venda"] = (dados["Close"] < dados["media_minima"]).astype(int)

len(dados)


dados["posicao"] = 0

for i in range(1, len(dados)):

    if dados["sinal_compra"].iloc[i] == 1:
        dados["posicao"].iloc[i] = 1

    elif dados["sinal_venda"].iloc[i] == 1:
        dados["posicao"].iloc[i] = 0

    else:
        if (dados["posicao"].iloc[i - 1] == 1) and (dados["sinal_venda"].iloc[i] == 0):
            dados["posicao"].iloc[i] = 1

        else:
            dados["posicao"].iloc[i] = 0


dados["posicao"] = dados["posicao"].shift()


dados["trades"] = (dados["posicao"] != dados["posicao"].shift()).cumsum()
dados["trades"] = dados["trades"].where(dados["posicao"] == 1)
dados = dados.dropna(subset = "trades")


df_retorno_acumulado = (1 + dados["retorno"]).cumprod() - 1
dados_retornos_completos_acum = (1 + dados_retornos_completos).cumprod() - 1

print(df_retorno_acumulado.iloc[-1], dados_retornos_completos_acum.iloc[-1])


df_retorno_acumulado.plot(label = "Modelo")
dados_retornos_completos_acum.plot(label = ticker)
plt.legend()

plt.show()
