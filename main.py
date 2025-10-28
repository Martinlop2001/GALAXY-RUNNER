#!/usr/bin/env python3
"""
Galaxy Runner - Endless Runner Game
Main entry point for the game
"""

import pygame
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scenes.start_menu import StartMenuScene
from db import DatabaseManager
from paths import Paths

class GalaxyRunner:
    def __init__(self):
        pygame.init()
        
        # Constantes del juego
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # Inicializar pantalla
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Galaxy Runner")
        
        # Inicializar reloj
        self.clock = pygame.time.Clock()
        
        # Inicializar rutas
        self.paths = Paths()
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        
        # Estado del juego
        self.running = True
        self.current_scene = None
        
        # Inicializar primera escena
        self.set_scene(StartMenuScene(self))
    
    def set_scene(self, scene):
        """Cambiar a una nueva escena"""
        self.current_scene = scene
    
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0  # Tiempo delta en segundos
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_scene.handle_event(event)
            
            # Actualizar escena actual
            self.current_scene.update(dt)
            
            # Renderizar escena actual
            self.current_scene.render(self.screen)
            
            pygame.display.flip()
        
        # Limpieza
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GalaxyRunner()
    game.run()
