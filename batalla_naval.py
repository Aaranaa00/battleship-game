from time import sleep
from sys import maxsize
from random import randint

TAMANIO_MINIMO, TAMANIO_MAXIMO = 5, 10
BARCO, BARCO_HUNDIDO  = "B", "x"
AGUA, POS_ATACADA = "~", "O"
JUGADOR_1, JUGADOR_2 = "Jugador 1", "Jugador 2"

def generar_tablero(tamanio):
    """Función que genera de 0 una matriz con un caracter"""
    return [[AGUA] * tamanio for _ in range(tamanio)]

def colocar_barcos(tablero, cant_barcos):
    """Con un parametro de la cantidad de barcos, esta función los coloca aleatoriamente"""
    posiciones_barcos = []
    cont = 0

    while cont < cant_barcos:
        coord_x = randint(0, len(tablero)-1)
        coord_y = randint(0, len(tablero)-1)
        if (coord_x, coord_y) not in posiciones_barcos:
            posiciones_barcos.append((coord_x, coord_y))
            tablero[coord_x][coord_y] = BARCO
            cont += 1
        
    return posiciones_barcos

def mostrar_tablero(tablero, ocultar_barcos = False):
    """Función que muestra el tablero, ocultando o sin ocultar los barcos"""
    for fila in range(len(tablero)):
        for colum in range(len(tablero[0])):
            if ocultar_barcos:
                if tablero[fila][colum] == BARCO:
                    print(AGUA, end=" ")
                elif tablero[fila][colum] == BARCO_HUNDIDO:
                    print(BARCO_HUNDIDO, end=" ")
                elif tablero[fila][colum] == POS_ATACADA:
                    print(POS_ATACADA, end=" ")
                else:
                    print(tablero[fila][colum], end=" ")
            else:
                print(tablero[fila][colum], end=" ")
        print()

def atacar(tablero_enem, posicion_a_atacar, tupla_posiciones):
    """Función que busca la coordenada a atacar y comprueba si toco algún barco o no"""
    if any(tupla == posicion_a_atacar for tupla in tupla_posiciones):
        ha_hundido = True
        tablero_enem[posicion_a_atacar[0]][posicion_a_atacar[1]] = BARCO_HUNDIDO
        tupla_posiciones.remove(posicion_a_atacar)
    else:
        ha_hundido = False
        tablero_enem[posicion_a_atacar[0]][posicion_a_atacar[1]] = POS_ATACADA

    return ha_hundido

def jugar(dimension, cant_barcos):
    """Main del juego, aqui se muestra por pantalla y se le da funcionalidad al juego"""
    tablero_jugador_1 = generar_tablero(dimension)
    tablero_jugador_2 = generar_tablero(dimension)
    turno_actual = ""
    cont = 0
    turnos_jugador_1, turnos_jugador_2 = 0,0
    hay_ganador = False

    #Para no repetir código, compruebo a que jugador le toca para añadirle sus correspondientes barcos
    for x in range(2):
        if x % 2 == 0:
            jugador_actual = tablero_jugador_1, JUGADOR_1
        else:
            jugador_actual = tablero_jugador_2, JUGADOR_2

        if x == 0:
            pos_barcos_jugador_1 = colocar_barcos(jugador_actual[0], cant_barcos)
        else:
            pos_barcos_jugador_2 = colocar_barcos(jugador_actual[0], cant_barcos)

        print(f"Colocando barcos para el {jugador_actual[1]}")
        sleep(1.5)

    print("\n¡Comienza la batalla naval!")
    
    while not hay_ganador:
        turno_actual = JUGADOR_1 if cont % 2 == 0 else JUGADOR_2
        posicion_elegida = (-1, -1)

        print(f"\nTurno de {turno_actual}")
        
        #Compruebo que jugador es el que juega para saber cual es el tablero actual y enemigo
        if turno_actual == JUGADOR_1:
            turnos_jugador_1 += 1
            tablero_actual = tablero_jugador_1
            tablero_enemigo = tablero_jugador_2
            posiciones_barcos = pos_barcos_jugador_2
        else:
            turnos_jugador_2 += 1
            tablero_actual = tablero_jugador_2
            tablero_enemigo = tablero_jugador_1
            posiciones_barcos = pos_barcos_jugador_1

        print("Tu tablero actual:")
        mostrar_tablero(tablero_actual)

        print("\nTablero enemigo:")
        mostrar_tablero(tablero_enemigo, True)
        print()
        
        #Valido que las coordenadas introducidas son correctas
        while posicion_elegida[0] < 0 or posicion_elegida[0] >= len(tablero_actual) or posicion_elegida[1] < 0 or posicion_elegida[1] >= len(tablero_actual[0]):
            posicion_elegida = tuple([int(x) for x in input(f"{turno_actual}, ingresa fila y columna separadas por espacio (0 - {dimension-1}): ").split()])

            if posicion_elegida[0] < 0 or posicion_elegida[0] >= len(tablero_actual) or posicion_elegida[1] < 0 or posicion_elegida[1] >= len(tablero_actual[0]):
                print("Posicion escogida incorrecta. Ingresa de nuevo")

        print("Hundido" if atacar(tablero_enemigo, posicion_elegida, posiciones_barcos) else "Atacada")

        cont += 1

        #Si no existen más coordenadas en la lista, significa que algún jugador ganó
        if len(posiciones_barcos) == 0:
            hay_ganador = True
            turnos = turnos_jugador_1 if jugador_actual == JUGADOR_1 else turnos_jugador_2
            print(f"¡{turno_actual} gana en {turnos} turnos! Todos los barcos del enemigo han sido hundidos")
            print("Gracias por jugar!. Hasta la próxima")
        
if __name__ == '__main__':
    tamanio_tablero = 0
    cantidad_barcos = maxsize

    while TAMANIO_MINIMO > tamanio_tablero or tamanio_tablero > TAMANIO_MAXIMO:
        tamanio_tablero = int(input("Introduce el tamaño del tablero (entre 5 y 10): "))

        if TAMANIO_MINIMO > tamanio_tablero or tamanio_tablero > TAMANIO_MAXIMO:
            print("Dimensión incorrecta. Ingresela de nuevo.")

    cant_barcos_max = tamanio_tablero * tamanio_tablero // 3

    while cantidad_barcos < 1 or cantidad_barcos > cant_barcos_max:
        cantidad_barcos = int(input(f"Introduce el número de barcos por jugador (máximo {cant_barcos_max}): "))

        if cantidad_barcos < 1 or cantidad_barcos > cant_barcos_max:
            print("Cantidad de barcos inválida. Ingrese de nuevo")
            
    #Antes de jugar, se debe comprobar que todos los datos introducidos son correctos
    jugar(tamanio_tablero, cantidad_barcos)