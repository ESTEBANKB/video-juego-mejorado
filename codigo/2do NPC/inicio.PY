import pygame  # Importamos la librería Pygame
import constantes  # Importamos las constantes del juego
from pantalla_inicio import mostrar_pantalla_inicio  #, mostrar_historia  # Importamos la función
from personaje import Personaje  # Importamos la clase del personaje
from items import Item  # Importamos la clase de los items
from mundo import Mundo  # Importamos la clase del mundo
from camara import Camara  # Importar la clase de la cámara
from movimiento import cargar_imagenes_personaje  # Importar la función para cargar imágenes del personaje
from generar_items import generar_monedas  # Importamos la nueva función para generar monedas
from colisiones import Colisiones  # Importamos la función para detectar colisiones
from npc import GatoNPC
from npc_bienvenida import NPCHumano
from gato_humano import cargar_imagenes_gato, crear_npc_humano
from refugio import Refugio  # Importamos la clase Refugio
from mapa_principal import Mundo  # Importa la clase Mundo
from colisiones_refugio import ColisionesRefugio  # Importamos la función para detectar colisiones en el
from gato_humano import NPCMision
from npc_mision import NPCMision  # Importamos la clase del NPC de misión
from npc_mision import crear_npc_mision


import os
import csv


# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("S.E.A - Saving species on an adventure")

# Configuración del reloj para controlar los FPS
clock = pygame.time.Clock()

# Definir la fuente de texto
fuente = pygame.font.Font(None, 36)  # Fuente predeterminada de Pygame, tamaño 36

# Mostrar pantalla de inicio
if not mostrar_pantalla_inicio(ventana, fuente):
    pygame.quit()
    exit()

# Función para dibujar texto en pantalla
def dibujar_texto(texto, fuente, x, y, color):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))

# Cargar las imágenes del personaje
diccionario_imagenes = cargar_imagenes_personaje()

# Crear el personaje en una posición inicial
personaje = Personaje(550, 550, diccionario_imagenes)

# Crear el refugio
refugio = Refugio(personaje)

# Variable para saber si estamos en el refugio
en_refugio = False

# Cargar imágenes del mundo
tile_list = []
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
        img = pygame.transform.scale(img, (constantes.ANCHO_MONEDA, constantes.ALTO_MONEDA))
        img.set_colorkey(constantes.COLOR_TRANSPARENTE)  # Elimina el color de fondo si es necesario
        coin_images.append(img)

# Cargar el nivel desde un archivo CSV
word_data = []
ruta_nivel = os.path.join("recursos", "imagenes", "caracteres", "niveles", "nivel_test.csv")

for fila in range(constantes.FILAS):
    filas = [5] * constantes.COLUMNAS
    word_data.append(filas)

