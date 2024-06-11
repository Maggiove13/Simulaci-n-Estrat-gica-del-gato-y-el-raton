# Importamos las librerias
import numpy as np # Para crear arreglos y matrices
import tkinter as tk # Para crear la interfaz grafica
import time # Para darle tiempo de espera y se muestren los movimientos en pantalla
import random # Para randomizar las ubicaciones de los personajes
import math # Para usar raiz cuadrada en la distancia Euclidiana la funcion "sqrt"

#Paso 1: Crear el tablero
tablero_fila = 5
tablero_columna = 5

tablero = np.zeros((tablero_fila, tablero_columna), dtype=int)

# Paso 2: Definir posiciones iniciales del gato y el raton
pos_raton = (random.randint(0, 4), random.randint(0, 4))

# Función para verificar la distancia
def distancia(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Asignar una posición inicial al gato que esté a tres casillas de distancia del ratón
pos_gato = (random.randint(0, 4), random.randint(0, 4))
while distancia(pos_raton, pos_gato) < 3:
    pos_gato = (random.randint(0, 4), random.randint(0, 4))


# Paso 3: Define los posibles movimientos de los personajes
def movimientos_posibles_gato(ubi, ultima_ubi):
    """Movimientos posibles del Gato"""
    x, y = ubi # Desempaquetar la posición actual del ratón en coordenadas x e y
    movimientos_posibles = [] # Inicializar una lista para almacenar los movimientos válidos
    direcciones =  [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # arriba, abajo, izquierda, derecha

    for dx, dy in direcciones: # Iterar sobre cada dirección posible
        nueva_ubi = (x + dx, y + dy) # Calcular la nueva posición sumando la dirección a las coordenadas actuales
        if distancia(ubi, pos_raton) < 3 and (dx, dy) in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            movimientos_posibles.insert(0, nueva_ubi)  # Priorizar movimientos diagonales cuando el raton este cerca
        else:
            movimientos_posibles.append(nueva_ubi)
            if 0 <= nueva_ubi[0] < tablero_fila  and 0 <= nueva_ubi[1] < tablero_columna and nueva_ubi != ultima_ubi:
                movimientos_posibles.append(nueva_ubi) # Si es válida, agregarla a la lista de movimientos posibles

    return movimientos_posibles

def movimientos_posibles_raton(ubi, ultima_ubi, pos_gato):
    """Movimientos posibles del Raton"""
    x, y = ubi  # Desempaquetar la posición actual del ratón en coordenadas x e y
    movimientos_posibles = []  # Inicializar una lista para almacenar los movimientos válidos
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Definir las posibles direcciones de movimiento: arriba, abajo, izquierda, derecha

    if ubi in [(0, 0), (0, 4), (4, 0), (4, 4)]:
        # Si el ratón está en una esquina, mover tres casillas
        for dx, dy in direcciones:
            nueva_ubi = (x + 3 * dx, y + 3 * dy)
            if 0 <= nueva_ubi[0] < tablero_fila and 0 <= nueva_ubi[1] < tablero_columna and nueva_ubi != ultima_ubi and nueva_ubi != pos_gato:
                movimientos_posibles.append(nueva_ubi)
    else:
        # Si el ratón no está en una esquina, mover una casilla
        for dx, dy in direcciones:
            nueva_ubi = (x + dx, y + dy)
            if 0 <= nueva_ubi[0] < tablero_fila and 0 <= nueva_ubi[1] < tablero_columna and nueva_ubi != ultima_ubi and nueva_ubi != pos_gato:
                movimientos_posibles.append(nueva_ubi)
    
    # Eliminar movimientos adyacentes al gato, si hay otras opciones disponibles
    movimientos_no_adyacentes = [] #Esta lista se usará para almacenar movimientos que no son adyacentes al gato.
    for m in movimientos_posibles: # Iterar sobre cada movimiento en la lista "movimientos_posibles" para valuar cada movimiento para verificar si es adyacente al gato.
        if not (abs(m[0] - pos_gato[0]) <= 1 and abs(m[1] - pos_gato[1]) <= 1): #Verificar si un movimiento no es adyacente al gato.
            movimientos_no_adyacentes.append(m) #Si el movimiento no es adyacente al gato, se agrega a la lista movimientos_no_adyacentes.
    #  Verificar si hay movimientos no adyacentes al gato en la lista "movimientos_no_adyacentes".
    if movimientos_no_adyacentes:
    ##Si hay movimientos en movimientos_no_adyacentes, reemplazar movimientos_posibles con movimientos_no_adyacentes
        movimientos_posibles = movimientos_no_adyacentes #Esto asegura que el ratón prefiera movimientos no adyacentes al gato si hay disponibles.

    return movimientos_posibles #Devolver la lista actualizada de movimientos posibles.


# Paso 4: Definir la funcion de evaluacion del gato y el raton
def evaluacion_gato(pos_gato, pos_raton):
    """Calcula la distancia minima entre el ratón y el gato"""
    min_distancia = min(abs(pos_raton[0] - pos_gato[0]), abs(pos_raton[1] - pos_gato[1]))
    return min_distancia

def evaluacion_raton(pos_raton, pos_gato):
    """Calcula la distancia máxima entre el ratón y el gato"""
    max_distancia = max(abs(pos_raton[0] - pos_gato[0]), abs(pos_raton[1] - pos_gato[1]))
    return max_distancia


# Paso 5: Implementar el algoritmo minimax
def minimax(pos_gato, pos_raton, es_turno_raton, profundidad, ultima_ubi_gato, ultima_ubi_raton):
    if pos_gato == pos_raton or profundidad == 0:
        if es_turno_raton:
            return evaluacion_raton(pos_raton, pos_gato), pos_raton #Devuelve tanto el valor de la evaluación (que es un número entero) como la posición actual del raton (una coordenada).
        else:
            return evaluacion_gato(pos_gato, pos_raton), pos_gato #Devuelve tanto el valor de la evaluación (que es un número entero) como la posición actual del raton (una coordenada).

    if es_turno_raton:
        max_eval = float('-inf')
        mejor_movimiento = pos_raton
        for movimiento in movimientos_posibles_raton(pos_raton, ultima_ubi_raton, pos_gato):
            # La función minimax devuelve una tupla:
            # Primera Parte de la Tupla: La evaluación (un número entero o flotante)
            # Segunda Parte de la Tupla: La posición (una coordenada).
            nueva_eval, posicion_evaluada = minimax(pos_gato, movimiento, False, profundidad - 1, ultima_ubi_gato, pos_raton)
            if nueva_eval > max_eval:
                max_eval = nueva_eval
                mejor_movimiento = movimiento
        return max_eval, mejor_movimiento
    else:
        min_eval = float('inf')
        mejor_movimiento = pos_gato
        for movimiento in movimientos_posibles_gato(pos_gato, ultima_ubi_gato):
            # La función minimax devuelve una tupla:
            # Primera Parte de la Tupla: La evaluación (un número entero o flotante)
            # Segunda Parte de la Tupla: La posición (una coordenada).
            nueva_eval, posicion_evaluada = minimax(movimiento, pos_raton, True, profundidad - 1, pos_gato, ultima_ubi_raton)
            if nueva_eval < min_eval:
                min_eval = nueva_eval
                mejor_movimiento = movimiento
        return min_eval, mejor_movimiento

# Paso 7: Crear la interfaz con Canvas
def crear_interfaz(actualizar_tablero, pos_raton, pos_gato):
    ventana = tk.Tk()
    ventana.title("Juego de Gato y Ratón")
    ventana.geometry("520x520")
    canvas = tk.Canvas(ventana, width=500, height=500, bg="white")
    canvas.pack()

    for i in range(1, 5):
        canvas.create_line(i * 100, 0, i * 100, 500, fill="black")
        canvas.create_line(0, i * 100, 500, i * 100, fill="black")

    actualizar_tablero(canvas, pos_raton, pos_gato)
    ventana.update()
    return ventana, canvas

# Paso 8: Funcion para actualizar la interfaz
def actualizar_tablero(canvas, pos_raton, pos_gato):
    canvas.delete("all")
    for i in range(1, 5):
        canvas.create_line(i * 100, 0, i * 100, 500, fill="black")
        canvas.create_line(0, i * 100, 500, i * 100, fill="black")

    x_raton, y_raton = pos_raton
    x_gato, y_gato = pos_gato 
    # Que muestre a la celda con el raton
    canvas.create_text(y_raton * 100 + 50, x_raton * 100 + 50, text="🐭", font=("Arial", 32), tag="raton")
    # Que muestre a la celda con el gato
    canvas.create_text(y_gato * 100 + 50, x_gato * 100 + 50, text="😼", font=("Arial", 32), tag="gato")

# Paso 9: Ciclo del juego
def jugar(actualizar_tablero, ventana, pos_raton, pos_gato):
    turno_raton = True  # Empieza con el turno del raton
    profundidad = 3 # Definimos la profundidad de busqueda
    contador_movimientos_gato = 0 # Contador de los movimientos del gato
    ultima_ubi_raton = None  # Almacena la última posición del ratón.
    ultima_ubi_gato = None  # Almacena la última posición del gato.

    while True:
        ventana.update()
    
        if turno_raton:
            movimientos_raton = movimientos_posibles_raton(pos_raton, ultima_ubi_raton, pos_gato)
            if movimientos_raton:
                posicion_evaluada, mejor_movimiento_raton = minimax(pos_gato, pos_raton, True, profundidad, ultima_ubi_gato, ultima_ubi_raton)
                ultima_ubi_raton = pos_raton
                pos_raton = mejor_movimiento_raton
            print(f"La posición del ratón es {pos_raton}")
            actualizar_tablero(canvas, pos_raton, pos_gato)
            turno_raton = False
            ventana.update()
            time.sleep(1)
        else:
            posicion_evaluada, mejor_movimiento_gato = minimax(pos_gato, pos_raton, False, profundidad, ultima_ubi_gato, ultima_ubi_raton)
            ultima_ubi_gato = pos_gato
            pos_gato = mejor_movimiento_gato
            print(f"La posición del gato es {pos_gato}")
            actualizar_tablero(canvas, pos_raton, pos_gato)
            ventana.update()
            time.sleep(1)
            contador_movimientos_gato += 1
            print(contador_movimientos_gato)
            if pos_gato == pos_raton or contador_movimientos_gato >= 6:
                if pos_gato == pos_raton:
                    print("¡El gato atrapó al ratón!")
                else:
                    print("¡El ratón escapó del gato!")
                break
            turno_raton = True
            ventana.update()

# Paso 10: Llamar a las funciones para iniciar el juego
ventana, canvas = crear_interfaz(actualizar_tablero, pos_raton, pos_gato)
jugar(actualizar_tablero, ventana, pos_raton, pos_gato)

ventana.mainloop
