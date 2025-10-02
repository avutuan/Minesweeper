
"""
Module: minesweeper.py
Description: Main entry point and game loop for the Minesweeper application. Handles initialization, event loop, and coordination between core logic, input, and rendering.
Author: Changwen Gong
Creation Date: September 17, 2025
External Sources: N/A - Original Code
"""

import pygame
import sys
from core.board import Board
from core.gamestate import GameState
from input_output.input_controller import InputController
from input_output.renderer import Renderer

class MinesweeperGame:
    """
    Description: Main Minesweeper game class using Pygame for graphical interface. Coordinates user interface, input processing, and game loop between Board and GameState classes.
    Author: Changwen Gong
    Creation Date: September 17, 2025
    External Sources: N/A - Original Code
    """
    
    def __init__(self):
        """
        Description: Initialize the Minesweeper game with Pygame and default settings.
        Args: None
        Returns: None
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Initialize Pygame and set up game constants.
        
        pygame.init()

        # Set up game constants for grid and UI layout.
        self.CELL_SIZE = 40
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 10
        self.INFO_HEIGHT = 80

        # Calculate window dimensions based on grid and info panel.
        self.WINDOW_WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.WINDOW_HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE + self.INFO_HEIGHT

        # Track game state for start/end screens.
        self.show_end_screen = False
        self.show_start_screen = True

        # Define color scheme for UI elements and cells.
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
        self.mode = "classic" # classic, easy, medium, hard
        self.board = None
        self.game_state = None
        self.delayed_events = []
        
        # Initialize I/O controllers
        self.input_controller = InputController(self)
        self.renderer = Renderer(self)
        # Don't start game immediately - show start screen first
    
    def _start_new_game(self, mode):
        """
        Description: Start a new game by resetting board and game state.
        Args: None
        Returns: None
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Reset board and game state for a new session.
        
        self.board = Board(self.mine_count)
        self.game_state = GameState(self.mine_count, mode, self)
        self.show_end_screen = False
        self.show_start_screen = False
    
    def _update_game_statistics(self):
        """
        Description: Update game state with current board statistics (revealed cells, flags placed).
        Args: None
        Returns: None
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Update statistics in GameState from Board state.
        self.game_state.update_statistics(
            self.board.revealed_cells,
            self.board.get_flag_count()
        )
    
    def _handle_events(self):
        """
        Description: Handle all Pygame events by delegating to the InputController.
        Args: None
        Returns: bool - True to continue game loop, False to quit
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Delegate event handling to InputController.
        return self.input_controller.handle_events()
    
    def delay_event(self, delay, callback, update):
        self.delayed_events.append({"time": 0, "delay": delay, "callback": callback, "update": update})
    
    def _update(self, delta_time):
        for i in range(len(self.delayed_events)-1, -1, -1):
            event = self.delayed_events[i]
            event["time"] += delta_time
            event["update"](event["time"])
            if event["time"] > event["delay"]:
                event["callback"]()
                del self.delayed_events[i]
    
    def run(self):
        """
        Description: Main game loop - runs until player quits. Handles event processing, rendering, and frame rate control.
        Args: None
        Returns: None
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Print game instructions to console for user reference.
        running = True
        print("Minesweeper Game Started!")
        print("Controls:")
        print("- Left click: Reveal cell")
        print("- Right click: Toggle flag")
        print("- SPACE or 1 key: Start new game")
        print("- 2 key: Start new game VS. AI (Easy)")
        print("- 3 key: Start new game VS. AI (Medium)")
        print("- 4 key: Start new game VS. AI (Hard)")
        print("- R key: Reset game (during play)")
        print("- UP/DOWN arrows: Adjust mine count (10-20)")
        print("- +/- keys: Also adjust mine count")
        print("- ESC: Quit game")

        # Main event loop for game execution.
        while running:
            # Control frame rate for smooth gameplay.
            delta_time = self.clock.tick(60) / 1000.0
            
            # Update animations
            self._update(delta_time)

            # Handle events from user input and system.
            running = self._handle_events()

            # Draw game using renderer to update UI.
            self.renderer.draw_game()

        # Clean up and exit Pygame when game ends.
        
        pygame.quit()
        sys.exit()

def main():
    """
    Description: Main function to start the Minesweeper game. Handles instantiation and error handling.
    Args: None
    Returns: None
    Author: Changwen Gong
    Creation Date: September 17, 2025
    External Sources: N/A - Original Code
    """
    # Entry point for launching the game application.
    try:
        game = MinesweeperGame()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    # Run the main function if this script is executed directly.
    main()