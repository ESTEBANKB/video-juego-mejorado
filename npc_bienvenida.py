# npc_bienvenida.py - Versión mejorada con lógica consistente
import pygame
import os
import textwrap

class NPCHumano(pygame.sprite.Sprite):
    def __init__(self, x, y, sistema_misiones=None):
        super().__init__()
        
        # Cargar imagen del NPC
        self.ruta_imagen = "recursos/imagenes/caracteres/humano/humanoo.png"
        self.image = self._cargar_imagen_con_check(self.ruta_imagen)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.sistema_misiones = sistema_misiones
        
        # Variables para controlar el diálogo
        self.dialogo_activo = False
        self.dialogo_ya_mostrado = False
        self.dialogo_actual = 0 # Índice del "tema" o "fase" del diálogo
        
        # Fuentes para el diálogo
        self.fuente_dialogo = pygame.font.Font(None, 28)
        self.fuente_pie = pygame.font.Font(None, 22)
        
        # Rectángulo del cuadro de diálogo
        self.dialogo_rect = pygame.Rect(50, 400, 700, 150)
        
        # Diálogos específicos del NPC humano (cada elemento es un "tema" o "fase")
        self.dialogos_por_tema = [ 
            """¡Bienvenido! Mi nombre es Rastafari; Me alegra que estés aquí para ayudar.
            Hemos estado esperando a alguien con tu coraje. El mundo animal te necesita.""",
            
            """Sé que tienes muchas preguntas, pero por ahora concéntrate en aprender 
            a moverte y recolectar las monedas que están por el mapa. 
            Te ayudarán a entender cómo funciona el juego.""",
            
            """Hay mucho que hacer aquí. Habla con los demás NPCs para aprender más 
            sobre las misiones y cómo puedes contribuir a salvar a las especies en peligro."""
        ]
        
        # NUEVO: Almacenar las páginas pre-calculadas para cada tema de diálogo
        # Esto será una lista de listas de líneas (tema -> página -> línea)
        self.paginas_por_tema = []
        for dialogo_completo in self.dialogos_por_tema:
            self.paginas_por_tema.append(self._obtener_paginas_dialogo(dialogo_completo))

        self.pagina_actual = 0 # Índice de la página actual dentro del diálogo activo
        
    def _cargar_imagen_con_check(self, ruta):
        """Carga una imagen y verifica que exista; si no, muestra un error rojo"""
        if not os.path.exists(ruta):
            print(f"Error: no se encontró la imagen en la ruta {ruta}")
            superficie_error = pygame.Surface((50, 70))
            superficie_error.fill((255, 0, 0))  # Relleno rojo como aviso de error
            return superficie_error
        return pygame.image.load(ruta).convert_alpha()  # Carga con transparencia

    def _obtener_paginas_dialogo(self, texto_completo):
        """
        Divide un texto completo en páginas que caben en el cuadro de diálogo.
        Cada página termina cuando no caben más líneas.
        """
        max_ancho_linea = 70  # Caracteres por línea (ajusta según tu fuente y tamaño de recuadro)
        altura_linea = self.fuente_dialogo.get_height() + 2 # Altura de cada línea de texto + un pequeño margen
        
        # Calcular el número máximo de líneas que caben en el cuadro de diálogo
        margen_vertical_dialogo = 40 # Margen superior e inferior dentro del diálogo (20 + 20)
        altura_disponible = self.dialogo_rect.height - margen_vertical_dialogo
        max_lineas_por_pagina = int(altura_disponible / altura_linea)
        
        paginas = []
        lineas_actuales_pagina = []
        
        # Primero, envolver todo el texto para tener las líneas que realmente se renderizarán
        todas_las_lineas_envueltas = []
        # Dividir por '\n' para manejar párrafos explícitos
        parrafos = texto_completo.replace('\\n', '\n').split('\n')
        
        for parrafo in parrafos:
            if parrafo.strip(): # Si no es una línea vacía
                todas_las_lineas_envueltas.extend(textwrap.wrap(parrafo, width=max_ancho_linea))
            else: # Mantener las líneas vacías para representar saltos de párrafo
                todas_las_lineas_envueltas.append("") # Añadir una línea vacía para el salto de párrafo

        for linea in todas_las_lineas_envueltas:
            # Si añadir la línea actual excede el límite de líneas por página,
            # cerramos la página actual y empezamos una nueva.
            if len(lineas_actuales_pagina) >= max_lineas_por_pagina:
                paginas.append(lineas_actuales_pagina)
                lineas_actuales_pagina = [linea] # Empezar una nueva página con la línea actual
            else:
                lineas_actuales_pagina.append(linea)
        
        # Añadir la última página si hay líneas restantes
        if lineas_actuales_pagina:
            paginas.append(lineas_actuales_pagina)
            
        return paginas

    def actualizar(self, personaje, grupo_monedas):
        """Actualiza el estado del NPC (p.ej., si el diálogo debe estar activo)."""
        # Lógica para activar el diálogo si el personaje está cerca y no se ha mostrado antes
        distancia_x = abs(personaje.rect.centerx - self.rect.centerx)
        distancia_y = abs(personaje.rect.centery - self.rect.centery)
        
        # Definir una distancia de interacción razonable
        distancia_interaccion = 80 # Ajusta según lo consideres necesario

        if distancia_x < distancia_interaccion and distancia_y < distancia_interaccion and not self.dialogo_ya_mostrado:
            self.dialogo_activo = True
        elif (distancia_x >= distancia_interaccion or distancia_y >= distancia_interaccion) and self.dialogo_activo:
            self.dialogo_activo = False
            # Reiniciar diálogo si el jugador se aleja (opcional, podrías querer mantener el estado)
            self.dialogo_actual = 0
            self.pagina_actual = 0

    def dibujar(self, ventana, camara=None):
        """Dibuja el cuadro de diálogo y el texto si está activo."""
        if not self.dialogo_activo:
            return

        # Fondo del cuadro de diálogo (semi-transparente negro)
        s = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        ventana.blit(s, (self.dialogo_rect.x, self.dialogo_rect.y))

        # Dibujar borde blanco
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)
        
        # NUEVO: Obtener las líneas de la página actual
        try:
            # self.dialogo_actual es el índice del "tema" o "fase" del diálogo (ej: "Bienvenida", "Misión 1")
            # self.pagina_actual es el índice de la página dentro de ese tema/fase
            lineas_a_mostrar = self.paginas_por_tema[self.dialogo_actual][self.pagina_actual]
        except IndexError:
            # Esto puede ocurrir si el diálogo está mal configurado o si se intenta
            # acceder a un índice de página que no existe.
            print(f"Error: Índice de diálogo/página fuera de rango para {self.__class__.__name__}. "
                  f"Dialogo actual: {self.dialogo_actual}, Página actual: {self.pagina_actual}")
            lineas_a_mostrar = ["Error en diálogo", "Presiona P para cerrar"]

        y_offset = self.dialogo_rect.y + 20
        for linea in lineas_a_mostrar:
            img_texto = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            ventana.blit(img_texto, (self.dialogo_rect.x + 20, y_offset))
            y_offset += self.fuente_dialogo.get_height() + 2

        # Mostrar instrucciones en el pie (modificado)
        hay_mas_paginas = self.pagina_actual < len(self.paginas_por_tema[self.dialogo_actual]) - 1
        hay_mas_dialogos = self.dialogo_actual < len(self.paginas_por_tema) - 1

        if hay_mas_paginas:
            texto_pie = "Presiona P para continuar..."
        elif hay_mas_dialogos:
            texto_pie = "Presiona P para continuar al siguiente tema..." # O "Presiona P para cerrar" si no quieres que avance a otro tema automáticamente
        else:
            texto_pie = "Presiona P para cerrar"
        
        img_pie = self.fuente_pie.render(texto_pie, True, (200, 200, 200))
        ventana.blit(img_pie, (self.dialogo_rect.x + 20, self.dialogo_rect.bottom - 35))

    def manejar_evento(self, evento, sistema_misiones=None):
        """Maneja eventos de teclado para el diálogo."""
        if self.dialogo_activo:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                
                # Comprobar si hay más páginas en el diálogo actual
                if self.pagina_actual < len(self.paginas_por_tema[self.dialogo_actual]) - 1:
                    self.pagina_actual += 1 # Avanzar a la siguiente página
                else:
                    # Si no hay más páginas, intentar avanzar al siguiente tema de diálogo
                    if self.dialogo_actual < len(self.paginas_por_tema) - 1:
                        self.dialogo_actual += 1 # Avanzar al siguiente tema
                        self.pagina_actual = 0  # Reiniciar a la primera página del nuevo tema
                    else:
                        # Si no hay más páginas ni más temas, cerrar el diálogo
                        self.dialogo_activo = False
                        self.dialogo_ya_mostrado = True # Para que no se repita si es de bienvenida/una vez
                        self.dialogo_actual = 0 # Reiniciar para la próxima vez
                        self.pagina_actual = 0 # Reiniciar página también
                        
                        # Lógica específica para misiones o eventos al finalizar el diálogo
                        if sistema_misiones and self.mision_activa: # Si tienes una misión asociada
                             # Aquí podrías activar una misión o marcarla como iniciada
                             pass # Esto dependerá de la lógica de tu sistema_misiones

# Función auxiliar para crear instancias de NPCHumano
def crear_npc_humano(x, y, sistema_misiones=None):
    return NPCHumano(x, y, sistema_misiones)