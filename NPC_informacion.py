# NPC_informacion.py - Versión con menú numerado
import pygame
import os
import textwrap

class NPCInformacion(pygame.sprite.Sprite):
    def __init__(self, x, y, sistema_misiones=None):
        super().__init__()

        self.ruta_imagen = "recursos/imagenes/caracteres/humano/npc_general.png"
        self.image = self._cargar_imagen_con_check(self.ruta_imagen)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.sistema_misiones = sistema_misiones

        # Variables para controlar el diálogo
        self.dialogo_activo = False
        self.dialogo_ya_mostrado = False
        self.texto_dialogo_actual = ""
        self.mostrar_menu = True  # Controla si mostrar el menú o información específica
        self.tema_seleccionado = None

        self.fuente_dialogo = pygame.font.Font(None, 16)  # Fuente más pequeña para el menú
        self.fuente_pie = pygame.font.Font(None, 18)
        self.dialogo_rect = pygame.Rect(50, 350, 700, 230)  # Cuadro más grande

        # Información sobre maltrato animal
        self.datos_maltrato = [
            {
                "titulo": "Abuso Físico",
                "info": "El abuso físico incluye golpes, patadas, quemaduras, o cualquier acto que cause dolor o sufrimiento innecesario a un animal. Es una de las formas más evidentes de maltrato.",
                "como_tratarlo": "Denuncia inmediatamente a las autoridades competentes (policía, fiscalía, inspecciones de policía). Documenta con fotos o videos si es seguro hacerlo. Busca atención veterinaria urgente para el animal."
            },
            {
                "titulo": "Negligencia",
                "info": "La negligencia ocurre cuando no se proveen las necesidades básicas: agua, alimento adecuado, refugio contra el clima, atención veterinaria o un ambiente limpio y seguro.",
                "como_tratarlo": "Habla con el dueño si es posible y seguro, ofreciendo ayuda o recursos. Si la situación no mejora, denuncia a las autoridades de protección animal. A veces, la educación es clave."
            },
            {
                "titulo": "Abandono",
                "info": "Abandonar a un animal es dejarlo desamparado, incapaz de cuidarse por sí mismo. Muchos animales abandonados sufren hambre, enfermedades o accidentes.",
                "como_tratarlo": "Nunca abandones a un animal. Si no puedes cuidarlo, busca un hogar responsable o contacta refugios y organizaciones de rescate. Si encuentras un animal abandonado, llévalo a un lugar seguro y contacta a protección animal."
            },
            {
                "titulo": "Explotación Animal",
                "info": "Incluye el uso de animales en peleas (perros, gallos), circos que no cumplen con bienestar, cría intensiva sin condiciones adecuadas, o trabajos forzados excesivos (como en algunos caballos carretilleros).",
                "como_tratarlo": "No apoyes eventos o negocios que exploten animales. Denuncia actividades ilegales como las peleas. Promueve el turismo responsable y apoya santuarios éticos."
            },
            {
                "titulo": "Maltrato Psicológico",
                "info": "Consiste en causar miedo, estrés crónico, ansiedad o depresión a un animal mediante intimidación, aislamiento prolongado, confinamiento excesivo o gritos constantes.",
                "como_tratarlo": "Proporciona un ambiente seguro, estimulante y positivo. Evita castigos severos. La socialización adecuada y el enriquecimiento ambiental son fundamentales. En casos graves, consulta a un etólogo o veterinario especializado en comportamiento."
            },
            {
                "titulo": "Envenenamiento",
                "info": "Administrar sustancias tóxicas a un animal con la intención de dañarlo o matarlo es un acto criminal y cruel.",
                "como_tratarlo": "Mantén productos tóxicos fuera del alcance de los animales. Si sospechas envenenamiento, lleva al animal al veterinario DE INMEDIATO. Denuncia cualquier intento de envenenamiento a las autoridades."
            },
            {
                "titulo": "Cómo Ayudar (General)",
                "info": "Educa a otros sobre tenencia responsable. Apoya a refugios y organizaciones de rescate con donaciones o voluntariado. Considera la adopción antes que la compra. Esteriliza a tus mascotas para evitar la sobrepoblación.",
                "como_tratarlo": "Sé un defensor activo del bienestar animal en tu comunidad. Participa en campañas de concienciación y exige leyes más estrictas contra el maltrato."
            }
        ]

    def _cargar_imagen_con_check(self, ruta):
        if not os.path.exists(ruta):
            print(f"Error: No se encontró la imagen en la ruta {ruta}")
            superficie_error = pygame.Surface((60, 60))
            superficie_error.fill((255, 0, 0))
            return superficie_error
        
        imagen_original = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(imagen_original, (60, 70))

    def _generar_menu_principal(self):
        """Genera el texto del menú principal con opciones numeradas."""
        menu_texto = "INFORMACIÓN SOBRE MALTRATO ANIMAL\n"
        menu_texto += "="*40 + "\n\n"
        menu_texto += "Selecciona un tema para obtener más información:\n\n"
        
        for i, dato in enumerate(self.datos_maltrato, 1):
            menu_texto += f"{i}. {dato['titulo']}\n"
        
        menu_texto += f"\n8. Volver al menú principal"
        
        return menu_texto

    def _generar_info_especifica(self, indice):
        """Genera la información específica de un tema."""
        if 0 <= indice < len(self.datos_maltrato):
            dato = self.datos_maltrato[indice]
            texto = f"TEMA: {dato['titulo']}\n"
            texto += "="*40 + "\n\n"
            texto += f"Información:\n{dato['info']}\n\n"
            texto += f"Cómo tratarlo/prevenirlo:\n{dato['como_tratarlo']}\n\n"
            texto += "Presiona P para SALIR"
            return texto
        return "Error: Tema no encontrado"

    def seleccionar_tema(self, numero):
        """Selecciona un tema específico basado en el número."""
        if 1 <= numero <= len(self.datos_maltrato):
            self.mostrar_menu = False
            self.tema_seleccionado = numero - 1
            self.texto_dialogo_actual = self._generar_info_especifica(self.tema_seleccionado)
        elif numero == 8:  # Volver al menú
            self.mostrar_menu = True
            self.tema_seleccionado = None
            self.texto_dialogo_actual = self._generar_menu_principal()

    def actualizar(self, personaje, teclas=None, evento=None):
        """Actualiza el estado del NPC basado en la proximidad del personaje"""
        distancia = pygame.math.Vector2(
            personaje.rect.centerx - self.rect.centerx,
            personaje.rect.centery - self.rect.centery
        ).length()
        
        # Si el personaje está lejos, resetear el flag de diálogo mostrado
        if distancia > 100:
            self.dialogo_ya_mostrado = False
            self.mostrar_menu = True
            self.tema_seleccionado = None

        # Manejar selección de temas con teclas numéricas
        if self.dialogo_activo and teclas:
            if self.mostrar_menu:
                # En el menú principal, detectar teclas numéricas
                for i in range(1, 9):  # Teclas 1-8
                    key_attr = getattr(pygame, f'K_{i}')
                    if teclas[key_attr]:
                        self.seleccionar_tema(i)
                        break

    def mostrar_dialogo(self):
        """Muestra el diálogo del NPC"""
        if not self.dialogo_activo and not self.dialogo_ya_mostrado:
            self.mostrar_menu = True
            self.tema_seleccionado = None
            self.texto_dialogo_actual = self._generar_menu_principal()
            self.dialogo_activo = True
            self.dialogo_ya_mostrado = True

    def mostrar_dialogo_aleatorio(self):
        """Alias para mostrar_dialogo para compatibilidad"""
        self.mostrar_dialogo()

    def ocultar_dialogo(self):
        """Oculta el diálogo del NPC"""
        self.dialogo_activo = False

    def avanzar_dialogo(self):
        """Maneja el avance del diálogo cuando se presiona P"""
        if self.dialogo_activo:
            if not self.mostrar_menu and self.tema_seleccionado is not None:
                # Si estamos viendo información específica, volver al menú
                self.mostrar_menu = True
                self.tema_seleccionado = None
                self.texto_dialogo_actual = self._generar_menu_principal()
            else:
                # Si estamos en el menú, cerrar el diálogo
                self.ocultar_dialogo()

    def dibujar(self, ventana, camara):
        """Dibuja el NPC en la ventana ajustado a la cámara."""
        ventana.blit(self.image, camara.aplicar(self.rect))

    def dibujar_dialogo(self, ventana):
        """Dibuja el cuadro de diálogo y el texto si está activo."""
        if not self.dialogo_activo:
            return

        # Fondo del cuadro de diálogo
        s = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        s.set_alpha(230)
        s.fill((0, 0, 0))
        ventana.blit(s, (self.dialogo_rect.x, self.dialogo_rect.y))

        # Borde del cuadro
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)

        # Ajustar texto a múltiples líneas
        lineas_envueltas = []
        parrafos = self.texto_dialogo_actual.split('\n') 
        for parrafo in parrafos:
            if parrafo.strip():
                lineas_envueltas.extend(textwrap.wrap(parrafo, width=80))
            else:
                lineas_envueltas.append("")

        y_offset = self.dialogo_rect.y + 15
        for linea in lineas_envueltas:
            if y_offset + self.fuente_dialogo.get_height() > self.dialogo_rect.bottom - 45:
                lineas_envueltas.append("...")
                break 
            img_texto = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            ventana.blit(img_texto, (self.dialogo_rect.x + 15, y_offset))
            y_offset += self.fuente_dialogo.get_height() + 2

        # Instrucciones en el pie
        if self.mostrar_menu:
            texto_pie = "Usa las teclas 1-8 para seleccionar | P para cerrar"
        else:
            texto_pie = "Presiona P para SALIR"
            
        img_pie = self.fuente_pie.render(texto_pie, True, (200, 200, 200))
        ventana.blit(img_pie, 
                     (self.dialogo_rect.centerx - img_pie.get_width()//2, 
                      self.dialogo_rect.bottom - img_pie.get_height() - 8))

def crear_npc_informacion(x, y, sistema_misiones=None):
    """Función helper para crear una instancia del NPC de información."""
    return NPCInformacion(x, y, sistema_misiones)