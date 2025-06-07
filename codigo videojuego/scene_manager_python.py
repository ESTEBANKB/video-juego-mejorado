import pygame
import constantes
from enum import Enum

class TipoEscena(Enum):
    MAPA_PRINCIPAL = "mapa_principal"
    REFUGIO = "refugio"

class GestorEscenas:
    def __init__(self):
        self.escena_actual = None
        self.escenas = {}
        self.en_transicion = False
        
    def registrar_escena(self, tipo_escena, escena):
        """Registra una nueva escena en el gestor"""
        self.escenas[tipo_escena] = escena
        
    def cambiar_escena(self, nuevo_tipo_escena, personaje=None):
        """Cambia de una escena a otra, limpiando la anterior"""
        if self.en_transicion:
            return False
            
        self.en_transicion = True
        
        # Limpiar escena anterior
        if self.escena_actual:
            self.limpiar_escena_actual()
            
        # Activar nueva escena
        if nuevo_tipo_escena in self.escenas:
            self.escena_actual = nuevo_tipo_escena
            escena = self.escenas[nuevo_tipo_escena]
            
            # Inicializar/resetear la nueva escena
            if hasattr(escena, 'inicializar_escena'):
                escena.inicializar_escena(personaje)
                
            print(f"Cambiado a escena: {nuevo_tipo_escena.value}")
            self.en_transicion = False
            return True
        else:
            print(f"Error: Escena {nuevo_tipo_escena.value} no encontrada")
            self.en_transicion = False
            return False
    
    def limpiar_escena_actual(self):
        """Limpia completamente la escena actual"""
        if self.escena_actual and self.escena_actual in self.escenas:
            escena = self.escenas[self.escena_actual]
            
            # Limpiar colisiones
            if hasattr(escena, 'colisiones') and hasattr(escena.colisiones, 'solid_tiles'):
                escena.colisiones.solid_tiles.empty()
                
            # Limpiar NPCs si existen
            if hasattr(escena, 'npcs'):
                if hasattr(escena.npcs, 'empty'):
                    escena.npcs.empty()
                elif isinstance(escena.npcs, list):
                    escena.npcs.clear()
                    
            # Limpiar otros elementos si existen
            if hasattr(escena, 'limpiar_escena'):
                escena.limpiar_escena()
                
            print(f"Escena {self.escena_actual.value} limpiada")
    
    def obtener_escena_actual(self):
        """Retorna la escena actual"""
        if self.escena_actual:
            return self.escenas.get(self.escena_actual)
        return None
    
    def actualizar(self):
        """Actualiza la escena actual"""
        escena = self.obtener_escena_actual()
        if escena and hasattr(escena, 'actualizar'):
            escena.actualizar()
    
    def dibujar(self, ventana):
        """Dibuja la escena actual"""
        escena = self.obtener_escena_actual()
        if escena and hasattr(escena, 'dibujar'):
            escena.dibujar(ventana)


# Clase base para todas las escenas
class EscenaBase:
    def __init__(self):
        self.activa = False
        self.colisiones = None
        self.camara = None
        
    def inicializar_escena(self, personaje=None):
        """Inicializa/resetea la escena cuando se activa"""
        self.activa = True
        
    def limpiar_escena(self):
        """Limpia recursos específicos de la escena"""
        self.activa = False
        
    def actualizar(self):
        """Actualiza la lógica de la escena"""
        pass
        
    def dibujar(self, ventana):
        """Dibuja la escena"""
        pass


