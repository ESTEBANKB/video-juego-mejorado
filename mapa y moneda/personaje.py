# personaje 
import pygame
import constantes
import os

class Personaje:
    def __init__(self, x, y, imagen):
  
        """Inicializa el personaje con su imagen y posición."""
        self.imagenes = [pygame.image.load(os.path.join("recursos", "imagenes", "caracteres", "jugador", img)) for img in imagen] # Carga la imagen con ruta segura
        self.imagenes = [pygame.transform.scale(img, (constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)) for img in self.imagenes]  # Ajusta el tamaño
        self.indice_imagen = 0  # Índice de animación
        self.rect = self.imagenes[0].get_rect(topleft=(x, y))
        self.flip = False  # Voltear imagen si se mueve a la izquierda
        self.update_time = pygame.time.get_ticks()  # Tiempo para controlar la animación
        self.score= 0

            
            
    def mover(self, teclas):
        """Mueve al personaje y cambia la animación."""
        moviendo = False

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:  # Mover a la izquierda
            self.rect.x -= constantes.VELOCIDAD_PERSONAJE
            self.flip = True
            moviendo = True
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:  # Mover a la derecha
            self.rect.x += constantes.VELOCIDAD_PERSONAJE
            self.flip = False
            moviendo = True
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:  # Mover arriba
            self.rect.y -= constantes.VELOCIDAD_PERSONAJE
            moviendo = True
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:  # Mover abajo
            self.rect.y += constantes.VELOCIDAD_PERSONAJE
            moviendo = True
        
        if moviendo:
         self.update()  # Si el personaje se mueve, actualizar animación
        else:
         self.indice_imagen = 0  # Mantener la primera imagen si está quieto 
            
        
    def update(self):
        """Actualiza la animación del personaje."""
        cooldown_imagen= 100 # Tiempo en milisegundos para cambiar de imagen
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.update_time >= cooldown_imagen:
         self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
         self.update_time = tiempo_actual  # Resetear el tiempo de animación
            
            
            
    def dibujar(self, ventana):
        """Dibuja al personaje en la pantalla con la imagen actual y su orientación."""
        imagen_actual = pygame.transform.flip(self.imagenes[self.indice_imagen], self.flip, False)
        ventana.blit (imagen_actual, self.rect)  # Dibuja la imagen en la posición del personaj