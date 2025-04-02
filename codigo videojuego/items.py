#items
import constantes
import pygame.sprite



class Item(pygame.sprite.Sprite):
    def __init__(self, x, y,animacion_list):
        """Inicializa el objeto Item (moneda) con su animación."""
        pygame.sprite.Sprite.__init__(self)
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animacion_list[self.frame_index]
        
         # 📌 Fijar la posición inicial correctamente en el mundo
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        
         # Guardar la posición fija en el mundo
        self.posicion_inicial = (x, y)

    def update(self, personaje):
        """Actualiza la animación de la moneda y detecta colisión con el personaje."""
        
         # 📌 Asegurar que la moneda no se mueva con la cámara
        self.rect.topleft = self.posicion_inicial 
        
        
        # 📌 Verificar colisión con el personaje
        if self.rect.colliderect(personaje.rect):
            if hasattr(personaje, "score"):  # Asegurarse de que `score` existe en el personaje
                personaje.score += 1  # Sumar 1 punto
            else:
                print(" Advertencia: El personaje no tiene un atributo 'score'.")
            self.kill()  # Eliminar la moneda del juego
        
        """Animación de la moneda"""
        cooldown_imagen = 150  # Tiempo en milisegundos para cambiar de imagen
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.update_time >= cooldown_imagen:
            self.frame_index = (self.frame_index + 1) % len(self.animacion_list)
            self.image = self.animacion_list[self.frame_index]
            self.update_time = tiempo_actual
