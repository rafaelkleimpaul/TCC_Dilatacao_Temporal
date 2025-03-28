# -----------------------------
# TCC: Modelagem Computacional de Buracos Negros
# Autor: Rafael Kleimpaul Parente Bueno
# Ferramentas: Python, Jupyter Notebook
# -----------------------------

# Importação das bibliotecas necessárias
import pandas as pd             # Biblioteca para manipulação de dados em tabelas (DataFrames)
import os                       # Biblioteca para percorrer diretórios e lidar com arquivos
import matplotlib.pyplot as plt # Biblioteca para visualização e criação de gráficos

# -----------------------------------------------------------
# Definição do caminho base onde estão as pastas com os arquivos CSV
# -----------------------------------------------------------
pasta_base = r"C:\Users\Zenn\Desktop\TCC\Projeto"

# -----------------------------------------------------------
# Busca recursiva por todos os arquivos .csv dentro das subpastas
# -----------------------------------------------------------
csv_paths = []
for raiz, dirs, arquivos in os.walk(pasta_base):
    for arquivo in arquivos:
        if arquivo.endswith(".csv"):  # Verifica se o arquivo tem extensão .csv
            csv_paths.append(os.path.join(raiz, arquivo))  # Adiciona o caminho completo do CSV

# -----------------------------------------------------------
# Inicialização da estrutura para armazenar os resultados resumidos
# -----------------------------------------------------------
resumo = {
    "Nome_Caso": [],         # Nome do arquivo (formatado)
    "Fator Mínimo": [],      # Menor valor de dilatação temporal no caso
    "Fator Máximo": [],      # Maior valor de dilatação temporal no caso
    "Média": [],             # Média dos valores de dilatação
    "Desvio Padrão": []      # Desvio padrão da série de dilatação
}

# -----------------------------------------------------------
# Leitura e análise estatística de cada arquivo CSV
# -----------------------------------------------------------
for caminho in csv_paths:
    df = pd.read_csv(caminho)  # Leitura do CSV como DataFrame

    # Cálculo das métricas estatísticas da coluna "Fator_Dilatacao"
    media = df["Fator_Dilatacao"].mean()
    minimo = df["Fator_Dilatacao"].min()
    maximo = df["Fator_Dilatacao"].max()
    desvio = df["Fator_Dilatacao"].std()

    # Formatação do nome do caso com base no nome do arquivo
    nome_arquivo = os.path.basename(caminho).replace(".csv", "").replace("_", " ").title()

    # Armazenamento dos resultados no dicionário "resumo"
    resumo["Nome_Caso"].append(nome_arquivo)
    resumo["Fator Mínimo"].append(round(minimo, 4))
    resumo["Fator Máximo"].append(round(maximo, 4))
    resumo["Média"].append(round(media, 4))
    resumo["Desvio Padrão"].append(round(desvio, 4))

# -----------------------------------------------------------
# Criação do DataFrame final com todos os resultados agregados
# -----------------------------------------------------------
df_resumo = pd.DataFrame(resumo)

# Exibição da tabela final no console (pode ser substituído por display() em Jupyter)
print(df_resumo)

# -----------------------------------------------------------
# Geração do gráfico comparativo das médias de dilatação temporal
# -----------------------------------------------------------
plt.figure(figsize=(10, 6))  # Define o tamanho do gráfico
plt.bar(
    df_resumo["Nome_Caso"],             # Nomes dos casos no eixo X
    df_resumo["Média"],                 # Altura das barras com base na média
    yerr=df_resumo["Desvio Padrão"],   # Barras de erro com o desvio padrão
    capsize=5                           # Tamanho das extremidades das barras de erro
)
plt.xticks(rotation=45, ha='right')     # Rotação dos nomes no eixo X para melhor leitura
plt.ylabel("Média do Fator de Dilatação")
plt.title("Comparação dos Casos – Média da Dilatação Temporal")
plt.tight_layout()                      # Ajuste automático dos elementos do gráfico

# -----------------------------------------------------------
# Salvamento do gráfico na pasta base do projeto
# -----------------------------------------------------------
grafico_saida = os.path.join(pasta_base, "comparacao_dilatacao_temporal.png")
plt.savefig(grafico_saida, dpi=300)     # Salva o gráfico em alta resolução
plt.close()                             # Fecha a figura para liberar memória

# Mensagem de confirmação no terminal
print(f"\n Gráfico salvo em: {grafico_saida}")
