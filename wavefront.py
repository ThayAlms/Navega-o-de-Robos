from collections import deque
from matplotlib import pyplot as plt

# Tamanho da matriz
linhas = 400
colunas = 400

class Path:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Pontos de inicio e fim
x_inicio = 10
y_inicio = 10

x_final = 50
y_final = 50

goal = (x_final, y_final)
start = (x_inicio, y_inicio)
path = [Path(start[0], start[1])]   

caminho_aberto = 1
obstaculo = 0

# Montando matrix do fafa
pgmf = open('map.pgm', 'rb')
matrix = plt.imread(pgmf)

matrix = (1.0 * (matrix > 220))

# Inicializa a matriz com zeros
matriz = [[0] * colunas for _ in range(linhas)]
matriz_caminho = [[0] * colunas for _ in range(linhas)]

matriz[x_final][y_final] = 2
matriz[x_inicio][y_inicio] = 1

# Fila para a busca em largura
fila = deque([(x_final, y_final)])

# Wavefront
while fila:
    x, y = fila.popleft()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            i, j = x + dx, y + dy
            if 0 <= i < linhas and 0 <= j < colunas and matriz[i][j] == 0:
                matriz[i][j] = matriz[x][y] + 1
                fila.append((i, j))
            if (i, j) == (x_inicio, y_inicio):
                fila.clear()  # Limpa a fila para encerrar o loop   
                break  # Sai do loop for interno
        else:
            continue  # Continua o loop while sem executar o else
        break  # Sai do loop for externo se o ponto inicial foi alcançado

# Para garantir que a célula inicial permaneça com o valor 1
matriz[x_final][y_final] = 2
matriz[x_inicio][y_inicio] = 1

x_atual, y_atual = x_inicio, y_inicio
def menor_valor(x_atual, y_atual, x_final, y_final,matriz):
    menor_valor = float('inf')
    prox_x, prox_y = x_atual, y_atual
    
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            novo_x = x_atual + dx
            novo_y = y_atual + dy
            if (dx, dy) != (0, 0) and 0 <= novo_x < linhas and 0 <= novo_y < colunas and matriz[novo_x][novo_y] > 0:  #and matrix{novo_x}[novo_y] == caminho_aberto
                valor = matriz[novo_x][novo_y]
                if valor < menor_valor:
                    menor_valor = valor
                    prox_x, prox_y = novo_x, novo_y
                if (novo_x, novo_y) == (x_final, y_final):
                    return novo_x, novo_y  # Return the goal coordinates directly
    
    return prox_x, prox_y


matriz[x_inicio][y_inicio] = float('inf')
while not(x_atual== x_final and y_atual == y_final):
    pros_x,pros_y = menor_valor(x_atual, y_atual, x_final, y_final,matriz)
    matriz_caminho[pros_x][pros_y] = "*"
    x_atual = pros_x
    y_atual = pros_y
    path.append(Path(x_atual,y_atual))
    
    
# Extract path coordinates ensuring they are within the matrix boundaries
path_x = [min(max(cell.x, 0), linhas - 1) for cell in path]
path_y = [min(max(cell.y, 0), colunas - 1) for cell in path]

# Visualize the path
 plt.imshow(matrix, interpolation='nearest', cmap='gray') 
plt.plot(path_y, path_x, color='yellow', linewidth=2)
plt.show()
