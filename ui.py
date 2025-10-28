"""
Utilidades de UI para Galaxy Runner
Componentes de interfaz comunes y ayudantes
"""

import pygame

class UIHelper:
    @staticmethod
    def draw_text(screen, text, font, color, x, y, centered=False):
        """Dibujar texto en pantalla"""
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
        else:
            screen.blit(text_surface, (x, y))
    
    @staticmethod
    def draw_button(screen, text, font, color, bg_color, x, y, width, height, centered=False):
        """Dibujar un botón"""
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, bg_color, button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
        
        if centered:
            UIHelper.draw_text(screen, text, font, color, x + width//2, y + height//2, centered=True)
        else:
            UIHelper.draw_text(screen, text, font, color, x + 10, y + height//2 - font.get_height()//2)
        
        return button_rect
    
    @staticmethod
    def draw_progress_bar(screen, x, y, width, height, progress, max_progress, 
                         bg_color=(128, 128, 128), fill_color=(0, 255, 0)):
        """Dibujar una barra de progreso"""
        # Fondo
        pygame.draw.rect(screen, bg_color, (x, y, width, height))
        
        # Relleno
        if max_progress > 0:
            fill_width = int(width * progress / max_progress)
            pygame.draw.rect(screen, fill_color, (x, y, fill_width, height))
        
        # Borde
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 2)
    
    @staticmethod
    def draw_starfield(screen, width, height, num_stars=100, seed=42):
        """Dibujar un fondo simple de campo de estrellas"""
        import random
        random.seed(seed)
        
        for _ in range(num_stars):
            x = random.randint(0, width)
            y = random.randint(0, height)
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), 1)
    
    @staticmethod
    def create_gradient_surface(width, height, color1, color2, vertical=True):
        """Crear una superficie con degradado"""
        surface = pygame.Surface((width, height))
        
        if vertical:
            for y in range(height):
                ratio = y / height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        else:
            for x in range(width):
                ratio = x / width
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
        
        return surface