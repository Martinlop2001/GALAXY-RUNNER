"""
Options Scene for Galaxy Runner
Settings and configuration
"""
import pygame
from .base_scene import BaseScene

class OptionsScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.selected_option = 0
        self.options = [
            ("Volume", self.toggle_volume),
            ("Difficulty", self.change_difficulty),
            ("Back", self.go_back)
        ]
        
        # Ajustes
        self.volume = 50
        self.difficulty = "Normal"
        self.difficulty_levels = ["Easy", "Normal", "Hard"]
        self.difficulty_index = 1
    
    def draw_stars_background(self):
        """Dibujar fondo de estrellas si se desea (opcional)"""
        pass
    
    def load_settings(self):
        """Cargar ajustes desde la BD para el jugador actual"""
        # Intentar obtener ajustes si hay jugador activo
        try:
            # ejemplo: player_id debería provenir del juego/DB en contexto real
            settings = self.db.get_settings(player_id=1)
            if settings:
                self.volume = settings.get("volumen", self.volume)
                self.difficulty = settings.get("dificultad", self.difficulty)
        except Exception:
            pass
    
    def save_settings(self):
        """Guardar ajustes en la BD"""
        try:
            self.db.update_settings(player_id=1, volume=self.volume, difficulty=self.difficulty)
        except Exception:
            pass
    
    def handle_event(self, event):
        """Manejar navegación y selección de opciones"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                _, action = self.options[self.selected_option]
                action()
            elif event.key == pygame.K_ESCAPE:
                self.go_back()
    
    def update(self, dt):
        pass
    
    def render(self, screen):
        screen.fill(self.BLACK)
        self.draw_text(screen, "Options", self.font_large, self.WHITE, self.screen.get_width()//2, 60, centered=True)
        
        start_y = 140
        for idx, (label, _) in enumerate(self.options):
            color = self.YELLOW if idx == self.selected_option else self.WHITE
            self.draw_button(screen, label, self.font_medium, color, self.GRAY, self.screen.get_width()//2 - 150, start_y + idx*64, 300, 48)
    
    def toggle_volume(self):
        """Alternar volumen (ejemplo simple)"""
        self.volume = 0 if self.volume > 0 else 50
        self.save_settings()
    
    def change_difficulty(self):
        """Cambiar dificultad cíclicamente"""
        self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulty_levels)
        self.difficulty = self.difficulty_levels[self.difficulty_index]
        self.save_settings()
    
    def go_back(self):
        """Volver al menú principal (importación local)"""
        from .start_menu import StartMenuScene
        self.game.set_scene(StartMenuScene(self.game))
