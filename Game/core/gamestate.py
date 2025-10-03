"""
Module: gamestate.py
Description: Manages the overall state of the Minesweeper game, including game status, timing, and statistics.
Author: Tuan Vu
Creation Date: September 19, 2025
External Sources: N/A - Original Code
"""
from enum import Enum
import random

class GameStatus(Enum):
    """
    Description: Enumeration for different game states (Playing, Won, Lost).
    Author: Tuan Vu
    Creation Date: September 19, 2025
    External Sources: N/A - Original Code
    """
    PLAYING = "Playing"
    WON = "Victory"
    LOST = "Game Over: Loss"

class GameState:
    """
    Description: Manages the overall state of the Minesweeper game including game status, timing, and game statistics.
    Author: Tuan Vu
    Creation Date: September 19, 2025
    External Sources: N/A - Original Code
    """
    
    def __init__(self, mine_count=10, mode="classic", game=None):
        """
        Description: Initialize a new game state with mine count and default statistics.
        Args:
            mine_count (int): Number of mines in the game (default 10)
        Returns: None
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - game state tracking
        self.status = GameStatus.PLAYING
        self.mine_count = mine_count
        self.game = game
        # Game statistics
        self.cells_revealed = 0
        self.flags_placed = 0
        self.first_click_made = False
        self.flags_left = mine_count  # Track remaining flags

        self.turn = 0
        self.players = ["You"]
        self.current_player = self.players[self.turn]

        self.ai_mode = "easy"
        self.ai_thinking_timer = 0
        if mode == "easy" or mode == "medium" or mode == "hard":
            self.ai_mode = mode
            self.players.append("AI")

    def next_turn(self):
        self.turn = (self.turn+1)%len(self.players)
        self.current_player = self.players[self.turn]
        if self.current_player == "AI":
            delay = 2
            self.game.delay_event(delay, lambda: self.ai_move(), lambda time: self.ai_update(time, delay))

    def ai_move(self):
        if self.ai_mode == "easy":
            row = random.randint(0, self.game.board.ROWS-1)
            col = random.randint(0, self.game.board.COLS-1)

            mine_hit = self.game.board.reveal_cell(row, col)
            if mine_hit and hasattr(self.game, "play_mine_hit_sound"):
                self.game.play_mine_hit_sound()
        elif self.ai_mode == "medium":
            pass
        elif self.ai_mode == "hard":
            pass
        self.ai_thinking_timer = 0
        self.next_turn()

    def ai_update(self, time, delay):
        self.ai_thinking_timer = time/delay
    
    def start_game(self):
        """
        Description: Start the game and set initial state.
        Args: None
        Returns: None
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        self.status = GameStatus.PLAYING
        self.first_click_made = False
    
    def end_game(self, won=False):
        """
        Description: End the game and record final state (win/loss).
        Args:
            won (bool): True if player won, False if lost
        Returns: None
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        self.status = GameStatus.WON if won else GameStatus.LOST
    
    def is_game_active(self):
        """
        Description: Check if the game is currently active (being played).
        Args: None
        Returns: bool - True if game is active, False if won or lost
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        return self.status == GameStatus.PLAYING
    
    def get_status_text(self):
        """
        Description: Get the current game status as a text string.
        Args: None
        Returns: str - Current game status
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        return self.status.value
    
    def update_statistics(self, cells_revealed, flags_placed):
        """
        Description: Update game statistics (revealed cells, flags placed).
        Args:
            cells_revealed (int): Number of cells currently revealed
            flags_placed (int): Number of flags currently placed
        Returns: None
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        self.cells_revealed = cells_revealed
        self.flags_placed = flags_placed
    
    def get_remaining_mines(self):
        """
        Description: Get the number of mines remaining to be flagged.
        Args: None
        Returns: int - Number of mines minus flags placed
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        return self.mine_count - self.flags_placed
    
    def mark_first_click(self):
        """
        Description: Mark that the first click has been made.
        Args: None
        Returns: None
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        self.first_click_made = True
    
    def reset(self, mine_count=None):
        """
        Description: Reset the game state for a new game.
        Args:
            mine_count (int, optional): New mine count, uses current if None
        Returns: None
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        if mine_count is not None:
            self.mine_count = mine_count
        
        self.status = GameStatus.PLAYING
        self.cells_revealed = 0
        self.flags_placed = 0
        self.first_click_made = False
    
    def get_game_info(self):
        """
        Description: Get comprehensive game information as a dictionary.
        Args: None
        Returns: dict - Game information including status and statistics
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        return {
            'status': self.get_status_text(),
            'mine_count': self.mine_count,
            'remaining_mines': self.get_remaining_mines(),
            'cells_revealed': self.cells_revealed,
            'flags_placed': self.flags_placed,
            'first_click_made': self.first_click_made,
            'is_active': self.is_game_active()
        }
    
    def __str__(self):
        """
        Description: String representation of the game state for debugging.
        Args: None
        Returns: str - String representation
        Author: Tuan Vu
        Creation Date: September 19, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation for debugging
        info = self.get_game_info()
        return (f"GameState(status={info['status']}, "
                f"mines={info['mine_count']}, remaining={info['remaining_mines']}, "
                f"revealed={info['cells_revealed']}, flags={info['flags_placed']})")
