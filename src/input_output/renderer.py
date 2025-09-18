from config import SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT, CELL_SIZE, COLOR_BG, COLOR_HIDDEN, COLOR_REVEALED, COLOR_BORDER_LIGHT, COLOR_BORDER_DARK, COLOR_TEXT, COLOR_MINE, COLOR_OVERLAY_LOSS, COLOR_OVERLAY_WIN, NUMBER_COLORS
import pygame
from core.enums.game_state_enum import GameStateEnum
from core.enums.cell_state_enum import CellState

class Renderer:
    """Converts the core state into pixels on the screen."""
    def __init__(self, screen):
        self.screen = screen
        self.font_cell = pygame.font.SysFont('Arial', CELL_SIZE // 2, bold=True)
        self.font_hud = pygame.font.SysFont('Arial', HEADER_HEIGHT // 2, bold=True)
        self.font_game_over = pygame.font.SysFont('Arial', HEADER_HEIGHT, bold=True)

    def _draw_beveled_rect(self, rect, depth=3):
        """Draws a rectangle with a 3D beveled edge."""
        pygame.draw.rect(self.screen, COLOR_BORDER_LIGHT, rect, depth, border_top_left_radius=3)
        pygame.draw.rect(self.screen, COLOR_BORDER_DARK, (rect.x, rect.y, rect.width + depth, rect.height + depth), depth, border_bottom_right_radius=3)

    def draw(self, board, game_state):
        """Main draw call for the entire game."""
        self.screen.fill(COLOR_BG)
        self.draw_board(board, game_state)
        self.draw_hud(game_state)
        if game_state.state in [GameStateEnum.WON, GameStateEnum.LOST]:
            self.draw_game_over(game_state)

    def draw_board(self, board, game_state):
        for r in range(board.rows):
            for c in range(board.cols):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE + HEADER_HEIGHT, CELL_SIZE, CELL_SIZE)
                cell = board.grid[r][c]

                if cell.state == CellState.REVEALED:
                    pygame.draw.rect(self.screen, COLOR_REVEALED, rect)
                    pygame.draw.rect(self.screen, COLOR_BORDER_DARK, rect, 1) # Sunken border
                    if cell.has_mine:
                        pygame.draw.circle(self.screen, COLOR_MINE, rect.center, CELL_SIZE // 3)
                    elif cell.adjacent_count > 0:
                        text_surf = self.font_cell.render(str(cell.adjacent_count), True, NUMBER_COLORS[cell.adjacent_count])
                        text_rect = text_surf.get_rect(center=rect.center)
                        self.screen.blit(text_surf, text_rect)
                else: # Hidden or Flagged
                    self._draw_beveled_rect(rect)
                    pygame.draw.rect(self.screen, COLOR_HIDDEN, (rect.x+3, rect.y+3, rect.width-6, rect.height-6))
                    if cell.state == CellState.FLAGGED:
                        text_surf = self.font_cell.render("•", True, COLOR_TEXT)
                        text_rect = text_surf.get_rect(center=rect.center)
                        self.screen.blit(text_surf, text_rect)
                    # Show incorrect flags and remaining mines on game over
                    if game_state.state == GameStateEnum.LOST and cell.has_mine and cell.state != CellState.FLAGGED:
                         pygame.draw.circle(self.screen, COLOR_TEXT, rect.center, CELL_SIZE // 4)

    def draw_hud(self, game_state):
        flags_text = self.font_hud.render(f"• {game_state.flags_left}", True, COLOR_TEXT)
        self.screen.blit(flags_text, (10, 10))

        timer_text = self.font_hud.render(f"⏱️ {game_state.elapsed_time}", True, COLOR_TEXT)
        timer_rect = timer_text.get_rect(right=SCREEN_WIDTH - 10, top=10)
        self.screen.blit(timer_text, timer_rect)

    def draw_game_over(self, game_state):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - HEADER_HEIGHT), pygame.SRCALPHA)
        if game_state.state == GameStateEnum.WON:
            overlay.fill(COLOR_OVERLAY_WIN)
            text = "YOU WON!"
        else: # LOST
            overlay.fill(COLOR_OVERLAY_LOSS)
            text = "YOU LOST!"

        self.screen.blit(overlay, (0, HEADER_HEIGHT))
        game_over_surf = self.font_game_over.render(text, True, COLOR_TEXT)
        game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + HEADER_HEIGHT / 2))
        self.screen.blit(game_over_surf, game_over_rect)