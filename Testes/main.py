# TCC: Modelagem Computacional de Buracos Negros
# Autor: Rafael Kleimpaul Parente Bueno
# Ferramentas: Python, Jupyter Notebook

# ------------------------------
# Introdução
"""
Este notebook tem como objetivo simular e visualizar os efeitos gravitacionais de um buraco negro
por meio de modelagem computacional utilizando Python. Serão abordados conceitos como o raio de
Schwarzschild, curvatura do espaço-tempo e desvio da luz.
"""

# ------------------------------
# Importação de Bibliotecas
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact

# ------------------------------
# Cálculo do Raio de Schwarzschild
G = 6.67430e-11  # Constante gravitacional (m^3 kg^-1 s^-2)
c = 3e8          # Velocidade da luz (m/s)
massa_solar = 1.989e30  # Massa do Sol em kg

# Função do raio de Schwarzschild
def raio_schwarzschild(m):
    return (2 * G * m) / (c**2)

massa = 5 * massa_solar
rs = raio_schwarzschild(massa)

print(f"Raio de Schwarzschild para 5 massas solares: {rs:.2f} metros")

# ------------------------------
# Visualização da Curvatura do Espaço-Tempo
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
Z = -rs / np.sqrt(X**2 + Y**2 + rs**2)  # Curvatura simplificada

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='plasma')
ax.set_title("Curvatura do Espaço-Tempo ao Redor de um Buraco Negro")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Curvatura")
plt.show()

# ------------------------------
# Simulação Básica da Deflexão da Luz (Lente Gravitacional)
deflexao = []

for y in np.linspace(2*rs, 10*rs, 500):
    theta = rs / y  # simplificação não-relativística
    deflexao.append((y, np.tan(theta)))

x_vals = [x for _, x in deflexao]
y_vals = [y for y, _ in deflexao]

plt.plot(x_vals, y_vals, label="Raio de luz desviado")
plt.axvline(0, color='black', linestyle='--', label='Buraco Negro')
plt.title("Desvio da Luz pela Gravidade (Simulação Simplificada)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()

# ------------------------------
# Comparação do Raio de Schwarzschild para Diferentes Massas
massas = np.linspace(1, 1e7, 1000) * massa_solar
rs_vals = raio_schwarzschild(massas)

plt.plot(massas / massa_solar, rs_vals / 1000)
plt.xlabel("Massa (em massas solares)")
plt.ylabel("Raio de Schwarzschild (km)")
plt.title("Raio de Schwarzschild vs Massa")
plt.grid(True)
plt.show()

# ------------------------------
# Simulação da Dilatação do Tempo
r = np.linspace(1.01*rs, 10*rs, 500)
dilatacao = np.sqrt(1 - rs/r)

plt.plot(r / rs, dilatacao)
plt.xlabel("Distância (em múltiplos de Rs)")
plt.ylabel("Fator de dilatação do tempo")
plt.title("Dilatação temporal próxima ao buraco negro")
plt.grid(True)
plt.show()

# ------------------------------
# Interface Interativa com ipywidgets
@interact(massa=(1, 20, 1))
def atualizar_curvatura(massa):
    m = massa * massa_solar
    rs_local = raio_schwarzschild(m)
    Z_local = -rs_local / np.sqrt(X**2 + Y**2 + rs_local**2)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z_local, cmap='plasma')
    ax.set_title(f"Curvatura do Espaço-Tempo (massa = {massa} M☉)")
    plt.show()

# ------------------------------
# Conclusão
"""
A modelagem computacional permitiu representar visualmente o efeito de um buraco negro sobre o
espaço-tempo e a luz. Embora simplificada, esta abordagem mostra o potencial do uso do Python para
simular conceitos da relatividade geral de forma didática e acessível.
"""