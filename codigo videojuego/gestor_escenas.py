# gestor_escenas.py - Sistema de gestión de escenas del juego

from enum import Enum

class TipoEscena(Enum):
    """Enumera los tipos de escenas disponibles en el juego."""
    MAPA_PRINCIPAL = "mapa_principal"
    REFUGIO = "refugio"

class GestorEscenas:
    """
    Clase que gestiona las diferentes escenas del juego.
    Controla el cambio entre escenas y su inicialización/limpieza.
    """
    
    def __init__(self):
        """Inicializa el gestor de escenas."""
        self.escena_actual = None
        self.escenas = {}
        self.en_transicion = False
        
    def registrar_escena(self, tipo_escena, escena):
        """
        Registra una nueva escena en el gestor.
        
        Args:
            tipo_escena (TipoEscena): El tipo de escena a registrar
            escena: La instancia de la escena a registrar
        """
        self.escenas[tipo_escena] = escena
        print(f"Escena registrada: {tipo_escena.value}")
        
    def cambiar_escena(self, nuevo_tipo_escena, personaje=None):
        """
        Cambia a una nueva escena.
        
        Args:
            nuevo_tipo_escena (TipoEscena): El tipo de escena a la que cambiar
            personaje: Referencia al personaje (opcional)
            
        Returns:
            bool: True si el cambio fue exitoso, False si falló
        """
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
            
            # Inicializar la nueva escena si tiene el método
            if hasattr(escena, 'inicializar_escena'):
                escena.inicializar_escena(personaje)
                
            print(f"Cambiado a escena: {nuevo_tipo_escena.value}")
            self.en_transicion = False
            return True
        else:
            print(f"Error: Escena no encontrada: {nuevo_tipo_escena.value}")
            self.en_transicion = False
            return False
    
    def limpiar_escena_actual(self):
        """Limpia los recursos de la escena actual antes del cambio."""
        if self.escena_actual and self.escena_actual in self.escenas:
            escena = self.escenas[self.escena_actual]
            
            # Limpiar colisiones si existen
            if hasattr(escena, 'colisiones') and hasattr(escena.colisiones, 'solid_tiles'):
                escena.colisiones.solid_tiles.empty()
                print(f"Colisiones limpiadas para escena: {self.escena_actual.value}")
                
            # Limpiar NPCs si existen
            if hasattr(escena, 'npcs_activos'):
                escena.npcs_activos = False
                
            # Llamar al método de limpieza personalizado si existe
            if hasattr(escena, 'limpiar_escena'):
                escena.limpiar_escena()
    
    def obtener_escena_actual(self):
        """
        Obtiene la instancia de la escena actual.
        
        Returns:
            La instancia de la escena actual o None si no hay escena activa
        """
        if self.escena_actual:
            return self.escenas.get(self.escena_actual)
        return None
    
    def obtener_tipo_escena_actual(self):
        """
        Obtiene el tipo de la escena actual.
        
        Returns:
            TipoEscena: El tipo de la escena actual o None
        """
        return self.escena_actual
    
    def esta_en_transicion(self):
        """
        Verifica si el gestor está en proceso de transición.
        
        Returns:
            bool: True si está en transición, False si no
        """
        return self.en_transicion
    
    def listar_escenas_registradas(self):
        """
        Lista todas las escenas registradas.
        
        Returns:
            list: Lista con los tipos de escenas registradas
        """
        return list(self.escenas.keys())
    
    def escena_existe(self, tipo_escena):
        """
        Verifica si una escena está registrada.
        
        Args:
            tipo_escena (TipoEscena): El tipo de escena a verificar
            
        Returns:
            bool: True si la escena existe, False si no
        """
        return tipo_escena in self.escenas