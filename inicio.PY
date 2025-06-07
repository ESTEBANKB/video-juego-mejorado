# inicio.py - Versión corregida con sistema de pausa, reinicio y NPCs integrados

import pygame  # Importamos la librería Pygame
import constantes  # Importamos las constantes del juego
from pantalla_inicio import mostrar_pantalla_inicio  # Importamos la función
from personaje import Personaje  # Importamos la clase del personaje
from items import Item  # Importamos la clase de los items
from mundo import Mundo  # Importamos la clase del mundo
from camara import Camara  # Importar la clase de la cámara
from movimiento import cargar_imagenes_personaje  # Importar la función para cargar imágenes del personaje
from generar_items import generar_monedas, activar_monedas  # Importamos la nueva función para generar monedas
from colisiones import Colisiones  # Importamos la función para detectar colisiones
from refugio import Refugio  # Importamos la clase Refugio
from mapa_principal import Mundo  # Importa la clase Mundo
from colisiones_refugio import ColisionesRefugio  # Importamos la función para detectar colisiones en el refugio
from puerta_refugio import PuertaRefugio  # Importación de la puerta del refugio
from gestor_npcs import GestorNPCs  # Importamos el gestor de NPCs
from sistema_misiones import SistemaMisiones  # Importamos el sistema de misiones
from sistema_pausa_reinicio import SistemaPausaReinicio  # NUEVO: Sistema de pausa

from enum import Enum
import os
import csv

# Tipos de escena
class TipoEscena(Enum):
    MAPA_PRINCIPAL = "mapa_principal"
    REFUGIO = "refugio"

# Gestor de escenas
class GestorEscenas:
    def __init__(self):
        self.escena_actual = None
        self.escenas = {}
        self.en_transicion = False
        
    def registrar_escena(self, tipo_escena, escena):
        self.escenas[tipo_escena] = escena
        
    def cambiar_escena(self, nuevo_tipo_escena, personaje=None):
        if self.en_transicion:
            return False
            
        self.en_transicion = True
        
        # Limpiar escena anterior
        if self.escena_actual:
            self.limpiar_escena_actual()
            
        # Activar nueva escena
        if nuevo_tipo_escena in self.escenas:
            self.escena_actual = nuevo_tipo_escena
            escena = self.escenas[nuevo_tipo_escena]
            
            if hasattr(escena, 'inicializar_escena'):
                escena.inicializar_escena(personaje)
                
            print(f"Cambiado a escena: {nuevo_tipo_escena.value}")
            self.en_transicion = False
            return True
        else:
            self.en_transicion = False
            return False
    
    def limpiar_escena_actual(self):
        if self.escena_actual and self.escena_actual in self.escenas:
            escena = self.escenas[self.escena_actual]
            
            # Limpiar colisiones
            if hasattr(escena, 'colisiones') and hasattr(escena.colisiones, 'solid_tiles'):
                escena.colisiones.solid_tiles.empty()
                
            # Limpiar NPCs si existen
            if hasattr(escena, 'npcs_activos'):
                escena.npcs_activos = False
                
            if hasattr(escena, 'limpiar_escena'):
                escena.limpiar_escena()
    
    def obtener_escena_actual(self):
        if self.escena_actual:
            return self.escenas.get(self.escena_actual)
        return None

