import pygame
from core.enums.game_state_enum import GameStateEnum

class GameState:
    """Tracks game status, timer, and flag count."""
    def __init__(self, num_mines):
        self.state = GameStateEnum.READY
        self.flags_left = num_mines
        self.start_time = 0
        self.elapsed_time = 0

    def start_timer(self):
        self.start_time = pygame.time.get_ticks()

    def update_timer(self):
        if self.state == GameStateEnum.RUNNING:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def win(self):
        self.state = GameStateEnum.WON

    def lose(self):
        self.state = GameStateEnum.LOST