# inicio

import pygame  # Importamos la librería Pygame.
import constantes  # Importamos las constantes del juego.
from personaje import Personaje  # Importamos la clase del personaje.

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("S.E.A - Story Entertainment Adventure")

# Configuración del reloj para controlar los FPS
clock = pygame.time.Clock()

#lista de imagenes 
imagenes_personaje = ["camina1.png", "camina2.png", "camina3.png", "camina4.png"]

# Crear el personaje en una posición inicial
personaje = Personaje(50, 50, imagenes_personaje)

# Bucle principal del juego
jugando = True
while jugando:
    clock.tick(constantes.FPS)  # Controla la velocidad del juego

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    # Captura de teclas presionadas
    teclas = pygame.key.get_pressed()
    personaje.mover(teclas)  # Movimiento del personaje
    
  
    
    # Dibujar en pantalla
    ventana.fill(constantes.VERDE)  # Establecer fondo de color verde
    personaje.dibujar(ventana)  # Dibujar el personaje en la pantalla

    pygame.display.flip()  # Actualiza la pantalla

pygame.quit()
