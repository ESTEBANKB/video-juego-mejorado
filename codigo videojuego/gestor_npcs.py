#gestor_npcs.py

import pygame
from npc import GatoNPC
from npc_bienvenida import NPCHumano
from gato_humano import cargar_imagenes_gato, crear_npc_humano
from npc_mision import crear_npc_mision

class GestorNPCs:
    def __init__(self, sistema_misiones):
        self.sistema_misiones = sistema_misiones
        
        # Variables para evitar repetición de teclas
        self.tecla_e_presionada = False
        self.tecla_p_presionada = False
        
        # Crear NPCs
        try:
            self.npc_humano = crear_npc_humano()
        except Exception as e:
            print(f"Error creando NPC humano: {e}")
            self.npc_humano = None
            
        # CORREGIDO: Pasar el sistema de misiones al crear el NPC de misión
        self.npc_mision = crear_npc_mision(sistema_misiones)
        
        # Crear gato
        try:
            imagenes_gato = cargar_imagenes_gato()
            self.gato = GatoNPC(2430, 600, imagenes_gato)
        except Exception as e:
            print(f"Error creando gato: {e}")
            self.gato = None
        
        # Grupo de NPCs
        self.grupo_npcs = pygame.sprite.Group()
        if self.npc_humano:
            self.grupo_npcs.add(self.npc_humano)
        self.grupo_npcs.add(self.npc_mision)
        if self.gato:
            self.grupo_npcs.add(self.gato)
    
    def actualizar(self, personaje, teclas, grupo_item):
        """Actualiza todos los NPCs y maneja sus interacciones"""
        
        # PRIMER NPC: humano informativo con opciones (si existe)
        if self.npc_humano:
            tocando_npc = pygame.sprite.collide_rect(personaje, self.npc_humano)
            if tocando_npc and not self.npc_humano.dialogo_ya_mostrado:
                self.npc_humano.mostrar_dialogo()
                self.npc_humano.dialogo_ya_mostrado = True
            elif not tocando_npc:
                self.npc_humano.ocultar_dialogo()
                self.npc_humano.dialogo_ya_mostrado = False

            if self.npc_humano.dialogo_visible:
                # Verificar si tiene el método cambiar_respuesta
                if hasattr(self.npc_humano, 'cambiar_respuesta'):
                    if teclas[pygame.K_e] and not self.tecla_e_presionada:
                        self.npc_humano.cambiar_respuesta()
                        self.tecla_e_presionada = True
                    elif not teclas[pygame.K_e]:
                        self.tecla_e_presionada = False

                if teclas[pygame.K_p] and not self.tecla_p_presionada:
                    self.npc_humano.avanzar_dialogo()
                    self.tecla_p_presionada = True
                elif not teclas[pygame.K_p]:
                    self.tecla_p_presionada = False

        # SEGUNDO NPC: misión y desbloqueo de monedas
        if personaje.rect.colliderect(self.npc_mision.rect):
            if teclas[pygame.K_p] and not self.tecla_p_presionada:
                self.npc_mision.avanzar_dialogo(grupo_item)
                self.tecla_p_presionada = True
            elif not teclas[pygame.K_p]:
                self.tecla_p_presionada = False
            self.npc_mision.mostrar_dialogo()
        else:
            self.npc_mision.ocultar_dialogo()

        # Gato sigue al personaje si colisiona (si existe)
        if self.gato:
            if pygame.sprite.collide_rect(personaje, self.gato) and not self.gato.siguiendo:
                self.gato.siguiendo = True
            self.gato.actualizar(personaje)
    
    def dibujar(self, ventana, camara):
        """Dibuja todos los NPCs en pantalla"""
        # Dibujar gato (si existe)
        if self.gato:
            try:
                self.gato.dibujar(ventana, camara)
            except Exception as e:
                print(f"Error dibujando gato: {e}")
        
        # Dibujar NPC humano (si existe)
        if self.npc_humano:
            try:
                self.npc_humano.dibujar(ventana, camara)
            except Exception as e:
                print(f"Error dibujando NPC humano: {e}")
        
        # Dibujar NPC de misión
        try:
            self.npc_mision.dibujar(ventana, camara)
            self.npc_mision.dibujar_dialogo(ventana)
        except Exception as e:
            print(f"Error dibujando NPC de misión: {e}")
    
    def manejar_evento_tecla(self, evento):
        """Maneja eventos específicos de teclas para los NPCs"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p:
                # Lógica adicional para la tecla P si es necesaria
                pass
            elif evento.key == pygame.K_e:
                # Lógica adicional para la tecla E si es necesaria
                pass
    
    def obtener_sistema_misiones(self):
        """Retorna el sistema de misiones para uso externo"""
        return self.sistema_misiones