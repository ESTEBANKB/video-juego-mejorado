# Importa el módulo os para gestionar rutas de archivos y verificar su existencia
import os

# Importa pygame para poder crear videojuegos y manejar gráficos, sonido, etc.
import pygame

# Importa textwrap para dividir textos largos en varias líneas (útil para diálogos)
import textwrap

from npc_mision import NPCMision  # Importa la clase del NPC de misión

# Clase que representa un NPC humano con diálogos
class NPCHumano(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, dialogos):
        super().__init__()  # Inicializa la clase Sprite de Pygame
        self.image = imagen  # Imagen del NPC
        self.rect = self.image.get_rect(topleft=(x, y))  # Rectángulo de posición y colisiones
        self.dialogos = dialogos  # Lista de textos que dirá el NPC
        self.dialogo_visible = False  # Bandera para saber si se debe mostrar el diálogo
        self.dialogo_actual = 0  # Índice del diálogo actual que se está mostrando

    # Activa la visibilidad del cuadro de diálogo
    def mostrar_dialogo(self):
        self.dialogo_visible = True

    # Desactiva el cuadro de diálogo
    def ocultar_dialogo(self):
        self.dialogo_visible = False

    # Pasa al siguiente diálogo o reinicia si ya mostró todos
    def avanzar_dialogo(self):
        if self.dialogo_actual < len(self.dialogos) - 1:
            self.dialogo_actual += 1  # Avanza al siguiente cuadro de texto
        else:
            self.ocultar_dialogo()  # Oculta el cuadro si era el último texto
            self.dialogo_actual = 0  # Reinicia el diálogo para futuras interacciones

    # Dibuja el NPC en pantalla, y el cuadro de diálogo si está activo
    def dibujar(self, superficie, camara):
        pos_pantalla = camara.aplicar(self.rect)  # Ajusta la posición según la cámara
        superficie.blit(self.image, pos_pantalla)  # Dibuja al NPC

        if self.dialogo_visible:
            self.dibujar_dialogo(superficie)  # Dibuja el cuadro de diálogo si está visible

    # Dibuja el cuadro de diálogo en la parte inferior de la pantalla
    def dibujar_dialogo(self, superficie):
        font = pygame.font.SysFont("arial", 22, bold=True)  # Fuente para texto principal
        aviso_font = pygame.font.SysFont("arial", 18)  # Fuente para "P para continuar..."

        padding = 20  # Espaciado interno del cuadro
        max_width = superficie.get_width() - 40  # Ancho máximo del cuadro
        max_text_width = max_width - 2 * padding  # Ancho útil para texto

        texto = self.dialogos[self.dialogo_actual]  # Texto actual del diálogo

        # Divide el texto en múltiples líneas que no excedan el ancho
        lineas = textwrap.wrap(texto, width=60)  # Puedes ajustar este valor

        # Renderiza cada línea de texto en superficies
        texto_surfs = [font.render(linea, True, (255, 255, 255)) for linea in lineas]
        aviso_surf = aviso_font.render("P para continuar...", True, (255, 255, 255))

        # Altura total del cuadro de diálogo
        alto_total = len(texto_surfs) * font.get_height() + aviso_surf.get_height() + padding * 3

        # Crea superficie del cuadro exterior (borde blanco)
        cuadro = pygame.Surface((max_width + 4, alto_total + 4))
        cuadro.fill((255, 255, 255))  # Borde blanco

        # Crea superficie del cuadro interior (fondo negro)
        inner = pygame.Surface((max_width, alto_total))
        inner.fill((0, 0, 0))  # Fondo negro

        # Dibuja cada línea de texto en el cuadro interior
        y_offset = padding
        for surf in texto_surfs:
            inner.blit(surf, (padding, y_offset))
            y_offset += font.get_height()

        # Dibuja el aviso "P para continuar..." en la esquina inferior derecha
        inner.blit(aviso_surf, (max_width - aviso_surf.get_width() - padding,
                                alto_total - aviso_surf.get_height() - padding))

        # Une el cuadro interior con el exterior
        cuadro.blit(inner, (2, 2))

        # Calcula posición final del cuadro en la parte inferior de la pantalla
        superficie_rect = superficie.get_rect()
        pos_cuadro = (20, superficie_rect.height - alto_total - 20)
        superficie.blit(cuadro, pos_cuadro)

# Carga una imagen y verifica que exista; si no, muestra un error rojo
def cargar_imagen_con_check(ruta):
    if not os.path.exists(ruta):
        print(f"Error: no se encontró la imagen en la ruta {ruta}")
        superficie_error = pygame.Surface((50, 70))
        superficie_error.fill((255, 0, 0))  # Relleno rojo como aviso de error
        return superficie_error
    return pygame.image.load(ruta).convert_alpha()  # Carga con transparencia

# Carga las animaciones del personaje gato (3 imágenes por dirección + quieto)
def cargar_imagenes_gato():
    carpeta_gato = "recursos/imagenes/caracteres/gato/"
    imagenes = {
        "abajo": [],
        "arriba": [],
        "derecha": [],
        "izquierda": [],
        "quieto": None
    }

    for i in range(1, 4):
        imagenes["abajo"].append(pygame.image.load(carpeta_gato + f"gabajo_{i}.png").convert_alpha())
        imagenes["arriba"].append(pygame.image.load(carpeta_gato + f"garriba_{i}.png").convert_alpha())
        imagenes["derecha"].append(pygame.image.load(carpeta_gato + f"gderecha_{i}.png").convert_alpha())
        imagenes["izquierda"].append(pygame.image.load(carpeta_gato + f"gizquierda_{i}.png").convert_alpha())

    imagenes["quieto"] = pygame.image.load(carpeta_gato + "gquieto.png").convert_alpha()
    return imagenes

# Crea el NPC humano con imagen y sus diálogos
def crear_npc_humano():
    ruta_imagen = "recursos/imagenes/caracteres/humano/humanoo.png"
    imagen_original = cargar_imagen_con_check(ruta_imagen)  # Verifica que la imagen existe
    imagen = pygame.transform.scale(imagen_original, (50, 70))  # Escala a tamaño del personaje

    dialogos = [
        # Cuadro 1: Bienvenida
        "¡Bienvenido! Mi nombre es Rastafari; Me alegra que estés aquí para comenzar esta aventura. Este mundo necesita héroes como tú.",

        # Cuadro 2: Información sobre maltrato animal
        "En Colombia se reportan más de 18.000 casos de maltrato animal al año. En Antioquia, los animales más afectados "
        "son los caballos usados para trabajos forzados, perros abandonados y gatos heridos. Muchos sufren abandono, peleas ilegales o falta de atención veterinaria.",

        # Cuadro 3: Tu misión en el juego
        "Tu misión es rescatarlos, brindarles cuidado y ayudarlos a tener una nueva oportunidad. ¿Estás listo para comenzar?",
    
        # Cuadro 4: Ir donde el siguiente NPC
        "Ve a la siguiente zona y habla con el siguiente NPC. Él te dará más información sobre tu Primera Misión."
    ]

    return NPCHumano(800, 680, imagen, dialogos)  # Posición inicial y configuración del NPC

