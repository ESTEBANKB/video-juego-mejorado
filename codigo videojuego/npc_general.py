import pygame
import os

class NPCGeneral(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, dialogos):
        super().__init__()
        # Imagen y rectángulo para el NPC
        self.image = imagen
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Variables para controlar el diálogo
        self.dialogo_activo = False         # ¿Se muestra diálogo?
        self.dialogo_ya_mostrado = False    # Para mostrar diálogo solo una vez si quieres
        self.dialogo_actual = 0             # Índice de la pestaña de diálogo actual
        self.linea_actual = 0               # Línea de texto dentro de la pestaña
        self.respuesta_actual = 0           # Índice para seleccionar opciones, si las hay
        
        # Fuente para el texto del diálogo
        self.fuente_dialogo = pygame.font.Font(None, 28)
        self.fuente_pie = pygame.font.Font(None, 22)
        
        # Tamaño y posición del cuadro de diálogo  
        self.dialogo_rect = pygame.Rect(50, 400, 700, 150)
        
        # Asignar los diálogos
        self.dialogos = dialogos

    def mostrar_dialogo(self):
        """Activa el diálogo para mostrarlo"""
        self.dialogo_activo = True
        self.dialogo_actual = 0  # Empezar con la primera pestaña
        self.linea_actual = 0    # Primera línea

    def ocultar_dialogo(self):
        """Oculta el diálogo"""
        self.dialogo_activo = False

    def avanzar_dialogo(self):
        """
        Avanza una línea en el diálogo,
        o cambia a la siguiente pestaña si termina la actual,
        o cierra el diálogo si termina todo.
        """
        if not self.dialogo_activo:
            return

        self.linea_actual += 1

        # Si terminamos las líneas de la pestaña actual
        if self.linea_actual >= len(self.dialogos[self.dialogo_actual]):
            if self.dialogo_actual == 0:
                # Pasar a la segunda pestaña
                self.dialogo_actual = 1
                self.linea_actual = 0
            else:
                # Terminar diálogo
                self.ocultar_dialogo()

    def cambiar_respuesta(self):
        """
        Cambiar opción seleccionada (si tuvieses opciones para seleccionar).
        Aquí como ejemplo simplemente alterna la respuesta (no usado en este diálogo).
        """
        self.respuesta_actual = (self.respuesta_actual + 1) % 2  # Ejemplo simple

    def dibujar(self, ventana, camara):
        """Dibuja el NPC en la ventana ajustado a la cámara"""
        ventana.blit(self.image, camara.aplicar(self.rect))

    def dibujar_dialogo(self, ventana):
        """Dibuja el cuadro de diálogo y el texto si está activo"""
        if not self.dialogo_activo:
            return

        # Fondo del cuadro de diálogo (semi-transparente negro)
        s = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        ventana.blit(s, (self.dialogo_rect.x, self.dialogo_rect.y))

        # Dibujar borde blanco
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)

        # Obtener la línea actual para mostrar
        texto = self.dialogos[self.dialogo_actual][self.linea_actual]

        # Renderizar texto y dibujar centrado horizontal en el cuadro
        lineas = texto.split('\n')
        for i, linea in enumerate(lineas):
            img_texto = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            ventana.blit(img_texto, (self.dialogo_rect.x + 20, self.dialogo_rect.y + 20 + i * 30))

        # Mostrar texto "Pulsa P para continuar..." abajo del cuadro
        if self.dialogo_actual < len(self.dialogos) - 1:
            texto_pie = "Pulsa P para continuar..."
            img_pie = self.fuente_pie.render(texto_pie, True, (255, 255, 255))
            ventana.blit(img_pie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + self.dialogo_rect.height - 35))


def cargar_imagen_con_check(ruta):
    """Carga una imagen y verifica que exista; si no, muestra un error rojo"""
    if not os.path.exists(ruta):
        print(f"Error: no se encontró la imagen en la ruta {ruta}")
        superficie_error = pygame.Surface((50, 70))
        superficie_error.fill((0, 0, 255))  # Relleno azul como aviso de error
        return superficie_error
    return pygame.image.load(ruta).convert_alpha()


def crear_npc_general():
    """Crea y retorna una instancia del NPC general"""
    ruta_imagen = "recursos/imagenes/caracteres/humano/npc_general.png"
    imagen_original = cargar_imagen_con_check(ruta_imagen)
    imagen = pygame.transform.scale(imagen_original, (50, 70))
    
    # Dialogos de ejemplo para el NPC general
    dialogos = [
        [
            "¡Hola aventurero!\n"
            "Soy un NPC general que puede ayudarte\n"
            "con información básica sobre el juego."
        ],
        [
            "Recuerda explorar todo el mapa\n"
            "y hablar con todos los NPCs.\n"
            "¡Buena suerte en tu aventura!"
        ]
    ]
    
    return NPCGeneral(1200, 800, imagen, dialogos)