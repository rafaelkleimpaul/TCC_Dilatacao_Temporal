# -----------------------------
# TCC: Modelagem Computacional de Buracos Negros
# Autor: Rafael Kleimpaul Parente Bueno
# Ferramentas: Python, Jupyter Notebook
# -----------------------------

# Importação das bibliotecas necessárias
import numpy as np                          # Biblioteca para operações numéricas e vetoriais
import matplotlib.pyplot as plt             # Biblioteca para geração de gráficos
from mpl_toolkits.mplot3d import Axes3D     # Suporte para gráficos 3D no matplotlib
import os                                   # Biblioteca para manipulação de diretórios
import unicodedata                          # Utilizada para remover acentuação em nomes de arquivos
import pandas as pd                         # Biblioteca para manipulação e exportação de dados em formato de tabela

# -----------------------------
# Definição de constantes físicas
# -----------------------------
G = 6.67430e-11         # Constante gravitacional universal (m³/kg/s²)
c = 3e8                 # Velocidade da luz no vácuo (m/s)
massa_solar = 1.989e30  # Massa do Sol (kg), usada como base para converter massas estelares

# -----------------------------
# Função para formatar nomes de arquivos/pastas, removendo acentos e símbolos
# -----------------------------
def formatar_nome(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    return nome.lower().replace(" ", "_").replace("–", "-").replace("—", "-")

# -----------------------------
# Função para calcular o Raio de Schwarzschild (Rs) a partir de uma massa M
# -----------------------------
def raio_schwarzschild(m):
    return 2 * G * m / c**2

# -----------------------------
# Função principal que executa a simulação de curvatura do espaço-tempo e dilatação temporal
# -----------------------------
def simular(massas_solares, distancia_rs, escala=1.0, titulo="Simulacao"):
    # Conversão da massa fornecida (em massas solares) para kg
    massa = massas_solares * massa_solar
    
    # Cálculo do raio de Schwarzschild correspondente
    rs = raio_schwarzschild(massa)

    # Impressão dos parâmetros utilizados na simulação
    print(f"➡ Massa: {massas_solares:.1f} M☉")
    print(f"➡ Raio de Schwarzschild: {rs:.2e} m")
    print(f"➡ Distância analisada: {distancia_rs:.2f} Rs\n")

    # Geração de uma grade (malha) para visualização da curvatura
    x = np.linspace(-10, 10, 100) * escala
    y = np.linspace(-10, 10, 100) * escala
    X, Y = np.meshgrid(x, y)
    
    # Cálculo da "profundidade" da curvatura para gerar o efeito visual em 3D
    Z = -rs / np.sqrt(X**2 + Y**2 + rs**2)

    # Criação de uma figura com dois gráficos lado a lado
    fig = plt.figure(figsize=(14, 5))

    # Gráfico 3D da curvatura do espaço-tempo
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='plasma')
    ax1.set_title(f"Curvatura do Espaço-Tempo\n{titulo}")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("Curvatura")

    # Geração de vetor de distâncias a partir de 1.01 Rs até a distância máxima escolhida
    r = np.linspace(1.01 * rs, distancia_rs * rs, 500)
    
    # Cálculo da dilatação do tempo usando a métrica de Schwarzschild
    dilatacao = np.sqrt(1 - rs / r)

    # Gráfico 2D da dilatação temporal
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(r / rs, dilatacao)
    ax2.set_title(f"Dilatação Temporal\n{titulo}")
    ax2.set_xlabel("Distância (em múltiplos de Rs)")
    ax2.set_ylabel("Fator de tempo")
    ax2.grid(True)

    # Ajuste automático da organização da figura
    plt.tight_layout()

    # Criação da pasta de saída com nome formatado
    pasta = formatar_nome(titulo)
    os.makedirs(pasta, exist_ok=True)

    # Definição dos caminhos para salvar os arquivos de imagem e dados
    nome_arquivo_img = os.path.join(pasta, f"{pasta}.png")
    nome_arquivo_csv = os.path.join(pasta, f"{pasta}.csv")

    # Salvamento do gráfico da simulação em formato PNG (alta qualidade)
    fig.savefig(nome_arquivo_img, dpi=300)

    # Criação de um DataFrame com os dados da simulação
    df = pd.DataFrame({
        "Distancia_RS": r / rs,            # Distância em múltiplos do Rs
        "Distancia_metros": r,             # Distância real em metros
        "Fator_Dilatacao": dilatacao       # Fator de dilatação temporal calculado
    })

    # Salvamento do DataFrame em formato CSV
    df.to_csv(nome_arquivo_csv, index=False)

    # Confirmação no terminal
    print(f" Gráfico salvo em: {nome_arquivo_img}")
    print(f" CSV salvo em: {nome_arquivo_csv}")

    # Fecha a figura para liberar memória
    plt.close(fig)

# -----------------------------
# Lista de casos definidos para simulação
# Cada tupla contém: (Nome do caso, Massa (M☉), Distância máxima (Rs), Escala gráfica)
# -----------------------------
casos = [
    ("Caso 1 – Estrela de Neutrons", 1.4, 5, 1.0),
    ("Caso 2 – Buraco Negro Estelar", 5, 10, 1.0),
    ("Caso 3 – Buraco Negro Supermassivo", 1_000_000, 100, 1.5),
    ("Caso 4 – Proximo do Horizonte", 10, 1.01, 0.8),
    ("Caso 5 – Massa Subcritica (Planeta)", 0.001, 5, 1.0)
]

# -----------------------------
# Execução de todas as simulações da lista
# Cada caso gera: 1 gráfico PNG + 1 tabela CSV com os dados
# -----------------------------
for nome, massa, distancia, escala in casos:
    simular(massa, distancia, escala, titulo=nome)

# Mensagem final de confirmação (opcional)
"Todos os casos foram executados e os resultados (gráficos e CSVs) foram salvos nas pastas correspondentes."