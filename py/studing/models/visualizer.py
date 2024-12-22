# Nescessário para mostrar os graficos na tela
import matplotlib.pyplot as plt

# Nescessário para mudar o tema dos gráficos
import mplcyberpunk 
plt.style.use("cyberpunk")

class Visualizer:
    def plot_results(self, data):
        plt.figure(figsize=(1080,720))
        plt.plot(data['Close'], label='Preço de Fechamento')
        plt.plot(data['MA_20'])
        plt.plot(data['MA_200'])
        # plt.plot(data['mostrar_lucro'], label='lucro')
        # plt.scatter(data.index[data['signal'] == 1], data['Close'][data['signal'] == 1], marker='^', color='green', label='Sinal de Compra')
        # plt.scatter(data.index[data['signal'] == 0], data['Close'][data['signal'] == 0], marker='v', color='red', label='Sinal de Venda')
        plt.legend()
        plt.show()