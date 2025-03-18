# inicio

import pygame  # Importamos la librería Pygame.
import constantes  # Importamos las constantes del juego.
from personaje import Personaje  # Importamos la clase del personaje.
from imagen import escalar_img # Importamos la función para escalar imágenes.
from items import Item  # Importamos la clase de los items.
from mundo import Mundo  # Importamos la clase del mundo.
import os

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("S.E.A - Saving species on an adventure")

# Configuración del reloj para controlar los FPS
clock = pygame.time.Clock()
# Definir la fuente de texto
fuente = pygame.font.Font(None, 36)  # Fuente predeterminada de Pygame, tamaño 36

# Función para dibujar texto en pantalla
def dibujar_texto(texto,fuente, x, y, color):
    img=fuente.render(texto,True, color)
    ventana.blit(img, (x, y))


#lista de imagenes 
imagenes_personaje = ["camina1.png", "camina2.png", "camina3.png", "camina4.png"]
#imagenes monedas 

# Crear el personaje en una posición inicial
personaje = Personaje(50, 50, imagenes_personaje)

#cargas imagenes del mundo
tile_list= []
ruta_mundo = os.path.join("recursos", "imagenes", "caracteres", "tiles")

if os.path.exists(ruta_mundo):
    for x in range(constantes.TILE_TYPES):  
        tile_image = pygame.image.load(os.path.join(ruta_mundo, f"tiles_{x+1}.png"))
        tile_image = pygame.transform.scale(tile_image, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
        tile_list.append(tile_image)



# Cargar imágenes de las monedas
coin_images = []
ruta_img = os.path.join("recursos", "imagenes", "caracteres", "monedas")

if os.path.exists(ruta_img):
    for i in range(9):
        img = pygame.image.load(os.path.join(ruta_img, f"monedas_{i+1}.png"))
        img = pygame.transform.scale(img, (constantes.ANCHO_MONEDA,constantes.ALTO_MONEDA))
        coin_images.append(img)
        img.set_colorkey((constantes.COLOR_TRANSPARENTE))  # Elimina el blanco de fondo si es necesario
        coin_images.append(img)
        
# Crear una moneda y agregarla al grupo
grupo_item = pygame.sprite.Group()
moneda = Item(350, 25,coin_images)
grupo_item.add(moneda)

word_data=[
    [26,4,4,4,4,4,4,4,4,4,4,8,4,4,4,4],
    [2,4,22,4,4,4,4,4,4,19,19,19,24,19,19,19],
    [2,4,4,22,4,4,4,4,4,4,4,4,4,4,4,4],
    [2,4,4,4,4,4,4,4,4,4,4,4,8,4,4,4],
    [2,4,4,4,4,2,4,4,4,4,4,4,4,4,4,4],
    [0,23,23,23,23,0,23,4,4,4,4,4,4,4,4,15],
    [2,4,4,4,4,2,4,24,4,4,4,4,4,4,4,27],
    [2,4,4,4,4,2,28,4,4,4,4,4,4,8,4,15],
    [2,4,4,4,4,2,28,4,4,4,4,4,4,4,4,27],
    [4,4,4,4,4,2,28,4,4,4,4,4,8,4,4,27],
    [4,8,4,4,4,4,4,4,4,4,4,4,4,4,4,27],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,27]

]

world = Mundo()
world.process_data(word_data, tile_list)

# Función para dibujar la cuadrícula
def dibujar_grilla():
    for x in range(0, constantes.ANCHO_VENTANA,constantes.CUADRICULA_TAMAÑO):
        pygame.draw.line(ventana, constantes.BLANCO, (x, 0), (x, constantes.ALTO_VENTANA))
    for y in range(0, constantes.ALTO_VENTANA, constantes.CUADRICULA_TAMAÑO):
        pygame.draw.line(ventana, constantes.BLANCO, (0, y), (constantes.ANCHO_VENTANA, y))
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
    world.draw(ventana)  #dibujar mundo
    personaje.dibujar(ventana)  # Dibujar el personaje en la pantalla
    grupo_item.update(personaje) # Actualizar el grupo de items
    grupo_item.draw(ventana)
    dibujar_grilla()# Dibujar la cuadrícula
    
     # Mostrar el puntaje en pantalla
    dibujar_texto(f"Score: {personaje.score}", fuente, 650, 5, (255, 255, 0))
    
   
    
    pygame.display.flip()  # Actualiza la pantalla

pygame.quit()
