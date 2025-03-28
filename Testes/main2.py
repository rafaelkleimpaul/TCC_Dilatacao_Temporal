import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact, FloatSlider

# Constantes
G = 6.67430e-11
c = 3e8
massa_solar = 1.989e30

# Função para calcular o raio de Schwarzschild
def raio_schwarzschild(m):
    return 2 * G * m / c**2

# Função principal com múltiplos sliders
@interact(
    massas_solares=FloatSlider(value=5, min=1, max=50, step=1, description='Massa (M☉)'),
    distancia_rs=FloatSlider(value=5, min=1.01, max=20, step=0.5, description='Distância (Rs)'),
    escala=FloatSlider(value=1.0, min=0.1, max=2.0, step=0.1, description='Escala')
)
def visualizar_completa(massas_solares, distancia_rs, escala):
    massa = massas_solares * massa_solar
    rs = raio_schwarzschild(massa)

    print(f"➡ Massa: {massas_solares:.1f} M☉")
    print(f"➡ Raio de Schwarzschild: {rs:.2e} m")
    print(f"➡ Distância analisada: {distancia_rs:.2f} Rs\n")

    # Geração de malha
    x = np.linspace(-10, 10, 100) * escala
    y = np.linspace(-10, 10, 100) * escala
    X, Y = np.meshgrid(x, y)
    Z = -rs / np.sqrt(X**2 + Y**2 + rs**2)

    # Curvatura do espaço-tempo
    fig = plt.figure(figsize=(14, 5))
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='plasma')
    ax1.set_title("Curvatura do Espaço-Tempo")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("Curvatura")

    # Dilatação do tempo
    r = np.linspace(1.01*rs, distancia_rs*rs, 500)
    dilatacao = np.sqrt(1 - rs/r)

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(r / rs, dilatacao)
    ax2.set_title("Dilatação Temporal")
    ax2.set_xlabel("Distância (em múltiplos de Rs)")
    ax2.set_ylabel("Fator de tempo")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()