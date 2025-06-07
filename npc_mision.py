#NPC_mision
import pygame
import os

class NPCMision(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, sistema_misiones=None):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sistema_misiones = sistema_misiones
        
        self.dialogo_activo = False
        self.dialogo_ya_mostrado = False
        self.dialogo_actual = 0
        self.linea_actual = 0
        self.mision_completada = False

        # Definir los diálogos del NPC de misión
        self.dialogos = [
            [
                "Hola, mi nombre es Rodrigo.\n"
                "Mi compañero Rastafari te envió conmigo, ¿verdad?"
            ],
            [
                "¿Sabías que hay más tipos de maltrato animal?\n"
                "No solo abuso físico, también psicológico,\n"
                "abandono, negligencia y explotación."
            ],
            [
                "Tu primera misión será recolectar las 10 monedas\n"
                "que están por todo el mapa para comprar el refugio.\n"
                "¿Estás preparado?"
            ]
        ]

        self.fuente_dialogo = pygame.font.Font(None, 28)
        self.fuente_pie = pygame.font.Font(None, 22)
        self.dialogo_rect = pygame.Rect(50, 400, 700, 180)

    def mostrar_dialogo(self):
        if not self.dialogo_activo:
            self.dialogo_activo = True
            self.dialogo_actual = 0
            self.linea_actual = 0

    def ocultar_dialogo(self):
        self.dialogo_activo = False

    def avanzar_dialogo(self, grupo_monedas=None):
        if not self.dialogo_activo:
            return

        self.linea_actual += 1

        # Si termina el cuadro actual, pasa al siguiente cuadro
        if self.linea_actual >= len(self.dialogos[self.dialogo_actual]):
            self.dialogo_actual += 1
            self.linea_actual = 0

            # Si ya no hay más cuadros, termina diálogo y activa misión
            if self.dialogo_actual >= len(self.dialogos):
                self.ocultar_dialogo()
                self.mision_completada = True
                
                # Completar misión en el sistema
                if self.sistema_misiones:
                    self.sistema_misiones.completar_mision("primera_mision")
                    print("¡Primera misión completada! Las monedas aparecerán ahora.")
                
                # Activar monedas
                if grupo_monedas:
                    for moneda in grupo_monedas:
                        if hasattr(moneda, 'activo'):
                            moneda.activo = True

    def dibujar(self, ventana, camara):
        ventana.blit(self.image, camara.aplicar(self.rect))

    def dibujar_dialogo(self, ventana):
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

        # Renderizar texto multilínea (separado por '\n')
        lineas = texto.split('\n')
        for i, linea in enumerate(lineas):
            img_texto = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            ventana.blit(img_texto, (self.dialogo_rect.x + 20, self.dialogo_rect.y + 20 + i * 30))

        # Mostrar texto "Pulsa P para continuar..." abajo del cuadro, sólo si NO es el último cuadro
        if self.dialogo_actual < len(self.dialogos) - 1:
            texto_pie = "Pulsa P para continuar..."
            img_pie = self.fuente_pie.render(texto_pie, True, (255, 255, 255))
            # Ponerlo en la parte inferior dentro del cuadro, centrado a la izquierda con algo de margen
            ventana.blit(img_pie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + self.dialogo_rect.height - 35))


def cargar_imagen_con_check(ruta):
    """Carga una imagen y verifica que exista; si no, muestra un error rojo"""
    if not os.path.exists(ruta):
        print(f"Error: no se encontró la imagen en la ruta {ruta}")
        superficie_error = pygame.Surface((60, 60))
        superficie_error.fill((255, 0, 0))  # Relleno rojo como aviso de error
        return superficie_error
    return pygame.image.load(ruta).convert_alpha()


def crear_npc_mision(sistema_misiones=None):
    """Crea y retorna una instancia del NPC de misión"""
    ruta_imagen = "recursos/imagenes/caracteres/humano/humano_mision.png"
    imagen_original = cargar_imagen_con_check(ruta_imagen)
    imagen = pygame.transform.scale(imagen_original, (60, 60))
    
    return NPCMision(1000, 1700, imagen, sistema_misiones)