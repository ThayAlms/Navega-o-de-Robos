import math
from random import randrange
from matplotlib import pyplot as plt
import numpy as np

#Pontos de inicio e fim
x_inicio = 40
y_inicio = 40
start = (x_inicio, y_inicio)

x_final = 250
y_final = 250
goal = (x_final, y_final)

#1 metro = 20 pixel
grid_maximo = 401
colunas = 401
linhas = 401

caminho_aberto = 1
obstaculo = 0

# Montando matrix do fafa
pgmf = open('map.pgm', 'rb')
matrix = plt.imread(pgmf)

matrix = (1.0 * (matrix > 220))

class NodoArvore:
    def __init__ (self,chave = None, pai = None, x=None,y=None):
        self.id = chave
        self.pai = pai
        self.filhos = []
        self.x = x
        self.y = y
        
    def chegou(self,x,y,raio):
        dist = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        if dist < raio:
            return True
        else:
            return False
    
id_atual = 0
raiz = NodoArvore(id_atual,None,x_inicio,y_inicio)
id_atual += 1
final = NodoArvore(id_atual,None,x_final,y_final)
id_atual += 1


# Nodos disponiveis para comparação
nodes = [
    NodoArvore(None, None, x_inicio, y_inicio),
    NodoArvore(None, None, x_final, y_final)
]

# --------------------------------------------------------------------------------------------------------------------------------------
def CoordenadaPoda(x_aleatorio,y_aleatorio,proximo_x,proximo_y):
    dist_x_maior = abs(proximo_x - x_aleatorio)
    dist_y_maior = abs(proximo_y - y_aleatorio)

    if dist_x_maior == 0:
        dist_x_maior = 1  # Evitar divisão por zero

    if dist_y_maior == 0:
        dist_y_maior = 1  # Evitar divisão por zero

    hipotenusa_maior = math.sqrt(dist_x_maior**2 + dist_y_maior**2)

    x_triangulo_menor = (20 * dist_x_maior) // hipotenusa_maior
    y_triangulo_menor = (20 * dist_y_maior) // hipotenusa_maior

    coordenada_x = abs(x_triangulo_menor - x_aleatorio)
    coordenada_y = abs(y_triangulo_menor - y_aleatorio)

    return coordenada_x, coordenada_y


def NodoProximo(nodes,nodo_aleatorio, matrix):
    menor_distancia = float('inf')
    nodo_proximo = None
    proximo_x, proximo_y = None, None

    for node in nodes:
        distancia = math.sqrt((node.x - nodo_aleatorio.x)**2 + (node.y - nodo_aleatorio.y)**2)
        if distancia < menor_distancia:
            menor_distancia = distancia
            nodo_proximo = node
    
    proximo_x = nodo_proximo.x
    proximo_y = nodo_proximo.y
            
    return nodo_proximo, proximo_x, proximo_y
# --------------------------------------------------------------------------------------------------------------------------------------
while True:
    x_aleatorio = randrange(grid_maximo)
    y_aleatorio = randrange(grid_maximo)
    nodo_aleatorio = NodoArvore(None,None,x_aleatorio,y_aleatorio) #   
    nodo_proximo,proximo_x,proximo_y = NodoProximo(nodes,nodo_aleatorio,matrix) #
    x_poda,y_poda = CoordenadaPoda(x_aleatorio,y_aleatorio,proximo_x,proximo_y) #
    nodo_novo = NodoArvore(id_atual,nodo_proximo.id,x_poda,y_poda)###########
    nodes.append(nodo_novo)
    nodo_proximo.filhos.append(nodo_novo)
    id_atual += 1
    if(nodo_novo.chegou(x_final, y_final, 20)):
        break
    
path = []
nodo = nodo_novo

while True:
    nodo = nodo.pai
    print(nodo)
    if nodo is None:
        break
    path.append(nodo)

    
# Visualize the path
plt.imshow(matrix, interpolation='nearest', cmap='gray')

# Plot the start and end points
plt.scatter(x_inicio, y_inicio, color='green', marker='o', label='Start')
plt.scatter(x_final, y_final, color='red', marker='o', label='Goal')

# Plot the path
x_path = [n.x for n in path]
y_path = [n.y for n in path]
plt.plot(x_path, y_path, color='blue', linestyle='-', linewidth=2, label='Path')

plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('RRT Path')
plt.show()
