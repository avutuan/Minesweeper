# minesweeper.py
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ROWS, COLS, NUM_MINES
from core.classes.board import Board
from core.classes.game_state import GameState
from input_output.renderer import Renderer
from input_output.input_controller import InputController
from core.enums.game_state_enum import GameStateEnum
from core.enums.cell_state_enum import CellState

class Game:
    """Orchestrates the game, connecting all components."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.input_controller = InputController()
        self._setup_game()

    def _setup_game(self):
        """Initializes or resets the game state for a new game."""
        self.board = Board(ROWS, COLS, NUM_MINES)
        self.game_state = GameState(NUM_MINES)

    def run(self):
        """The main game loop."""
        running = True
        while running:
            # 1. Interpret Input
            intent = self.input_controller.handle_input()

            if intent:
                if intent["action"] == "QUIT":
                    running = False
                    continue
                if intent["action"] == "RESTART":
                    self._setup_game()
                    continue

                # Game logic only processes if the game is active
                if self.game_state.state in [GameStateEnum.READY, GameStateEnum.RUNNING]:
                    self._process_intent(intent)

            # 2. Update State
            self.game_state.update_timer()

            # 3. Render
            self.renderer.draw(self.board, self.game_state)
            pygame.display.flip()

            self.clock.tick(30) # Limit frame rate

        pygame.quit()
        sys.exit()

    def _process_intent(self, intent):
        """Applies core logic based on user intent."""
        action = intent.get("action")
        pos = intent.get("pos")

        # Handle first move (deferred mine placement)
        if action == "REVEAL" and self.game_state.state == GameStateEnum.READY:
            self.game_state.state = GameStateEnum.RUNNING
            self.board.place_mines(pos[0], pos[1])
            self.game_state.start_timer()

        # Handle subsequent moves
        if action == "REVEAL":
            cell = self.board.grid[pos[0]][pos[1]]
            if cell.state == CellState.HIDDEN:
                self.board.reveal(pos[0], pos[1])
                # Check for loss condition
                if cell.has_mine:
                    self.game_state.lose()
        
        elif action == "FLAG":
            cell = self.board.grid[pos[0]][pos[1]]
            # Only allow flagging if flags are available
            if cell.state == CellState.HIDDEN and self.game_state.flags_left > 0:
                self.board.toggle_flag(pos[0], pos[1])
                self.game_state.flags_left -= 1
            elif cell.state == CellState.FLAGGED:
                
                self.board.toggle_flag(pos[0], pos[1])
                self.game_state.flags_left += 1

        # Check for win condition after any move that could cause it
        if self.game_state.state == GameStateEnum.RUNNING and self.board.is_cleared():
            self.game_state.win()

if __name__ == '__main__':
    game = Game()
    game.run()