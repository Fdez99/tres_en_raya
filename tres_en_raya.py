### Tres en Raya ###
import random

victorias = 0
derrotas = 0
empates = 0

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
simbolicos = ['#', '*', '9', 'ç', '$', '€', '!', 'j', '+', 'º', '?', '@', '&', '%']

# Pedir al jugador si quiere jugar con X o con O
ficha = (input('Elige X u O: ')).upper()
if ficha == 'X':
    ficha_maq = 'O'
elif ficha == 'O':
    ficha_maq = 'X'
else:
    print("\033[1;33m" + "Un rebelde. Eso me gusta. 😈" + '\033[0;m')
    ficha = ficha
    ficha_maq = random.choice(simbolicos)
    while ficha_maq == ficha:
        ficha_maq = random.choice(simbolicos)


def jugar(board):
    global victorias, derrotas, empates
    inicial = jugador_inicial()

    while True:
        if inicial == 'jugador':
            muestra_tablero(board)
            entra_movimiento(board)
            muestra_tablero(board)

            if victoria_para(board, ficha):
                print("\033[1;32m" + "¡¡Has ganado!! 🥳" + '\033[0;m')
                victorias += 1
                break
            if not lista_de_pos_vacias(board):
                print("\033[1;36m" + "Empate. 😐" + '\033[0;m')
                empates += 1
                break
            print("\033[1;35m"+f"Casillas libres: {casillas_libres(board)}"+'\033[0;m')

            dibuja_movimiento_maquina(board)
            if victoria_para(board, ficha_maq):
                print("\033[1;31m" + "Ja, ja, has perdido 😝" + '\033[0;m')
                derrotas += 1
                break
            if not lista_de_pos_vacias(board):
                print("\033[1;36m" + "Empate. 😐" + '\033[0;m')
                empates += 1
                break
            print("\033[1;35m"+f"Casillas libres: {casillas_libres(board)}"+'\033[0;m')

        else:
            dibuja_movimiento_maquina(board)
            if victoria_para(board, ficha_maq):
                print("\033[1;31m" + "Ja, ja, has perdido 😝" + '\033[0;m')
                derrotas += 1
                break
            if not lista_de_pos_vacias(board):
                print("\033[1;36m" + "Empate. 😐" + '\033[0;m')
                empates += 1
                break
            print("\033[1;35m"+f"Casillas libres: {casillas_libres(board)}"+'\033[0;m')

            entra_movimiento(board)
            muestra_tablero(board)
            if victoria_para(board, ficha):
                print("\033[1;32m" + "¡¡Has ganado!! 🥳" + '\033[0;m')
                victorias += 1
                break
            if not lista_de_pos_vacias(board):
                print("\033[1;36m" + "Empate. 😐" + '\033[0;m')
                empates += 1
                break
            print("\033[1;35m"+f"Casillas libres: {casillas_libres(board)}"+'\033[0;m')

    registrar_resultados()
    mostrar_marcador()



########################
# Funciones auxiliares #
########################

def jugador_inicial():
    """ Elige aleatoriamente quién empieza """
    jug_ini = random.choice(['jugador', 'máquina'])
    if jug_ini == 'jugador':
        print("\033[1;33m" + "¡Empiezas tú! 😀" + '\033[0;m')
    else:
        print("\033[1;33m" + "Empiezo yo 🤖" + '\033[0;m')
    return jug_ini


def muestra_tablero(board):
    """ Muestra el tablero en consola """
    for i in range(3):
        print(board[i][0], '|', board[i][1], '|', board[i][2])
        if i != 2:
            print('--+---+--')
    return board


def lista_de_pos_vacias(board):
    """ Devuelve las posiciones libres """
    vacios = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                vacios.append([i, j])
    return vacios

# ---- Traducción de posiciones vacías al número de casilla --
def casillas_libres(board):
    pos = {(0, 0): 1, (0, 1): 2, (0, 2): 3,
           (1, 0): 4, (1, 1): 5, (1, 2): 6,
           (2, 0): 7, (2, 1): 8, (2, 2): 9}
    
    libres = []
    for casilla in lista_de_pos_vacias(board):
        libres.append(pos[tuple(casilla)])
    return libres


