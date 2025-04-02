# generar_items
import pygame
import random
from items import Item
import constantes

def generar_monedas(cantidad, animacion_list, ancho_mapa, alto_mapa):
    """Genera monedas en posiciones aleatorias dentro del mapa."""
    grupo_monedas = pygame.sprite.Group()  # Crear un nuevo grupo para las monedas

    for _ in range(cantidad):
        x = random.randint(0, constantes.COLUMNAS * constantes.CUADRICULA_TAMAÑO - constantes.ANCHO_MONEDA)  # Posición aleatoria en X
        y = random.randint(0, constantes.FILAS * constantes.CUADRICULA_TAMAÑO - constantes.ALTO_MONEDA)  # Posición aleatoria en Y
        print(f"Moneda en: ({x}, {y})")  # Depuración
        moneda = Item(x, y, animacion_list)
        grupo_monedas.add(moneda)

    return grupo_monedas  # Retorna el grupo de monedas generado