# Clase para el mapa principal - VERSIÓN MEJORADA CON INTEGRACIÓN DE NPCs
class MapaPrincipal:
    def __init__(self, personaje, world, colisiones, camara, grupo_item, puerta_refugio, gestor_npcs):
        self.personaje = personaje
        self.world = world
        self.colisiones = colisiones
        self.camara = camara
        self.grupo_item = grupo_item
        self.puerta_refugio = puerta_refugio
        self.gestor_npcs = gestor_npcs  # Usar el gestor de NPCs
        self.npcs_activos = True
        self.activa = False
        
    def inicializar_escena(self, personaje=None):
        self.activa = True
        self.npcs_activos = True
        
        # Recargar colisiones del mapa principal si es necesario
        if hasattr(self, 'word_data'):
            self.colisiones.solid_tiles.empty()
            self.colisiones.cargar_colisiones(self.word_data)
            
        print("Mapa principal inicializado - Colisiones:", len(self.colisiones.solid_tiles))
        
    def limpiar_escena(self):
        self.activa = False
        self.npcs_activos = False
        if self.colisiones and hasattr(self.colisiones, 'solid_tiles'):
            self.colisiones.solid_tiles.empty()
            
    def actualizar(self, teclas):
        if not self.activa:
            return
            
        # Mover personaje con colisiones del mapa principal
        self.personaje.mover(teclas, self.colisiones)
        
        # Actualizar cámara
        self.camara.update(self.personaje)
        
        # Actualizar sistema de puerta
        self.puerta_refugio.actualizar_mensaje()
        
        # Actualizar NPCs usando el gestor
        if self.npcs_activos:
            self.gestor_npcs.actualizar(self.personaje, teclas, self.grupo_item)
                    
        # Actualizar items
        self.grupo_item.update(self.personaje)

    def _dibujar_indicadores_interaccion(self, ventana):
        """Dibuja indicadores de interacción cerca de NPCs"""
        fuente_pequena = pygame.font.Font(None, 24)
        
        # Verificar proximidad con NPCs y mostrar indicadores
        if self.gestor_npcs.npc_humano:
            distancia = abs(self.personaje.rect.centerx - self.gestor_npcs.npc_humano.rect.centerx) + \
                       abs(self.personaje.rect.centery - self.gestor_npcs.npc_humano.rect.centery)
            if distancia < 80:  # Si está cerca
                pos_texto = self.camara.aplicar(pygame.Rect(
                    self.gestor_npcs.npc_humano.rect.x - 20, 
                    self.gestor_npcs.npc_humano.rect.y - 30, 0, 0))
                superficie_texto = fuente_pequena.render("Presiona E para hablar", True, (255, 255, 255))
                
                # Fondo semi-transparente
                fondo = pygame.Surface((superficie_texto.get_width() + 10, superficie_texto.get_height() + 5))
                fondo.set_alpha(180)
                fondo.fill((0, 0, 0))
                
                ventana.blit(fondo, (pos_texto.x - 5, pos_texto.y - 2))
                ventana.blit(superficie_texto, pos_texto)
        
        # Similar para otros NPCs
        if self.gestor_npcs.npc_mision:
            distancia = abs(self.personaje.rect.centerx - self.gestor_npcs.npc_mision.rect.centerx) + \
                       abs(self.personaje.rect.centery - self.gestor_npcs.npc_mision.rect.centery)
            if distancia < 80:
                pos_texto = self.camara.aplicar(pygame.Rect(
                    self.gestor_npcs.npc_mision.rect.x - 20, 
                    self.gestor_npcs.npc_mision.rect.y - 30, 0, 0))
                superficie_texto = fuente_pequena.render("Presiona E para misiones", True, (255, 255, 255))
                
                fondo = pygame.Surface((superficie_texto.get_width() + 10, superficie_texto.get_height() + 5))
                fondo.set_alpha(180)
                fondo.fill((0, 0, 0))
                
                ventana.blit(fondo, (pos_texto.x - 5, pos_texto.y - 2))
                ventana.blit(superficie_texto, pos_texto)
        
        if self.gestor_npcs.npc_informacion:
            distancia = abs(self.personaje.rect.centerx - self.gestor_npcs.npc_informacion.rect.centerx) + \
                       abs(self.personaje.rect.centery - self.gestor_npcs.npc_informacion.rect.centery)
            if distancia < 80:
                pos_texto = self.camara.aplicar(pygame.Rect(
                    self.gestor_npcs.npc_informacion.rect.x - 20, 
                    self.gestor_npcs.npc_informacion.rect.y - 30, 0, 0))
                superficie_texto = fuente_pequena.render("Presiona E para información", True, (255, 255, 255))
                
                fondo = pygame.Surface((superficie_texto.get_width() + 10, superficie_texto.get_height() + 5))
                fondo.set_alpha(180)
                fondo.fill((0, 0, 0))
                
                ventana.blit(fondo, (pos_texto.x - 5, pos_texto.y - 2))
                ventana.blit(superficie_texto, pos_texto)
        
    def dibujar(self, ventana):
        if not self.activa:
            return
            
        # Dibujar el mundo ajustado a la cámara
        for tile in self.world.map_tiles:
            ventana.blit(tile[0], self.camara.aplicar(tile[1]))
            
        # Dibujar items
        for item in self.grupo_item:
            ventana.blit(item.image, self.camara.aplicar(item))
            
        # Dibujar NPCs usando el gestor
        if self.npcs_activos:
            self.gestor_npcs.dibujar(ventana, self.camara)
            
            # Dibujar indicadores de interacción
            self._dibujar_indicadores_interaccion(ventana)
        
        # Dibujar indicador de la puerta
        self.puerta_refugio.dibujar_indicador_puerta(ventana, self.camara)
        
        # Dibujar mensaje de la puerta
        self.puerta_refugio.dibujar_mensaje(ventana)

