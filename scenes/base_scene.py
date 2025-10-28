"""
Clase de escena base para Galaxy Runner
Todas las escenas heredan de esta clase base.
"""
from abc import ABC, abstractmethod
import pygame

class BaseScene(ABC):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.db = game.db
        self.paths = game.paths
        
        # Colores comunes
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 200)
        self.RED = (200, 0, 0)
        self.GREEN = (0, 200, 0)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        
        # Fuentes comunes
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
    
    @abstractmethod
    def handle_event(self, event):
        """Manejar eventos de pygame"""
        pass
    
    @abstractmethod
    def update(self, dt):
        """Actualizar lógica de la escena"""
        pass
    
    @abstractmethod
    def render(self, screen):
        """Representar la escena en pantalla"""
        pass
    
    def draw_text(self, screen, text, font, color, x, y, centered=False):
        """Dibujar texto en pantalla"""
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
        else:
            screen.blit(text_surface, (x, y))
    
    def draw_button(self, screen, text, font, color, bg_color, x, y, width, height, centered=False):
        """Dibujar un botón"""
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, bg_color, button_rect)
        pygame.draw.rect(screen, self.BLACK, button_rect, 2)
        
        if centered:
            self.draw_text(screen, text, font, color, x + width//2, y + height//2, centered=True)
        else:
            self.draw_text(screen, text, font, color, x + 10, y + height//2 - font.get_height()//2)
        
        return button_rect
