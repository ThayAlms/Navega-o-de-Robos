import math
from matplotlib import pyplot as plt

class Path:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Pontos de inicio e fim
x_inicio = 50
y_inicio = 50

x_final = 178
y_final = 138
goal = (x_final, y_final)

start = (x_inicio, y_inicio)
path = [Path(start[0], start[1])]   

#Montando a matriz obstaculo
pgmf = open('map.pgm', 'rb')
matrix = plt.imread(pgmf)
print (matrix)

matrix = 1 - (1.0 * (matrix > 220))
matriz_obstaculo = [[0] * 400 for _ in range(400)] # 0 par vazio, 40000000 para obstaculo

for i in range(400):
     for j in range(400):
         if(matrix[i][j] == 0):
            matriz_obstaculo[i][j] = 40000
         else:
            matriz_obstaculo[i][j] = 0    
              
# Criando uma matriz vazia de 400x400 para g,h,f e obstaculo

matriz_g = [[0] * 400 for _ in range(400)] #Recebe 1(Cruzinha) ou 1,4(Diagonal)
matriz_h = [[0] * 400 for _ in range(400)] #Distâncai até o objetivo final (y e x final) (cte)
matriz_obstaculo = [[0] * 400 for _ in range(400)] # 0 par vazio, 40000000 para obstaculo
matriz_f = [[0] * 400 for _ in range(400)] #Soma de g + h + obstaculo
matriz_caminho = [[" "] * 400 for _ in range(400)] #Para poder observar o caminho gerado

#FUNÇÕED PRA CHAMAR NA MAIN

def calcular_adjacentes(x_atual, y_atual):
    for i in range(max(0, x_atual - 1), min(400, x_atual + 2)):
        for j in range(max(0, y_atual - 1), min(400, y_atual + 2)): 
            # Analisa apenas os elementos adjacentes ao ponto atual
            if (i, j) != (x_atual, y_atual):
                # Define os valores de G para o ponto adjacente
                if (y_atual == j) or (x_atual == i):
                    matriz_g[i][j] = 1
                else:
                    matriz_g[i][j] = 1.4
                # Calcula a distância H para o ponto adjacente
                matriz_h[i][j] = math.sqrt((x_final - i )** 2 + (y_final - j) ** 2)
                # Calcula F considerando obstáculos
                if matrix[i][j] == 1:
                    matriz_f[i][j] = 40000
                else:
                    matriz_f[i][j] = matriz_g[i][j] + matriz_h[i][j] + matriz_obstaculo[i][j]

def calcular_diagonais(x_atual, y_atual):
    for i in [x_atual-1, x_atual+1]:
        for j in [y_atual-1, y_atual+1]:
            if 0 <= i < 400 and 0 <= j < 400:  # Verifica se a célula está dentro dos limites da matriz
                # Define os valores de G para a célula diagonal adjacente
                matriz_g[i][j] = 1.4
                # Calcula a distância H para a célula diagonal adjacente
                matriz_h[i][j] = math.sqrt((x_final - i )** 2 + (y_final - j) ** 2)
                # Calcula F considerando obstáculos
                if matrix[i][j] == 1:
                    matriz_f[i][j] = 40000
                else:
                    matriz_f[i][j] = matriz_g[i][j] + matriz_h[i][j] + matriz_obstaculo[i][j]

def menor_valor(matriz_f, x_atual, y_atual, x_final, y_final):
    menor_valor = float('inf')  # Inicialize o menor valor como infinito
    menor_x = x_atual  # Inicialize a coordenada x do menor valor com a atual
    menor_y = y_atual  # Inicialize a coordenada y do menor valor com a atual
    matriz_f[x_final][y_final] = 1
    # Loop apenas sobre as células adjacentes ao ponto atual
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:  # Verifica se não é a célula atual
                novo_x = x_atual + i
                novo_y = y_atual + j
                # Verifique se as coordenadas estão dentro dos limites da matriz
                if 0 <= novo_x < 400 and 0 <= novo_y < 400:
                    valor = matriz_f[novo_x][novo_y]
                    if valor < menor_valor:
                        menor_valor = valor
                        menor_x = novo_x
                        menor_y = novo_y
            elif(i == x_final and j == y_final):
                x_atual = menor_x
                y_atual = menor_y
    return menor_valor, menor_x, menor_y



#MAAAAAAAAAAAAAIN

x_atual = x_inicio
y_atual = y_inicio
qtd = 0

while not(x_atual== x_final and y_atual == y_final):
    matriz_caminho[x_atual][y_atual] = "█"
    # print("x_atual é:",x_atual)
    # print("y_atual é:",y_atual)
    # for linha in matriz_caminho:
    #     print(linha)
    qtd += 1
    calcular_adjacentes(x_atual,y_atual)
    calcular_diagonais(x_atual,y_atual)
    menor, x_atual, y_atual = menor_valor(matriz_f, x_atual, y_atual,x_final,y_final)
    
# Initialize the path
path = [Path(start[0], start[1])]

while path[-1].x != goal[0] or path[-1].y != goal[1]:
    matriz_caminho[path[-1].x][path[-1].y] = '*'
    calcular_adjacentes(path[-1].x, path[-1].y)
    calcular_diagonais(path[-1].x, path[-1].y)
    menor, next_x, next_y = menor_valor(matriz_f, path[-1].x, path[-1].y,x_final,y_final)
    path.append(Path(next_x, next_y))

# Visualize the path
plt.imshow(matrix, interpolation='nearest', cmap='gray')
for cell in path:
    plt.scatter(x=cell.x, y=cell.y, c='r', s=5)
plt.show()
    
    
#CASO QUEIRA VER EM PRINT NO TERMINAL  
    
# print("--------------------------------------------------------------------------------------------")
# print("CHEGUEI!!!!!!!!!!!!!!!!! ")
# print("x_atual é:",x_atual)
# print("y_atual é:",y_atual)
# print("Quantidade de passos até o final:", qtd)
# for linha in matriz_caminho:
#     print(linha)