# Refugio mejorado con gestión independiente
class RefugioMejorado(EscenaBase):
    def __init__(self, personaje):
        super().__init__()
        self.personaje = personaje
        self.posicion_entrada_personaje = None
        
        # Inicializar componentes del refugio
        self._cargar_mapa()
        self._configurar_colisiones()
        self._configurar_camara()
        
    def _cargar_mapa(self):
        """Carga el mapa del refugio"""
        from refugio import Refugio  # Importar tu clase existente
        refugio_temp = Refugio(self.personaje)
        self.mapa_refugio = refugio_temp.mapa_refugio
        self.tile_list_refugio = refugio_temp.tile_list_refugio
        
    def _configurar_colisiones(self):
        """Configura las colisiones específicas del refugio"""
        from colisiones_refugio import ColisionesRefugio
        self.colisiones = ColisionesRefugio()
        # NO cargar colisiones aquí, se hará en inicializar_escena
        
    def _configurar_camara(self):
        """Configura la cámara específica del refugio"""
        from camara import Camara
        ancho_refugio = constantes.COLUMNAS_REFUGIO * constantes.CUADRICULA_TAMAÑO
        alto_refugio = constantes.FILAS_REFUGIO * constantes.CUADRICULA_TAMAÑO
        self.camara = Camara(ancho_refugio, alto_refugio)
        
    def inicializar_escena(self, personaje=None):
        """Inicializa la escena del refugio de forma independiente"""
        super().inicializar_escena(personaje)
        
        if personaje:
            self.personaje = personaje
            
        # Limpiar colisiones anteriores completamente
        self.colisiones.solid_tiles.empty()
        
        # Recargar colisiones específicas del refugio
        self.colisiones.cargar_colisiones(self.mapa_refugio)
        
        # Posicionar personaje en la entrada del refugio
        if self.posicion_entrada_personaje:
            self.personaje.rect.x = self.posicion_entrada_personaje[0]
            self.personaje.rect.y = self.posicion_entrada_personaje[1]
        else:
            # Posición por defecto (centro del refugio)
            self.personaje.rect.x = (constantes.COLUMNAS_REFUGIO // 2) * constantes.CUADRICULA_TAMAÑO
            self.personaje.rect.y = (constantes.FILAS_REFUGIO // 2) * constantes.CUADRICULA_TAMAÑO
            
        print("Refugio inicializado - Colisiones cargadas:", len(self.colisiones.solid_tiles))
        
    def limpiar_escena(self):
        """Limpia recursos específicos del refugio"""
        super().limpiar_escena()
        if self.colisiones and hasattr(self.colisiones, 'solid_tiles'):
            self.colisiones.solid_tiles.empty()
            
    def establecer_posicion_entrada(self, x, y):
        """Establece donde aparecerá el personaje al entrar al refugio"""
        self.posicion_entrada_personaje = (x, y)
        
    def actualizar(self):
        """Actualiza la lógica del refugio"""
        if not self.activa:
            return
            
        # Actualizar cámara
        if self.camara:
            self.camara.update(self.personaje)
            
        # Aquí puedes agregar lógica específica del refugio
        # como NPCs, interacciones, etc.
        
    def dibujar(self, ventana):
        """Dibuja el refugio"""
        if not self.activa:
            return
            
        # Obtener desplazamiento de la cámara
        scroll = self.camara.camara_rect if self.camara else pygame.Rect(0, 0, 0, 0)
        
        # Dibujar tiles del refugio
        for y, fila in enumerate(self.mapa_refugio):
            for x, tile in enumerate(fila):
                if 0 <= tile < len(self.tile_list_refugio):
                    imagen_tile = self.tile_list_refugio[tile]
                    if imagen_tile:
                        ventana.blit(imagen_tile, 
                                   (x * constantes.CUADRICULA_TAMAÑO - scroll.x,
                                    y * constantes.CUADRICULA_TAMAÑO - scroll.y))


# Ejemplo de uso en tu juego principal
class JuegoPrincipal:
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
        self.reloj = pygame.time.Clock()
        
        # Crear personaje (aquí usarías tu clase de personaje)
        self.personaje = None  # Tu clase Personaje()
        
        # Crear gestor de escenas
        self.gestor_escenas = GestorEscenas()
        
        # Crear y registrar escenas
        self.refugio = RefugioMejorado(self.personaje)
        self.gestor_escenas.registrar_escena(TipoEscena.REFUGIO, self.refugio)
        
        # Aquí registrarías tu mapa principal también
        # self.mapa_principal = MapaPrincipal(self.personaje)
        # self.gestor_escenas.registrar_escena(TipoEscena.MAPA_PRINCIPAL, self.mapa_principal)
        
    def manejar_cambio_escena(self):
        """Maneja los cambios de escena basado en la lógica del juego"""
        keys = pygame.key.get_pressed()
        
        # Ejemplo: presionar R para ir al refugio
        if keys[pygame.K_r]:
            self.gestor_escenas.cambiar_escena(TipoEscena.REFUGIO, self.personaje)
            
        # Ejemplo: presionar M para volver al mapa principal
        if keys[pygame.K_m]:
            self.gestor_escenas.cambiar_escena(TipoEscena.MAPA_PRINCIPAL, self.personaje)
    
    def actualizar(self):
        """Actualiza el juego"""
        self.manejar_cambio_escena()
        
        # Actualizar personaje
        if self.personaje:
            self.personaje.actualizar()
            
            # Verificar colisiones con la escena actual
            escena_actual = self.gestor_escenas.obtener_escena_actual()
            if escena_actual and hasattr(escena_actual, 'colisiones'):
                escena_actual.colisiones.verificar_colision(self.personaje, "horizontal")
                escena_actual.colisiones.verificar_colision(self.personaje, "vertical")
        
        # Actualizar escena actual
        self.gestor_escenas.actualizar()
    
    def dibujar(self):
        """Dibuja el juego"""
        self.ventana.fill(constantes.VERDE)
        
        # Dibujar escena actual
        self.gestor_escenas.dibujar(self.ventana)
        
        # Dibujar personaje
        if self.personaje:
            escena_actual = self.gestor_escenas.obtener_escena_actual()
            if escena_actual and hasattr(escena_actual, 'camara'):
                scroll = escena_actual.camara.camara_rect
                self.ventana.blit(self.personaje.image, 
                                (self.personaje.rect.x - scroll.x, 
                                 self.personaje.rect.y - scroll.y))
        
        pygame.display.flip()
    
    def ejecutar(self):
        """Bucle principal del juego"""
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
            
            self.actualizar()
            self.dibujar()
            self.reloj.tick(constantes.FPS)
        
        pygame.quit()


# Para usar este sistema, reemplaza tu lógica actual con:
if __name__ == "__main__":
    juego = JuegoPrincipal()
    juego.ejecutar()