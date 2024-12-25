"""
Vamos Criar Gráficos Múltiplos em Python!
Para te apresentar um código mais específico, preciso de algumas informações adicionais:

Que tipo de dados você está trabalhando? Séries temporais, dados categóricos, numéricos?
Qual biblioteca você prefere usar? Matplotlib, Seaborn, Plotly, ou outra?
Qual o objetivo da sua visualização? Comparar valores, identificar padrões, mostrar distribuições?
Mas, enquanto isso, aqui estão alguns exemplos básicos utilizando a biblioteca Matplotlib, que é uma das mais populares para criar gráficos em Python:

Exemplo 1: Gráficos de Linha Simples
Python

"""
import matplotlib.pyplot as plt
import numpy as np

# Criando dados de exemplo
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Criando a figura e os subplots
fig, (ax1, ax2) = plt.subplots(2, 1)

# Plotando os dados
ax1.plot(x, y1, label='Seno')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.legend()

ax2.plot(x, y2, label='Cosseno')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.legend()

plt.show()