# Clase mejorada del refugio con cámara corregida
class RefugioMejorado:
    def __init__(self, personaje):
        self.personaje = personaje
        self.refugio_original = Refugio(personaje)
        self.colisiones = ColisionesRefugio()
        self.camara = None
        self.activa = False
        self.posicion_entrada = (300, 300)  # Posición donde aparece el personaje
        
        # Configurar cámara del refugio
        ancho_refugio = constantes.COLUMNAS_REFUGIO * constantes.CUADRICULA_TAMAÑO
        alto_refugio = constantes.FILAS_REFUGIO * constantes.CUADRICULA_TAMAÑO
        self.camara = Camara(ancho_refugio, alto_refugio)
        
    def inicializar_escena(self, personaje=None):
        self.activa = True
        
        if personaje:
            self.personaje = personaje
            
        # Limpiar colisiones anteriores
        self.colisiones.solid_tiles.empty()
        
        # Recargar colisiones del refugio
        self.colisiones.cargar_colisiones(self.refugio_original.mapa_refugio)
        
        # Posicionar personaje en la entrada
        self.personaje.rect.x = self.posicion_entrada[0]
        self.personaje.rect.y = self.posicion_entrada[1]
        
        print("Refugio inicializado - Colisiones:", len(self.colisiones.solid_tiles))
        
    def limpiar_escena(self):
        self.activa = False
        if self.colisiones and hasattr(self.colisiones, 'solid_tiles'):
            self.colisiones.solid_tiles.empty()
            
    def actualizar(self, teclas):
        if not self.activa:
            return
            
        # Mover personaje con colisiones del refugio
        self.personaje.mover(teclas, self.colisiones)
        
        # Actualizar cámara del refugio
        self.camara.update(self.personaje)
        
        # Actualizar lógica específica del refugio
        self.refugio_original.actualizar()
        
    def dibujar(self, ventana):
        if not self.activa:
            return
            
        # Dibujar el refugio con la cámara correcta
        self.dibujar_refugio_con_camara(ventana)
    
    def dibujar_refugio_con_camara(self, ventana):
        """Dibuja el mapa del refugio tile por tile aplicando la cámara."""
        # Obtener el desplazamiento de la cámara
        scroll = self.camara.camara_rect
        
        # Calcular qué tiles están visibles para optimizar el rendimiento
        start_x = max(0, scroll.x // constantes.CUADRICULA_TAMAÑO)
        end_x = min(constantes.COLUMNAS_REFUGIO, (scroll.x + constantes.ANCHO_VENTANA) // constantes.CUADRICULA_TAMAÑO + 1)
        start_y = max(0, scroll.y // constantes.CUADRICULA_TAMAÑO)
        end_y = min(constantes.FILAS_REFUGIO, (scroll.y + constantes.ALTO_VENTANA) // constantes.CUADRICULA_TAMAÑO + 1)
        
        # Dibujar solo los tiles visibles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if y < len(self.refugio_original.mapa_refugio) and x < len(self.refugio_original.mapa_refugio[y]):
                    tile = self.refugio_original.mapa_refugio[y][x]
                    
                    if 0 <= tile < len(self.refugio_original.tile_list_refugio):
                        imagen_tile = self.refugio_original.tile_list_refugio[tile]
                        if imagen_tile:
                            # Aplicar la cámara al dibujar el tile
                            pos_x = x * constantes.CUADRICULA_TAMAÑO - scroll.x
                            pos_y = y * constantes.CUADRICULA_TAMAÑO - scroll.y
                            ventana.blit(imagen_tile, (pos_x, pos_y))

# FUNCIÓN PARA REINICIAR EL JUEGO
def reiniciar_juego():
    """Reinicia todos los componentes del juego"""
    print("Reiniciando juego...")
    
    # Cargar recursos del juego
    diccionario_imagenes = cargar_imagenes_personaje()
    personaje = Personaje(550, 550, diccionario_imagenes)

    # Cargar tiles del mundo
    tile_list = []
    ruta_mundo = os.path.join("recursos", "imagenes", "caracteres", "tiles")
    if os.path.exists(ruta_mundo):
        for x in range(constantes.TILE_TYPES):  
            tile_image = pygame.image.load(os.path.join(ruta_mundo, f"tiles_{x+1}.png"))
            tile_image = pygame.transform.scale(tile_image, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
            tile_list.append(tile_image)

    # Cargar imágenes de monedas
    coin_images = []
    ruta_img = os.path.join("recursos", "imagenes", "caracteres", "monedas")
    if os.path.exists(ruta_img):
        for i in range(9):
            img = pygame.image.load(os.path.join(ruta_img, f"monedas_{i+1}.png"))
            img = pygame.transform.scale(img, (constantes.ANCHO_MONEDA, constantes.ALTO_MONEDA))
            img.set_colorkey(constantes.COLOR_TRANSPARENTE)
            coin_images.append(img)

    # Cargar nivel desde CSV
    word_data = []
    ruta_nivel = os.path.join("recursos", "imagenes", "caracteres", "niveles", "nivel_test.csv")

    for fila in range(constantes.FILAS):
        filas = [5] * constantes.COLUMNAS
        word_data.append(filas)

    with open(ruta_nivel, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for x, fila in enumerate(reader):
            for y, columna in enumerate(fila):
                word_data[x][y] = int(columna)

    # Crear mundo y colisiones
    world = Mundo()
    world.process_data(word_data, tile_list)

    colisiones = Colisiones()
    colisiones.cargar_colisiones(word_data)

    # Crear cámara
    ancho_mapa = constantes.COLUMNAS * constantes.CUADRICULA_TAMAÑO
    alto_mapa = len(world.map_tiles) * constantes.CUADRICULA_TAMAÑO
    camara = Camara(ancho_mapa, alto_mapa)

    # CREAR SISTEMA DE MISIONES PRIMERO
    sistema_misiones = SistemaMisiones()

    # Generar items CON el sistema de misiones
    grupo_item = generar_monedas(10, coin_images, sistema_misiones)

    # Crear sistema de puerta del refugio
    puerta_refugio = PuertaRefugio(world, [312, 313])

    # CREAR GESTOR DE NPCS CON EL SISTEMA DE MISIONES
    gestor_npcs = GestorNPCs(sistema_misiones)

    # Crear escenas
    mapa_principal = MapaPrincipal(personaje, world, colisiones, camara, grupo_item, puerta_refugio, gestor_npcs)
    mapa_principal.word_data = word_data  # Para poder recargar colisiones

    refugio = RefugioMejorado(personaje)

    # Crear gestor de escenas
    gestor_escenas = GestorEscenas()
    gestor_escenas.registrar_escena(TipoEscena.MAPA_PRINCIPAL, mapa_principal)
    gestor_escenas.registrar_escena(TipoEscena.REFUGIO, refugio)

    # Empezar en el mapa principal
    gestor_escenas.cambiar_escena(TipoEscena.MAPA_PRINCIPAL, personaje)
    
    return personaje, gestor_escenas, gestor_npcs

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("S.E.A - Saving species on an adventure")
clock = pygame.time.Clock()
fuente = pygame.font.Font(None, 36)

# Mostrar pantalla de inicio
if not mostrar_pantalla_inicio(ventana, fuente):
    pygame.quit()
    exit()

def dibujar_texto(texto, fuente, x, y, color):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))

# INICIALIZAR COMPONENTES DEL JUEGO
personaje, gestor_escenas, gestor_npcs = reiniciar_juego()

# CREAR SISTEMA DE PAUSA
sistema_pausa = SistemaPausaReinicio(ventana, fuente)

# Variables de control
jugando = True

# BUCLE PRINCIPAL DEL JUEGO - VERSIÓN MEJORADA CON INTEGRACIÓN DE NPCs
while jugando:  
    clock.tick(constantes.FPS)

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        else:
            # NUEVO: Manejar eventos del sistema de pausa
            sistema_pausa.manejar_eventos(evento)
            
            # Manejar eventos específicos de NPCs solo si no está pausado
            if not sistema_pausa.esta_pausado():
                gestor_npcs.manejar_evento_tecla(evento)
                
                # NUEVA LÓGICA: Verificar interacciones con NPCs cuando se presiona E
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                    escena_actual_obj = gestor_escenas.obtener_escena_actual()
                    if gestor_escenas.escena_actual == TipoEscena.MAPA_PRINCIPAL:
                        # Verificar colisión con NPC humano
                        if (gestor_npcs.npc_humano and 
                            personaje.rect.colliderect(gestor_npcs.npc_humano.rect)):
                            if not gestor_npcs.npc_humano.dialogo_activo:
                                gestor_npcs.npc_humano.mostrar_dialogo()
                        
                        # Verificar colisión con NPC de misión
                        elif (gestor_npcs.npc_mision and 
                              personaje.rect.colliderect(gestor_npcs.npc_mision.rect)):
                            if hasattr(gestor_npcs.npc_mision, 'mostrar_dialogo'):
                                gestor_npcs.npc_mision.mostrar_dialogo()
                        
                        # Verificar colisión con NPC de información
                        elif (gestor_npcs.npc_informacion and 
                              personaje.rect.colliderect(gestor_npcs.npc_informacion.rect)):
                            if not gestor_npcs.npc_informacion.dialogo_activo:
                                gestor_npcs.npc_informacion.mostrar_dialogo()
                
                # NUEVA LÓGICA: Avanzar diálogos con P
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                    # Avanzar diálogo del NPC humano
                    if (gestor_npcs.npc_humano and 
                        gestor_npcs.npc_humano.dialogo_activo):
                        gestor_npcs.npc_humano.avanzar_dialogo()
                    
                    # Avanzar diálogo del NPC de información
                    elif (gestor_npcs.npc_informacion and 
                          gestor_npcs.npc_informacion.dialogo_activo):
                        gestor_npcs.npc_informacion.avanzar_dialogo()
                    
                    # Avanzar diálogo del NPC de misión
                    elif (gestor_npcs.npc_mision and 
                          hasattr(gestor_npcs.npc_mision, 'dialogo_activo') and
                          gestor_npcs.npc_mision.dialogo_activo):
                        gestor_npcs.npc_mision.avanzar_dialogo()
                
                # NUEVA LÓGICA: Manejar teclas numéricas para el NPC de información
                if evento.type == pygame.KEYDOWN:
                    escena_actual_obj = gestor_escenas.obtener_escena_actual()
                    if (gestor_escenas.escena_actual == TipoEscena.MAPA_PRINCIPAL and 
                        gestor_npcs.npc_informacion and
                        gestor_npcs.npc_informacion.dialogo_activo):
                        
                        # Detectar teclas numéricas 1-8 para el menú del NPC
                        if pygame.K_1 <= evento.key <= pygame.K_8:
                            numero = evento.key - pygame.K_0  # Convierte K_1 a 1, K_2 a 2, etc.
                            gestor_npcs.npc_informacion.seleccionar_tema(numero)
    
    # VERIFICAR SOLICITUDES DEL SISTEMA DE PAUSA
    if sistema_pausa.obtener_salida_solicitada():
        jugando = False
        continue
    
    if sistema_pausa.obtener_reinicio_solicitado():
        # Reiniciar el juego
        personaje, gestor_escenas, gestor_npcs = reiniciar_juego()
        sistema_pausa.reiniciar_estado()
        continue
    
    # Solo actualizar el juego si no está pausado
    if not sistema_pausa.esta_pausado():
        # Captura de teclas
        teclas = pygame.key.get_pressed()
        
        # Verificar cambio de escena
        escena_actual_obj = gestor_escenas.obtener_escena_actual()
        
        # NUEVA LÓGICA: Cambio al refugio con verificación de monedas
        if gestor_escenas.escena_actual == TipoEscena.MAPA_PRINCIPAL:
            # Verificar si puede entrar al refugio
            if escena_actual_obj.puerta_refugio.verificar_entrada(personaje):
                # Si presiona A y tiene suficientes monedas, entrar
                if teclas[pygame.K_a]:
                    gestor_escenas.cambiar_escena(TipoEscena.REFUGIO, personaje)
        
        # Lógica de salida del refugio (presionar ESC)
        if gestor_escenas.escena_actual == TipoEscena.REFUGIO and teclas[pygame.K_ESCAPE]:
            gestor_escenas.cambiar_escena(TipoEscena.MAPA_PRINCIPAL, personaje)
        
        # Actualizar escena actual
        if gestor_escenas.escena_actual == TipoEscena.MAPA_PRINCIPAL:
            mapa_principal = gestor_escenas.obtener_escena_actual()
            mapa_principal.actualizar(teclas)
        elif gestor_escenas.escena_actual == TipoEscena.REFUGIO:
            refugio = gestor_escenas.obtener_escena_actual()
            refugio.actualizar(teclas)
    
    # Actualizar sistema de pausa (siempre se actualiza)
    teclas = pygame.key.get_pressed()
    sistema_pausa.actualizar(teclas)
    
    # Dibujar
    ventana.fill(constantes.VERDE)
    
    # Dibujar escena actual
    escena_actual_obj = gestor_escenas.obtener_escena_actual()
    if escena_actual_obj:
        escena_actual_obj.dibujar(ventana)
    
    # Dibujar personaje (siempre visible)
    if escena_actual_obj and hasattr(escena_actual_obj, 'camara'):
        ventana.blit(personaje.imagenes[personaje.direccion_actual][personaje.indice_imagen], 
                    escena_actual_obj.camara.aplicar(personaje))
    
    # Mostrar puntaje
    dibujar_texto(f"Monedas: {personaje.score}", fuente, 650, 5, (255, 255, 0))
    
    # Mostrar instrucciones según la escena (solo si no está pausado)
    if not sistema_pausa.esta_pausado():
        if gestor_escenas.escena_actual == TipoEscena.REFUGIO:
            dibujar_texto("Presiona ESC para salir del refugio", fuente, 10, 50, (255, 255, 255))
        
        # Mostrar indicador de pausa
        sistema_pausa.dibujar_indicador_pausa()
    
    # IMPORTANTE: Dibujar el overlay de pausa AL FINAL (sobre todo lo demás)
    sistema_pausa.dibujar_overlay_pausa()
    
    pygame.display.flip()

pygame.quit()