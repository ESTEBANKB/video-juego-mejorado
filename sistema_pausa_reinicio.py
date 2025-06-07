# sistema_pausa_reinicio.py - Sistema de pausa y reinicio para el juego S.E.A

import pygame
import constantes
from enum import Enum

class EstadoJuego(Enum):
    JUGANDO = "jugando"
    PAUSADO = "pausado"
    REINICIANDO = "reiniciando"

class SistemaPausaReinicio:
    def __init__(self, ventana, fuente):
        self.ventana = ventana
        self.fuente = fuente
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
        self.estado = EstadoJuego.JUGANDO
        self.mostrar_menu_pausa = False
        
        # Colores
        self.COLOR_OVERLAY = (0, 0, 0, 128)  # Negro semi-transparente
        self.COLOR_TEXTO_TITULO = (255, 255, 255)  # Blanco
        self.COLOR_TEXTO_OPCION = (200, 200, 200)  # Gris claro
        self.COLOR_TEXTO_SELECCIONADO = (255, 255, 0)  # Amarillo
        
        # Opciones del menú de pausa
        self.opciones_pausa = [
            "Continuar",
            "Reiniciar Juego",
            "Salir"
        ]
        self.opcion_seleccionada = 0
        
        # Control de teclas
        self.tecla_pausa_presionada = False
        self.tecla_enter_presionada = False
        self.tecla_arriba_presionada = False
        self.tecla_abajo_presionada = False
        
        # Variables para reinicio
        self.reiniciar_solicitado = False
        self.salir_solicitado = False
        
    def manejar_eventos(self, evento):
        """Maneja los eventos del sistema de pausa"""
        if evento.type == pygame.KEYDOWN:
            # CORREGIDO: Usar RETURN para la tecla ENTER principal
            if evento.key == pygame.K_RETURN:  # ENTER para pausar/despausar
                if self.estado == EstadoJuego.JUGANDO:
                    self.pausar_juego()
                elif self.estado == EstadoJuego.PAUSADO:
                    # Si estamos en pausa, ENTER ejecuta la opción seleccionada
                    self.ejecutar_opcion_seleccionada()
            elif self.estado == EstadoJuego.PAUSADO:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    self.cambiar_seleccion(-1)
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    self.cambiar_seleccion(1)
                elif evento.key == pygame.K_SPACE:  # ESPACIO también selecciona
                    self.ejecutar_opcion_seleccionada()
                elif evento.key == pygame.K_ESCAPE:  # ESC para continuar directamente
                    self.continuar_juego()
    
    def actualizar(self, teclas):
        """Actualiza el estado del sistema de pausa"""
        # Solo procesar si el juego está pausado
        if self.estado != EstadoJuego.PAUSADO:
            return
            
        # Aquí podrías agregar lógica adicional si es necesario
        pass
    
    def alternar_pausa(self):
        """Alterna entre pausado y jugando"""
        if self.estado == EstadoJuego.JUGANDO:
            self.pausar_juego()
        elif self.estado == EstadoJuego.PAUSADO:
            self.continuar_juego()
    
    def pausar_juego(self):
        """Pausa el juego"""
        self.estado = EstadoJuego.PAUSADO
        self.mostrar_menu_pausa = True
        self.opcion_seleccionada = 0
        print("Juego pausado")
    
    def continuar_juego(self):
        """Continúa el juego"""
        self.estado = EstadoJuego.JUGANDO
        self.mostrar_menu_pausa = False
        print("Juego continuado")
    
    def cambiar_seleccion(self, direccion):
        """Cambia la opción seleccionada en el menú de pausa"""
        self.opcion_seleccionada = (self.opcion_seleccionada + direccion) % len(self.opciones_pausa)
    
    def ejecutar_opcion_seleccionada(self):
        """Ejecuta la opción seleccionada del menú"""
        opcion = self.opciones_pausa[self.opcion_seleccionada]
        
        if opcion == "Continuar":
            self.continuar_juego()
        elif opcion == "Reiniciar Juego":
            self.solicitar_reinicio()
        elif opcion == "Salir":
            self.solicitar_salida()
    
    def solicitar_reinicio(self):
        """Solicita el reinicio del juego"""
        self.reiniciar_solicitado = True
        self.estado = EstadoJuego.REINICIANDO
        print("Reinicio solicitado")
    
    def solicitar_salida(self):
        """Solicita salir del juego"""
        self.salir_solicitado = True
        print("Salida solicitada")
    
    def obtener_reinicio_solicitado(self):
        """Verifica si se solicitó reinicio y resetea la flag"""
        if self.reiniciar_solicitado:
            self.reiniciar_solicitado = False
            return True
        return False
    
    def obtener_salida_solicitada(self):
        """Verifica si se solicitó salida y resetea la flag"""
        if self.salir_solicitado:
            self.salir_solicitado = False
            return True
        return False
    
    def esta_pausado(self):
        """Verifica si el juego está pausado"""
        return self.estado == EstadoJuego.PAUSADO
    
    def dibujar_overlay_pausa(self):
        """Dibuja el overlay de pausa sobre el juego"""
        if not self.mostrar_menu_pausa:
            return
        
        # Crear superficie semi-transparente
        overlay = pygame.Surface((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.ventana.blit(overlay, (0, 0))
        
        # Dibujar título "PAUSADO"
        titulo = self.fuente_grande.render("JUEGO PAUSADO", True, self.COLOR_TEXTO_TITULO)
        titulo_rect = titulo.get_rect(center=(constantes.ANCHO_VENTANA // 2, 200))
        self.ventana.blit(titulo, titulo_rect)
        
        # Dibujar opciones del menú
        y_inicial = 300
        espacio_entre_opciones = 50
        
        for i, opcion in enumerate(self.opciones_pausa):
            # Determinar color según si está seleccionada
            color = self.COLOR_TEXTO_SELECCIONADO if i == self.opcion_seleccionada else self.COLOR_TEXTO_OPCION
            
            # Renderizar texto
            texto = self.fuente.render(opcion, True, color)
            texto_rect = texto.get_rect(center=(constantes.ANCHO_VENTANA // 2, y_inicial + i * espacio_entre_opciones))
            
            # Dibujar indicador de selección
            if i == self.opcion_seleccionada:
                indicador = self.fuente.render("> ", True, self.COLOR_TEXTO_SELECCIONADO)
                indicador_rect = indicador.get_rect()
                indicador_rect.right = texto_rect.left - 10
                indicador_rect.centery = texto_rect.centery
                self.ventana.blit(indicador, indicador_rect)
            
            self.ventana.blit(texto, texto_rect)
        
        # Instrucciones CORREGIDAS
        instrucciones = [
            "Usa ↑↓ o W/S para navegar",
            "ENTER o ESPACIO para seleccionar",
            "ESC para continuar directamente"
        ]
        
        y_instrucciones = 500
        for i, instruccion in enumerate(instrucciones):
            texto_instruccion = self.fuente_pequena.render(instruccion, True, self.COLOR_TEXTO_OPCION)
            texto_rect = texto_instruccion.get_rect(center=(constantes.ANCHO_VENTANA // 2, y_instrucciones + i * 25))
            self.ventana.blit(texto_instruccion, texto_rect)
    
    def dibujar_indicador_pausa(self):
        """Dibuja un pequeño indicador de que se puede pausar"""
        if self.estado == EstadoJuego.JUGANDO:
            texto = self.fuente_pequena.render("Presiona ENTER para pausar", True, (255, 255, 255))
            self.ventana.blit(texto, (10, constantes.ALTO_VENTANA - 30))
    
    def reiniciar_estado(self):
        """Reinicia el estado del sistema de pausa"""
        self.estado = EstadoJuego.JUGANDO
        self.mostrar_menu_pausa = False
        self.opcion_seleccionada = 0
        self.reiniciar_solicitado = False
        self.salir_solicitado = False
        print("Sistema de pausa reiniciado")

# Función auxiliar para crear el sistema de pausa
def crear_sistema_pausa(ventana, fuente):
    """Función auxiliar para crear una instancia del sistema de pausa"""
    return SistemaPausaReinicio(ventana, fuente)