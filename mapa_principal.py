# mapa_principal
import pygame
import constantes
from refugio import Refugio

class Mundo:
    def __init__(self):
        self.map_tiles = []
        self.refugio = None
        self.mapa_actual = "principal"

    def process_data(self, data, tile_list):
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    image = tile_list[tile]
                    image_rect = image.get_rect()
                    image_x = x * constantes.CUADRICULA_TAMAÑO
                    image_y = y * constantes.CUADRICULA_TAMAÑO
                    image_rect.topleft = (image_x, image_y)
                    tile_data = [image, image_rect]
                    self.map_tiles.append(tile_data)

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])

    def cambiar_a_refugio(self, personaje):
        self.mapa_actual = "refugio"
        self.refugio = Refugio(personaje)

    def detectar_entrada_refugio(self, personaje):
        if personaje.rect.colliderect(pygame.Rect(312 * constantes.CUADRICULA_TAMAÑO, 313 * constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO)):
            self.cambiar_a_refugio(personaje)

    def actualizar(self, personaje):
        if self.mapa_actual == "refugio":
            self.refugio.actualizar()
        else:
            self.detectar_entrada_refugio(personaje)