with open(ruta_nivel, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            word_data[x][y] = int(columna)  # Convertir a entero

# Crear el mundo con la información del nivel
world = Mundo()
world.process_data(word_data, tile_list)

# Cargar colisiones
colisiones = Colisiones()
colisiones.cargar_colisiones(word_data)

# Crear la cámara con el tamaño del mapa (suponiendo 20x15 tiles)
ancho_mapa = constantes.COLUMNAS * constantes.CUADRICULA_TAMAÑO
alto_mapa = len(world.map_tiles) * constantes.CUADRICULA_TAMAÑO
camara = Camara(ancho_mapa, alto_mapa)

# Generar monedas en todo el mapa
grupo_item = generar_monedas(10, coin_images)

# Crear NPC humano
npc_humano = crear_npc_humano()  # Llamas a la función y te da una instancia de NPCHumano

# Crear el segundo NPC de misión
npc_mision = crear_npc_mision()


# Grupo de NPCs (opcional para manejo conjunto)
grupo_npcs = pygame.sprite.Group()
grupo_npcs.add(npc_humano)
grupo_npcs.add(npc_mision)

# Cargar gato
imagenes_gato = cargar_imagenes_gato()  # Carga las imágenes del gato
gato = GatoNPC(2430, 600, imagenes_gato)
grupo_npcs.add(gato)

tecla_e_presionada = False
tecla_p_presionada = False


#
# Crear NPCs con funciones ya listas
npc_mision = crear_npc_mision()
npc_humano = crear_npc_humano()

# Grupo de monedas (debes tenerlo creado con monedas invisibles)
grupo_monedas = pygame.sprite.Group()
# Aquí agrega las monedas, recuerda poner moneda.visible = False inicialmente

# En el loop principal, detectar interacción con npc_mision
teclas = pygame.key.get_pressed()
if npc_mision.rect.colliderect(personaje.rect):
    if teclas[pygame.K_p]:
        npc_mision.avanzar_dialogo(grupo_monedas)
    npc_mision.mostrar_dialogo()
else:
    npc_mision.ocultar_dialogo()

npc_mision.dibujar(ventana, camara)


# Bucle principal del juego
jugando = True

def cargar_mapa_refugio():
    global world, en_refugio, camara
    en_refugio = True
    world = refugio
    ancho_refugio = len(refugio.mapa_refugio[0]) * constantes.CUADRICULA_TAMAÑO
    alto_refugio = len(refugio.mapa_refugio) * constantes.CUADRICULA_TAMAÑO
    camara = Camara(ancho_refugio, alto_refugio)

# Variables para evitar repetición de teclas
tecla_e_presionada = False
tecla_p_presionada = False

while jugando:
    clock.tick(constantes.FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                npc_humano.ocultar_dialogo()

    teclas = pygame.key.get_pressed()

    # PRIMER NPC: humano informativo con opciones
    tocando_npc = pygame.sprite.collide_rect(personaje, npc_humano)
    if tocando_npc and not npc_humano.dialogo_ya_mostrado:
        npc_humano.mostrar_dialogo()
        npc_humano.dialogo_ya_mostrado = True
    elif not tocando_npc:
        npc_humano.ocultar_dialogo()
        npc_humano.dialogo_ya_mostrado = False

    if npc_humano.dialogo_visible:
        if teclas[pygame.K_e] and not tecla_e_presionada:
            npc_humano.cambiar_respuesta()
            tecla_e_presionada = True
        elif not teclas[pygame.K_e]:
            tecla_e_presionada = False

        if teclas[pygame.K_p] and not tecla_p_presionada:
            npc_humano.avanzar_dialogo()
            tecla_p_presionada = True
        elif not teclas[pygame.K_p]:
            tecla_p_presionada = False

    # SEGUNDO NPC: misión y desbloqueo de monedas
    if personaje.rect.colliderect(npc_mision.rect):
        if teclas[pygame.K_p] and not tecla_p_presionada:
            npc_mision.avanzar_dialogo(grupo_item)
            tecla_p_presionada = True
        elif not teclas[pygame.K_p]:
            tecla_p_presionada = False
        npc_mision.mostrar_dialogo()
    else:
        npc_mision.ocultar_dialogo()

    # Movimiento del personaje
    if en_refugio:
        personaje.mover(teclas, refugio.colisiones_refugio)
    else:
        personaje.mover(teclas, colisiones)

    # Cámara sigue al personaje
    camara.update(personaje)

    # Gato sigue al personaje si colisiona
    if pygame.sprite.collide_rect(personaje, gato) and not gato.siguiendo:
        gato.siguiendo = True
    gato.actualizar(personaje)

    # Verifica entrada al refugio (tiles 312 o 313)
    if not en_refugio and (personaje.rect.colliderect(world.map_tiles[312][1]) or personaje.rect.colliderect(world.map_tiles[313][1])):
        cargar_mapa_refugio()

    # Dibujar mundo
    ventana.fill(constantes.VERDE)
    if en_refugio:
        refugio.actualizar()
        refugio.dibujar(ventana)
    else:
        for tile in world.map_tiles:
            ventana.blit(tile[0], camara.aplicar(tile[1]))

    # Dibujo del personaje
    ventana.blit(personaje.imagenes[personaje.direccion_actual][personaje.indice_imagen], camara.aplicar(personaje))

    # Dibujar monedas si están visibles
    grupo_item.update(personaje)
    grupo_item.draw(ventana)

    # Dibujar personajes y textos
    gato.dibujar(ventana, camara)
    npc_humano.dibujar(ventana, camara)
    npc_mision.dibujar(ventana, camara)

    # Mostrar puntaje
    dibujar_texto(f"Score: {personaje.score}", fuente, 650, 5, (255, 255, 0))

    npc_mision.dibujar_dialogo(ventana) 

    pygame.display.flip()

pygame.quit()


