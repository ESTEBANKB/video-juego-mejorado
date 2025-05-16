#gato_humaono

# Importamos las librerías necesarias
import pygame
from humano import NPCHumano  # Importamos la clase del NPC humano desde el archivo humano.py
import constantes  # Importamos el archivo donde están definidas las constantes globales

# Función para cargar las imágenes del gato en diferentes direcciones
def cargar_imagenes_gato():
    # Diccionario que guarda listas de imágenes para cada dirección de movimiento y una imagen para cuando está quieto
    imagenes = {
        "abajo": [pygame.image.load(f"recursos/imagenes/caracteres/gato/gabajo_{i}.png") for i in range(1, 4)],
        "arriba": [pygame.image.load(f"recursos/imagenes/caracteres/gato/garriba_{i}.png") for i in range(1, 4)],
        "izquierda": [pygame.image.load(f"recursos/imagenes/caracteres/gato/gizquierda_{i}.png") for i in range(1, 4)],
        "derecha": [pygame.image.load(f"recursos/imagenes/caracteres/gato/gderecha_{i}.png") for i in range(1, 4)],
        "quieto": pygame.image.load("recursos/imagenes/caracteres/gato/gquieto.png")  # Imagen estática del gato quieto
    }

    # Escalamos todas las imágenes al tamaño definido por la cuadrícula del juego
    for direccion in imagenes:
        if isinstance(imagenes[direccion], list):  # Si es una lista (animación)
            # Escalamos cada imagen de la lista
            imagenes[direccion] = [
                pygame.transform.scale(img, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
                for img in imagenes[direccion]
            ]
        else:
            # Si es solo una imagen (gato quieto), la escalamos
            imagenes[direccion] = pygame.transform.scale(
                imagenes[direccion], (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO)
            )

    # Retornamos el diccionario completo con las imágenes escaladas
    return imagenes

# Función para crear un NPC humano en una posición específica
def crear_npc_humano():
    # Cargamos la imagen del personaje humano desde los recursos
    imagen = pygame.image.load("recursos/imagenes/caracteres/humano/humanoo.png")
    
    # Escalamos la imagen al tamaño de la cuadrícula
    imagen = pygame.transform.scale(imagen, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
    
    # Creamos y devolvemos una instancia del NPC humano, con su posición inicial y texto de bienvenida
    return NPCHumano(
        800, 680, imagen,
        "¡Hola! Bienvenido a la isla. Ayuda al gato a encontrar a sus amigos perdidos."
    )
