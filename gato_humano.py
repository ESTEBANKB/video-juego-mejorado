# gato_humano.py - Versión mejorada con lógica consistente
import os
import pygame
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
        self.dialogo_actual = 0
        self.texto_dialogo_completo = ""
        
        # PROTECCIÓN ANTI-SPAM para evitar múltiples avances
        self.ultimo_avance = 0
        self.cooldown_avance = 200  # 200ms entre avances
        
        # Fuentes para el diálogo
        self.fuente_dialogo = pygame.font.Font(None, 22)  # Reducido de 20 a 18
        self.fuente_pie = pygame.font.Font(None, 18)      # Reducido de 18 a 16
        
        # Rectángulo del cuadro de diálogo (más alto para textos largos)
        self.dialogo_rect = pygame.Rect(50, 350, 700, 200)  # Aumentado altura de 150 a 200
        
        # Diálogos específicos del NPC humano
        self.dialogos = [
            "¡Bienvenido! Mi nombre es Rastafari; Me alegra que estés aquí para comenzar esta aventura. Este mundo necesita héroes como tú.",
            
            "En Colombia se reportan más de 18.000 casos de maltrato animal al año. En Antioquia, los animales más afectados son los caballos usados para trabajos forzados, perros abandonados y gatos heridos. Muchos sufren abandono, peleas ilegales o falta de atención veterinaria.",
            
            "Tu misión es rescatarlos, brindarles cuidado y ayudarlos a tener una nueva oportunidad. ¿Estás listo para comenzar?",
            
            "Ve a la siguiente zona y habla con Rodrigo. Él te dará más información sobre tu Primera Misión."
        ]
    
    def _cargar_imagen_con_check(self, ruta):
        """Carga una imagen y verifica que exista; si no, muestra un error rojo"""
        if not os.path.exists(ruta):
            print(f"Error: No se encontró la imagen en la ruta {ruta}")
            superficie_error = pygame.Surface((50, 70))
            superficie_error.fill((255, 0, 0))  # Relleno rojo como aviso de error
            return superficie_error
        
        imagen_original = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(imagen_original, (50, 70))
    
    def actualizar(self, personaje, teclas=None, evento=None):
        """Actualiza el estado del NPC basado en la proximidad del personaje"""
        distancia = pygame.math.Vector2(
            personaje.rect.centerx - self.rect.centerx,
            personaje.rect.centery - self.rect.centery
        ).length()
        
        # Si el personaje está lejos, resetear el flag de diálogo mostrado
        if distancia > 100:
            self.dialogo_ya_mostrado = False
            self.dialogo_actual = 0
    
    def mostrar_dialogo(self):
        """Muestra el diálogo del NPC"""
        print(f"mostrar_dialogo() llamado - dialogo_activo: {self.dialogo_activo}, ya_mostrado: {self.dialogo_ya_mostrado}")
        
        if not self.dialogo_activo and not self.dialogo_ya_mostrado:
            self.dialogo_actual = 0
            self.texto_dialogo_completo = self.dialogos[self.dialogo_actual]
            self.dialogo_activo = True
            self.dialogo_ya_mostrado = True
            #print(f"Diálogo iniciado - índice: {self.dialogo_actual}, texto: {self.texto_dialogo_completo[:50]}...")
        else:
            print("Diálogo no iniciado - condiciones no cumplidas")
    
    def mostrar_dialogo_aleatorio(self):
        """Alias para mostrar_dialogo para compatibilidad"""
        self.mostrar_dialogo()
    
    def ocultar_dialogo(self):
        """Oculta el diálogo del NPC"""
        self.dialogo_activo = False
    
    def avanzar_dialogo(self):
        """Avanza al siguiente diálogo o cierra si es el último - CON PROTECCIÓN ANTI-SPAM"""
        # Protección anti-spam usando tiempo
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_avance < self.cooldown_avance:
            print(f"Bloqueado por cooldown: {tiempo_actual - self.ultimo_avance}ms < {self.cooldown_avance}ms")
            return False
        
        if not self.dialogo_activo:
            print("Error: Intentando avanzar diálogo cuando no está activo")
            return False
        
        # Actualizar el tiempo del último avance
        self.ultimo_avance = tiempo_actual
        
        #print(f"ANTES - Diálogo actual: {self.dialogo_actual}, Total: {len(self.dialogos)}")
        
        self.dialogo_actual += 1
        
        #print(f"DESPUÉS - Diálogo actual: {self.dialogo_actual}, Total: {len(self.dialogos)}")
        
        # Si hay más diálogos, mostrar el siguiente
        if self.dialogo_actual < len(self.dialogos):
            self.texto_dialogo_completo = self.dialogos[self.dialogo_actual]
            print(f"Texto nuevo: {self.texto_dialogo_completo[:50]}...")
            return True
        else:
            # Si no hay más diálogos, cerrar el cuadro
            print("Cerrando diálogo - llegamos al final")
            self.ocultar_dialogo()
            self.dialogo_actual = 0  # Reiniciar para futuras interacciones
            return False
    
    def dibujar(self, ventana, camara):
        """Dibuja el NPC en la ventana ajustado a la cámara"""
        ventana.blit(self.image, camara.aplicar(self.rect))
    
    def dibujar_dialogo(self, ventana):
        """Dibuja el cuadro de diálogo y el texto si está activo"""
        if not self.dialogo_activo:
            return
        
        # Fondo del cuadro de diálogo (semi-transparente negro)
        s = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        s.set_alpha(230)
        s.fill((0, 0, 0))
        ventana.blit(s, (self.dialogo_rect.x, self.dialogo_rect.y))
        
        # Dibujar borde blanco
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)
        
        # Ajustar texto a múltiples líneas con más caracteres por línea
        lineas_envueltas = []
        parrafos = self.texto_dialogo_completo.split('\n')
        for parrafo in parrafos:
            if parrafo.strip():
                # Aumentado de 60 a 80 caracteres por línea para aprovechar mejor el espacio
                lineas_envueltas.extend(textwrap.wrap(parrafo, width=80))
            else:
                lineas_envueltas.append("")
        
        # Dibujar texto línea por línea
        y_offset = self.dialogo_rect.y + 15  # Reducido margen superior
        espacio_entre_lineas = 6  # Reducido espacio entre líneas de 10 a 6
        
        for linea in lineas_envueltas:
            # Verificar si la línea cabe en el cuadro
            if y_offset + self.fuente_dialogo.get_height() > self.dialogo_rect.bottom - 40:
                # Si no cabe, mostrar indicador de texto cortado
                texto_cortado = "..."
                img_cortado = self.fuente_dialogo.render(texto_cortado, True, (255, 255, 0))
                ventana.blit(img_cortado, (self.dialogo_rect.x + 20, y_offset))
                break
            
            img_texto = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            ventana.blit(img_texto, (self.dialogo_rect.x + 15, y_offset))  # Reducido margen izquierdo
            y_offset += self.fuente_dialogo.get_height() + espacio_entre_lineas
        
        # Mostrar instrucciones en el pie
        if self.dialogo_actual < len(self.dialogos) - 1:
            texto_pie = f"Presiona P para continuar... ({self.dialogo_actual + 1}/{len(self.dialogos)})"
        else:
            texto_pie = f"Presiona P para cerrar ({self.dialogo_actual + 1}/{len(self.dialogos)})"
        
        img_pie = self.fuente_pie.render(texto_pie, True, (200, 200, 200))
        ventana.blit(img_pie, (self.dialogo_rect.x + 15, self.dialogo_rect.bottom - 25))

# Funciones auxiliares para compatibilidad con el código existente
def cargar_imagen_con_check(ruta):
    """Carga una imagen y verifica que exista; si no, muestra un error rojo"""
    if not os.path.exists(ruta):
        print(f"Error: no se encontró la imagen en la ruta {ruta}")
        superficie_error = pygame.Surface((50, 70))
        superficie_error.fill((255, 0, 0))  # Relleno rojo como aviso de error
        return superficie_error
    return pygame.image.load(ruta).convert_alpha()  # Carga con transparencia

def cargar_imagenes_gato():
    """Carga las animaciones del personaje gato (3 imágenes por dirección + quieto)"""
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

def crear_npc_humano(x=800, y=680, sistema_misiones=None):
    """Función helper para crear una instancia del NPC humano."""
    return NPCHumano(x, y, sistema_misiones)