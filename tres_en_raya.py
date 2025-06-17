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

            dibuja_movimiento_maquina(board)
            if victoria_para(board, ficha_maq):
                print("\033[1;31m" + "Ja, ja, has perdido 😝" + '\033[0;m')
                derrotas += 1
                break
            if not lista_de_pos_vacias(board):
                print("\033[1;36m" + "Empate. 😐" + '\033[0;m')
                empates += 1
                break

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

    registrar_resultados()
    mostrar_marcador()



#######################
# Funciones auxiliares
#######################

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


def dibuja_movimiento_maquina(board):
    """ Movimiento aleatorio de la máquina """
    disponibles = lista_de_pos_vacias(board)
    if not disponibles:
        return
    elegido = random.choice(disponibles)
    board[elegido[0]][elegido[1]] = ficha_maq
    return muestra_tablero(board)


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
    """ Guarda el resultado en un archivo CSV """
    with open('3enraya_resultados.csv', 'a+') as resultados:
        resultados.write(f'{victoria_para(board, ficha)}, {victoria_para(board, ficha_maq)}, {victorias}, {derrotas}, {empates}\n')



def mostrar_marcador():
    print("\n\033[1;36m" + "Marcador actual:" + '\033[0;m')
    print(f"\033[1;32mVictorias: {victorias}\033[0;m")
    print(f"\033[1;31mDerrotas: {derrotas}\033[0;m")
    print(f"\033[1;33mEmpates: {empates}\033[0;m")


def reiniciar_tablero():
    return [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]




# Iniciar el juego ▶
while True:
    board = reiniciar_tablero()
    jugar(board)
    
    respuesta = input("\n¿Quieres jugar otra partida? (s/n): ").lower()
    if respuesta != 's':
        print("\n\033[1;36mGracias por jugar. ¡Hasta la próxima!\033[0;m")
        break
