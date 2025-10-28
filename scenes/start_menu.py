"""
Start Menu Scene for Galaxy Runner
"""
import pygame
from .base_scene import BaseScene
from ui import UIHelper

class StartMenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.selected_option = 0
        self.options = [
            ("Play", self.start_game),
            ("Leaderboard", self.show_leaderboard),
            ("Options", self.show_options),
            ("Exit", self.exit_game)
        ]
        
        # Fondo de estrellas (sin entrada de nombre en el menú principal)
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill(self.BLACK)
        self.draw_stars_background()
    
    def draw_stars_background(self):
        """Dibujar un campo de estrellas simple en la superficie de fondo"""
        self.background.fill(self.BLACK)
        UIHelper.draw_starfield(self.background, self.screen.get_width(), self.screen.get_height(), num_stars=120, seed=42)
    
    def handle_event(self, event):
        """Manejar entradas de teclado y ratón (sin input de nombre en el menú)"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                _, action = self.options[self.selected_option]
                action()
            elif event.key == pygame.K_ESCAPE:
                self.exit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # (Opcional) detectar clicks sobre botones por su posición
            mx, my = event.pos
            start_y = 180
            for idx in range(len(self.options)):
                bx = self.screen.get_width()//2 - 150
                by = start_y + idx*60
                rect = pygame.Rect(bx, by, 300, 48)
                if rect.collidepoint((mx, my)):
                    _, action = self.options[idx]
                    action()
                    break
    
    def update(self, dt):
        """Actualización por frame (animaciones, temporizadores)"""
        pass
    
    def render(self, screen):
        """Renderizar menú de inicio (sin caja de entrada)"""
        screen.blit(self.background, (0,0))
        
        # Título
        self.draw_text(screen, "Galaxy Runner", self.font_large, self.WHITE, self.screen.get_width()//2, 80, False)
        
        # Opciones
        start_y = 180
        for idx, (label, _) in enumerate(self.options):
            color = self.YELLOW if idx == self.selected_option else self.WHITE
            # dibujar botón; el último argumento es booleana para centrar texto (usado como positional)
            self.draw_button(screen, label, self.font_medium, color, self.GRAY, self.screen.get_width()//2 - 150, start_y + idx*60, 300, 48, False)
    
    def start_game(self):
        """Iniciar la escena de juego (importación local para evitar circularidad)"""
        from .game_scene import GameScene
        self.game.set_scene(GameScene(self.game))
    
    def show_leaderboard(self):
        """Mostrar la tabla de puntuaciones (importación local)"""
        from .leaderboard_scene import LeaderboardScene
        self.game.set_scene(LeaderboardScene(self.game))
    
    def show_options(self):
        """Mostrar las opciones (importación local)"""
        from .options_scene import OptionsScene
        self.game.set_scene(OptionsScene(self.game))
    
    def exit_game(self):
        """Salir del juego"""
        self.game.running = False
