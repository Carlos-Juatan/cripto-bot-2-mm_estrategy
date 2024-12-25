# Nescessário para mostrar os graficos na tela
import matplotlib.pyplot as plt

# Nescessário para mudar o tema dos gráficos
import mplcyberpunk 
plt.style.use("cyberpunk")

class Visualizer:
    def plot_results(self, data, backtester):
        # Criando uma figura com 4 linhas e 1 coluna e  compartilhando o eixo x
        fig, axs = plt.subplots(2, 1, figsize=(16, 9), sharex=True, gridspec_kw={'height_ratios': [10, 1]})

        # Plotando o preço de fechamento no primeiro subplot (maior)
        axs[0].plot(data['close'], label='Preço de Fechamento')
        axs[0].plot(data['BB_upper'])
        axs[0].plot(data['BB_lower'])
        axs[0].legend()

        # Plotando K no terceiro subplot
        axs[1].plot(data['K'], label='K', color='brown')
        axs[1].axhline(y=20, color='gray', linestyle='--')
        axs[1].axhline(y=80, color='gray', linestyle='--')
        axs[1].legend()

        # Sinais de compra
        axs[0].scatter(data.index[data['event'] == 1], data['close'][data['event'] == 1], marker='^', color='green', label='Sinal de Compra')
        axs[0].scatter(data.index[data['event'] == -1], data['close'][data['event'] == -1], marker='v', color='red', label='Sinal de Venda')
        axs[0].legend()

        # Ajustando o espaçamento entre os subplots
        plt.tight_layout()

        # Removendo os eixos x dos subplots intermediários
        for ax in axs[1:-1]:
            plt.setp(ax.get_xticklabels(), visible=False)

        plt.show()