def entra_movimiento(board):
    """ Registra el movimiento del jugador """
    posiciones = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2)
    }
    try:
        mov_jugador = int(input("\033[1;34m" + "Número de casilla (1-9): " + '\033[0;m'))
        if mov_jugador not in posiciones:
            print("\033[1;35m" + "Introduce un número del 1 al 9" + '\033[0;m')
            entra_movimiento(board)
            return

        h, v = posiciones[mov_jugador]
        if board[h][v] != ' ':
            print("\033[1;36m" + "Posición ocupada. Elige otra, anda." + '\033[0;m')
            entra_movimiento(board)
        else:
            board[h][v] = ficha
    except:
        print("\033[1;35m" + "Introduce un número válido" + '\033[0;m')
        entra_movimiento(board)


def victoria_para(board, ficha):
    pos = {(0, 0): 1, (0, 1): 2, (0, 2): 3,
           (1, 0): 4, (1, 1): 5, (1, 2): 6,
           (2, 0): 7, (2, 1): 8, (2, 2): 9}
    victorias = [
        {1, 2, 3}, {4, 5, 6}, {7, 8, 9},
        {1, 4, 7}, {2, 5, 8}, {3, 6, 9},
        {1, 5, 9}, {3, 5, 7}
    ]

    jugadas = {pos[(i, j)] for i in range(3) for j in range(3) if board[i][j] == ficha}
    return any(v.issubset(jugadas) for v in victorias)


def evaluar_estado(board):
    if victoria_para(board, ficha_maq):
        return 1
    elif victoria_para(board, ficha):
        return -1
    elif not lista_de_pos_vacias(board):
        return 0
    return None


def minimax(board, es_max):
    estado = evaluar_estado(board)
    if estado is not None:
        return estado

    if es_max:
        mejor = -float('inf')
        for pos in lista_de_pos_vacias(board):
            board[pos[0]][pos[1]] = ficha_maq
            val = minimax(board, False)
            board[pos[0]][pos[1]] = ' '
            mejor = max(mejor, val)
        return mejor
    else:
        mejor = float('inf')
        for pos in lista_de_pos_vacias(board):
            board[pos[0]][pos[1]] = ficha
            val = minimax(board, True)
            board[pos[0]][pos[1]] = ' '
            mejor = min(mejor, val)
        return mejor

def dibuja_movimiento_maquina(board):
    """ Movimiento según algoritmo minimax """
    mejor_valor = -float('inf')
    mejor_jugada = None

    for pos in lista_de_pos_vacias(board):
        board[pos[0]][pos[1]] = ficha_maq
        val = minimax(board, False)
        board[pos[0]][pos[1]] = ' '
        if val > mejor_valor:
            mejor_valor = val
            mejor_jugada = pos

    if mejor_jugada:
        board[mejor_jugada[0]][mejor_jugada[1]] = ficha_maq
        print(f"\033[1;33mHe jugado en la casilla {mejor_jugada[0]*3 + mejor_jugada[1] + 1}\033[0;m")
        muestra_tablero(board)

def victoria_para(board, ficha):
    """ Comprueba si la ficha ha ganado """
    posiciones = {
        (0, 0): 1, (0, 1): 2, (0, 2): 3,
        (1, 0): 4, (1, 1): 5, (1, 2): 6,
        (2, 0): 7, (2, 1): 8, (2, 2): 9
    }
    victorias = (
        {1, 2, 3}, {4, 5, 6}, {7, 8, 9},
        {1, 4, 7}, {2, 5, 8}, {3, 6, 9},
        {1, 5, 9}, {3, 5, 7}
    )

    casillas_ficha = set()
    for fila in range(3):
        for col in range(3):
            if board[fila][col] == ficha:
                casillas_ficha.add(posiciones[(fila, col)])

    for vic in victorias:
        if vic.issubset(casillas_ficha):
            return True
    return False


def registrar_resultados():
    """ Guarda el resultado en un archivo .csv """
    with open('3enraya_resultados.csv', 'a+') as resultados:
        resultados.writelines(f'{victorias}, {derrotas}, {empates}\n')



def mostrar_marcador():
    print("\n\033[1;36m" + "Marcador actual:" + '\033[0;m')
    print(f"\033[1;32mVictorias: {victorias}\033[0;m")
    print(f"\033[1;31mDerrotas: {derrotas}\033[0;m")
    print(f"\033[1;33mEmpates: {empates}\033[0;m")


def reiniciar_tablero():
    return [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]


###########################

# Iniciar el juego ▶
while True:
    board = reiniciar_tablero()
    jugar(board)
    
    respuesta = input("\n¿Echamos otra? (s/n): ").lower()
    if respuesta != 's':
        print("\n\033[1;36m¡Enga, taluego! 😄\033[0;m")
        break
