#humano
import pygame

class NPCHumano(pygame.sprite.Sprite):  # Clase para crear un NPC tipo humano que interactúa con el jugador
    def __init__(self, x, y, imagen_surface, texto_bienvenida):
        super().__init__()
        self.image = imagen_surface  # Imagen que representa visualmente al NPC
        self.rect = self.image.get_rect()  # Obtiene el rectángulo que delimita la imagen
        self.rect.topleft = (x, y)  # Posición inicial del NPC en el mapa

        self.texto_bienvenida = texto_bienvenida  # Texto inicial que se muestra al hablar con el NPC
        self.dialogo_activo = False  # Indica si el diálogo está activo o no
        self.dialogo_ya_mostrado = False  # Controla si ya se mostró el diálogo (opcional, no usado aún)

        self.respuestas = ["¿Dónde está el gato?", "¿Qué tengo que hacer?", "Adiós"]  # Opciones que puede seleccionar el jugador
        self.respuesta_seleccionada = 0  # Índice de la opción actualmente seleccionada
        self.respuesta_actual = ""  # Texto que muestra la respuesta del NPC a la opción elegida
        self.mostrar_respuesta = False  # Controla si se debe mostrar la respuesta actual

        self.lineas_dialogo = [texto_bienvenida]  # Lista con el texto que se mostrará en el cuadro de diálogo
        self.fuente = pygame.font.Font(None, 24)  # Fuente que se usará para dibujar el texto
        self.color_fondo = (0, 0, 0)  # Color de fondo del cuadro de diálogo (negro)
        self.color_borde = (255, 255, 255)  # Color del borde del cuadro de diálogo (blanco)

    def mostrar_dialogo(self):
        self.dialogo_activo = True  # Activa el diálogo
        self.mostrar_respuesta = False  # Resetea el estado de la respuesta
        self.respuesta_actual = ""  # Borra la respuesta anterior

    def ocultar_dialogo(self):
        self.dialogo_activo = False  # Desactiva el diálogo

    def cambiar_respuesta(self):
        if self.dialogo_activo:
            # Cambia a la siguiente opción de respuesta, en forma circular
            self.respuesta_seleccionada = (self.respuesta_seleccionada + 1) % len(self.respuestas)

    def actualizar_dialogo(self):
        if self.dialogo_activo:
            seleccion = self.respuestas[self.respuesta_seleccionada]  # Obtiene la respuesta seleccionada
            # Define la respuesta del NPC según la opción seleccionada
            if seleccion == "¿Dónde está el gato?":
                self.respuesta_actual = "Está al este del mapa, ¡búscalo!"
            elif seleccion == "¿Qué tengo que hacer?":
                self.respuesta_actual = "Ayuda al gato a encontrar a sus amigos."
            elif seleccion == "Adiós":
                self.respuesta_actual = "¡Buena suerte!"
            self.mostrar_respuesta = True  # Habilita mostrar la respuesta

    def dibujar(self, ventana, camara):
        # Dibuja la imagen del NPC en pantalla ajustada a la cámara
        ventana.blit(self.image, camara.aplicar(self))

    def dibujar_dialogo(self, ventana):
        if not self.dialogo_activo:
            return  # No dibuja nada si el diálogo no está activo

        # Define el área del cuadro de diálogo
        ancho = 600
        alto = 140
        x = 100
        y = 400

        # Dibuja el fondo y el borde del cuadro de diálogo
        cuadro = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(ventana, self.color_fondo, cuadro)  # Fondo negro
        pygame.draw.rect(ventana, self.color_borde, cuadro, 3)  # Borde blanco

        # Prepara las líneas de texto para mostrar
        lineas = self.lineas_dialogo.copy()

        if self.mostrar_respuesta:
            lineas.append("")  # Línea en blanco antes de la respuesta
            lineas.append(self.respuesta_actual)  # Muestra la respuesta del NPC
        else:
            lineas.append("")  # Línea en blanco antes de las opciones
            for i, r in enumerate(self.respuestas):
                marcador = ">> " if i == self.respuesta_seleccionada else "   "  # Marca la opción seleccionada
                lineas.append(marcador + r)  # Agrega la opción con o sin el marcador

        lineas.append("E para seleccionar / P para enviar")  # Instrucción para el jugador

        # Dibuja cada línea de texto en pantalla
        for i, linea in enumerate(lineas):
            texto = self.fuente.render(linea, True, (255, 255, 255))  # Convierte texto a imagen
            ventana.blit(texto, (x + 10, y + 10 + i * 20))  # Muestra cada línea con espacio entre ellas
