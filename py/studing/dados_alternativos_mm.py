from estrategia import BigStrategy
from indicadores import MakeIndicator
from data_feed import ReadData
from otimizacao_movel import WalkFowardAnalysis

class MM_estrategia(BigStrategy):

    def __init__(self):
        super().__init__()

    def fazendo_indicadores(self):

        self.media_maxima = MakeIndicator().media_movel_simples(self.dados.maxima, self.parametro1)
        self.media_minima = MakeIndicator().media_movel_simples(self.dados.minima, self.parametro1)

        self.lista_indicadores = [self.media_maxima, self.media_minima]

    def evento(self, data, i):

        if self.dados.fechamento[data] > self.media_maxima[data]:

            if self.comprado:

                pass

            else:

                self.compra()

        if self.dados.fechamento[data] < self.media_minima[data]:

            if self.comprado:

                self.venda(zerar = True)

            else:

                pass



if __name__ == '__main__':

    acao = 'BTC-USD'

    import yfinance as yf
    import os

    dados_yf = yf.download(acao)
    dados_yf['fator_ajuste'] = dados_yf['Close'] / dados_yf['Adj Close']

    ajsutar = ['Open', 'High', 'Low']

    for ajuste in ajsutar:

        dados_yf[ajuste] = dados_yf[ajuste] / dados_yf['fator_ajuste']

    dados_yf = dados_yf.drop(['Close', 'fator_ajustte'], axis = 1)
    dados_yf = dados_yf.reset_index()

    dados_yf.to_parquet(os.path.join('.', 'dados', f'cotacoes_{acao}.parquet'))

    dados = ReadData(

        nome_arquivo = f'cotacoes_{acao}.parquet',
        data_inicial = '2000-01-01',
        data_final = '2025-03-15',

        formato_data = ('%Y-%m-%d'),

        coluna_data = 0,
        abertura = 1,
        minima = 3,
        maxima = 2,
        fechamento = 4,
        volume = 5
    )

    walk = WalkFowardAnalysis(estrategia = MM_estrategia(), class_dados = dados,
                              parametro1 = range(7, 50, 3), anos_otimizados = 2, anos_teste = 1
                              nome_arquivo = f'backtest_2pra1_{acao}_btc.pdf'
                        )
    
    walk.run_walk()