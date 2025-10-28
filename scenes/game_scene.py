"""
Game Scene for Galaxy Runner
Main gameplay scene with runner mechanics
"""
import pygame
import random
from .base_scene import BaseScene

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.velocity = pygame.Vector2(0, 0)
    
    def update(self, dt):
        self.rect.x += int(self.velocity.x * dt)
        self.rect.y += int(self.velocity.y * dt)
    
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ship(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, (0, 200, 0))
        self.shield_active = False
        self.shield_timer = 0.0
        self.health = 100
    
    def update(self, dt):
        super().update(dt)
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False
    
    def move_left(self):
        self.velocity.x = -300
    
    def move_right(self):
        self.velocity.x = 300
    
    def stop(self):
        self.velocity.x = 0
    
    def activate_shield(self, duration=6.0):
        self.shield_active = True
        self.shield_timer = duration
    
    def take_damage(self, amount=10):
        if not self.shield_active:
            self.health = max(0, self.health - amount)
            return True
        return False

class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Ship(self.screen.get_width()//2 - 20, self.screen.get_height() - 100)
        self.score = 0
        self.paused = False

        # Estadísticas de partida (se guardan al final si corresponde)
        self.play_time = 0.0
        self.stars_collected = 0
        self.max_combo = 0
        self.level = 1

        # Estado de fin de partida / input para nombre
        self.game_over = False
        self.game_over_input_active = False
        self.game_over_name = ""
        self.game_over_rect = pygame.Rect(self.screen.get_width()//2 - 200, self.screen.get_height()//2 - 90, 400, 180)
        self.name_input_rect = pygame.Rect(self.game_over_rect.x + 40, self.game_over_rect.y + 70, 320, 36)

    def trigger_game_over(self):
        """Activar modo Game Over y preparar la entrada de nombre para guardar record"""
        self.game_over = True
        self.paused = True
        self.game_over_input_active = True
        self.game_over_name = ""
        pygame.key.start_text_input()  # Habilitar entrada de texto (pygame.TEXTINPUT)

    def handle_event(self, event):
        """Manejar controles y entrada cuando hay Game Over se usa entrada de texto"""
        # Si estamos en modo Game Over, procesar entrada de texto primero
        if self.game_over:
            # Eventos TEXTINPUT (recomendado para entrada de nombres)
            if event.type == pygame.TEXTINPUT:
                if self.game_over_input_active and len(self.game_over_name) < 16:
                    self.game_over_name += event.text
                return

            # Click para activar/desactivar el input
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.name_input_rect.collidepoint(event.pos):
                    if not self.game_over_input_active:
                        self.game_over_input_active = True
                        pygame.key.start_text_input()
                else:
                    # click fuera: si ya hay nombre, podemos guardar; si no, desactivar input
                    if self.game_over_input_active:
                        self.game_over_input_active = False
                        pygame.key.stop_text_input()
                return

            # Teclas mientras estamos en Game Over
            if event.type == pygame.KEYDOWN:
                if self.game_over_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.game_over_name = self.game_over_name[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        # Guardar score cuando el jugador confirma con Enter
                        self._save_score_and_finish()
                else:
                    # Si no estamos editando el nombre, permitir volver al menú con ESC
                    if event.key == pygame.K_ESCAPE:
                        from .start_menu import StartMenuScene
                        pygame.key.stop_text_input()
                        self.game.set_scene(StartMenuScene(self.game))
                return

            return  # ignorar otro tipo de eventos cuando estamos en Game Over

        # Si no es Game Over, comportamiento normal de la escena
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Volver al menú principal (importación local)
                from .start_menu import StartMenuScene
                self.game.set_scene(StartMenuScene(self.game))
            elif event.key == pygame.K_LEFT:
                self.player.move_left()
            elif event.key == pygame.K_RIGHT:
                self.player.move_right()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.player.stop()

    def _save_score_and_finish(self):
        """Guardar la puntuación en la base de datos usando el nombre ingresado"""
        name = self.game_over_name.strip() or "Player"
        try:
            # Intentar obtener jugador; si no existe, crearlo
            existing = self.db.get_player(name)
            if existing:
                player_id = existing.get("id")
            else:
                player_id = self.db.create_player(name)

            # Guardar puntuación (ajustar los campos según tu esquema)
            self.db.save_score(player_id=player_id,
                               score=self.score,
                               level=self.level,
                               time=int(self.play_time),
                               stars=self.stars_collected,
                               max_combo=self.max_combo)
        except Exception:
            # Si hay error con la BD, no rompemos el juego; al menos salir al menú
            pass

        # Desactivar entrada de texto y volver al menú principal
        self.game_over_input_active = False
        pygame.key.stop_text_input()
        from .start_menu import StartMenuScene
        self.game.set_scene(StartMenuScene(self.game))

    def update(self, dt):
        """Actualizar lógica del juego"""
        if not self.paused:
            self.play_time += dt
            self.player.update(dt)
            # ejemplo: si la vida llega a 0, terminar la partida
            if self.player.health <= 0 and not self.game_over:
                self.trigger_game_over()

    def render(self, screen):
        """Dibujar elementos del juego"""
        screen.fill(self.BLACK)
        # Dibujar jugador
        self.player.render(screen)
        # Dibujar HUD simple
        self.draw_text(screen, f"Score: {self.score}", self.font_small, self.WHITE, 10, 10, center=False)
        self.draw_text(screen, f"Health: {self.player.health}", self.font_small, self.WHITE, 10, 34, center=False)

        # Si estamos en Game Over, dibujar overlay con entrada de nombre
        if self.game_over:
            # Fondo semitransparente
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0,0))

            # Caja central
            pygame.draw.rect(screen, (40,40,40), self.game_over_rect)
            pygame.draw.rect(screen, self.WHITE, self.game_over_rect, 2)

            # Texto Game Over y score
            self.draw_text(screen, "GAME OVER", self.font_large, self.RED, self.screen.get_width()//2, self.game_over_rect.y + 30, centered=True)
            self.draw_text(screen, f"Score: {self.score}", self.font_medium, self.WHITE, self.screen.get_width()//2, self.game_over_rect.y + 60, centered=True)

            # Input para nombre
            pygame.draw.rect(screen, (30,30,30), self.name_input_rect)
            pygame.draw.rect(screen, self.WHITE, self.name_input_rect, 2)
            name_display = self.game_over_name if self.game_over_name else "Enter name to save..."
            self.draw_text(screen, name_display, self.font_small, self.WHITE, self.name_input_rect.x + 8, self.name_input_rect.y + 6, centered=False)

            # Botón guardar (haga click o ENTER)
            save_rect = pygame.Rect(self.game_over_rect.x + 120, self.game_over_rect.y + 120, 160, 36)
            pygame.draw.rect(screen, self.GRAY, save_rect)
            pygame.draw.rect(screen, self.WHITE, save_rect, 2)
            self.draw_text(screen, "Save & Menu", self.font_small, self.WHITE, save_rect.x + save_rect.width//2, save_rect.y + save_rect.height//2, centered=True)

            # Manejo de click en botón guardar (se procesa aquí en render para simplicidad)
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                mx, my = pygame.mouse.get_pos()
                if save_rect.collidepoint((mx, my)):
                    # Pequeña espera para evitar múltiples triggers por mantener click
                    pygame.time.wait(120)
                    self._save_score_and_finish()
