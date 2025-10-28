"""
Leaderboard Scene for Galaxy Runner
Shows high scores and current player stats
"""
import pygame
from .base_scene import BaseScene

class LeaderboardScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.selected_tab = 0
        self.tabs = ["Global", "Level 1", "Level 2", "Level 3"]
        self.leaderboard_data = []
        # Cargar datos iniciales
        self.load_leaderboard_data()
    
    def draw_stars_background(self):
        """Dibujar fondo de estrellas si se desea (opcional)"""
        pass
    
    def load_leaderboard_data(self):
        """Cargar datos desde la base de datos"""
        try:
            self.leaderboard_data = self.db.get_leaderboard(limit=10)
        except Exception:
            self.leaderboard_data = []
    
    def handle_event(self, event):
        """Volver al menú principal con ESC o tecla B"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                from .start_menu import StartMenuScene
                self.game.set_scene(StartMenuScene(self.game))
    
    def update(self, dt):
        """Actualizar animaciones o datos"""
        pass
    
    def render(self, screen):
        """Renderizar la tabla de puntuaciones"""
        screen.fill(self.BLACK)
        self.draw_text(screen, "Leaderboard", self.font_large, self.WHITE, self.screen.get_width()//2, 40, centered=True)
        
        y = 120
        for idx, row in enumerate(self.leaderboard_data):
            name = row.get("nombre") or row.get("name") or "Unknown"
            score = row.get("puntuacion") or row.get("score") or 0
            self.draw_text(screen, f"{idx+1}. {name} - {score}", self.font_medium, self.WHITE, 80, y, centered=False)
            y += 36
