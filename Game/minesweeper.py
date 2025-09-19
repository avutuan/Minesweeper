import pygame
import sys
from core.board import Board
from core.gamestate import GameState
from input_output.input_controller import InputController
from input_output.renderer import Renderer

class MinesweeperGame:
    """
    Main Minesweeper game class using Pygame for graphical interface.
    
    Handles user interface, input processing, and game loop coordination
    between Board and GameState classes.
    """
    
    def __init__(self):
        """
        Initialize the Minesweeper game with Pygame and default settings.
        
        Inputs: None
        Outputs: None (constructor)
        """
        # Original implementation - Pygame initialization
        pygame.init()
        
        # Game constants
        self.CELL_SIZE = 40
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 10
        self.INFO_HEIGHT = 80
        
        # Window dimensions
        self.WINDOW_WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.WINDOW_HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE + self.INFO_HEIGHT
        
        # Game state
        self.show_end_screen = False
        self.show_start_screen = True
        
        # Colors (original color scheme)
        self.COLORS = {
            'background': (192, 192, 192),
            'cell_covered': (160, 160, 160),
            'cell_revealed': (224, 224, 224),
            'cell_mine': (255, 0, 0),
            'cell_flag': (255, 255, 0),
            'border': (128, 128, 128),
            'text': (0, 0, 0),
            'number_colors': {
                1: (0, 0, 255),
                2: (0, 128, 0),
                3: (255, 0, 0),
                4: (0, 0, 128),
                5: (128, 0, 0),
                6: (0, 128, 128),
                7: (0, 0, 0),
                8: (128, 128, 128)
            }
        }
        
        # Initialize Pygame components
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Minesweeper - EECS 581 Project 1")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Initialize game components
        self.mine_count = 10  # Default mine count
        self.board = None
        self.game_state = None
        
        # Initialize I/O controllers
        self.input_controller = InputController(self)
        self.renderer = Renderer(self)
        # Don't start game immediately - show start screen first
    
    def _start_new_game(self):
        """
        Start a new game by resetting board and game state.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - game initialization
        self.board = Board(self.mine_count)
        self.game_state = GameState(self.mine_count)
        self.show_end_screen = False
        self.show_start_screen = False
    
    def _update_game_statistics(self):
        """
        Update game state with current board statistics.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - statistics update
        self.game_state.update_statistics(
            self.board.revealed_cells,
            self.board.get_flag_count()
        )
    
    def _handle_events(self):
        """
        Handle all Pygame events by delegating to the InputController.
        
        Inputs: None
        Outputs: bool - True to continue game loop, False to quit
        """
        return self.input_controller.handle_events()
    
    def run(self):
        """
        Main game loop - runs until player quits.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - main game loop
        running = True
        
        print("Minesweeper Game Started!")
        print("Controls:")
        print("- Left click: Reveal cell")
        print("- Right click: Toggle flag")
        print("- SPACE: Start new game")
        print("- R key: Reset game (during play)")
        print("- UP/DOWN arrows: Adjust mine count (10-20)")
        print("- +/- keys: Also adjust mine count")
        print("- ESC: Quit game")
        
        while running:
            # Handle events
            running = self._handle_events()
            
            # Draw game using renderer
            self.renderer.draw_game()
            
            # Control frame rate
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    """
    Main function to start the Minesweeper game.
    
    Inputs: None
    Outputs: None
    """
    # Original implementation - application entry point
    try:
        game = MinesweeperGame()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()