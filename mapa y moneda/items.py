#items
import constantes
import pygame.sprite
import personaje


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y,animacion_list):
        pygame.sprite.Sprite.__init__(self)
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animacion_list[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x,y))
          

    def update(self, personaje):
        #colicion entre el personaje y la moneda 
        if self.rect.colliderect(personaje.rect):
            #monedas
            personaje.score += 1  # Sumar 1 punto
            self.kill()  # Eliminar la moneda del grupo
        
                
            self.kill()
        
        """Animación de la moneda"""
        cooldown_imagen = 150  # Tiempo en milisegundos para cambiar de imagen
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.update_time >= cooldown_imagen:
            self.frame_index = (self.frame_index + 1) % len(self.animacion_list)
            self.image = self.animacion_list[self.frame_index]
            self.update_time = tiempo_actual
