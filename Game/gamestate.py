from enum import Enum

class GameStatus(Enum):
    """
    Enumeration for different game states.
    """
    PLAYING = "Playing"
    WON = "Victory"
    LOST = "Game Over: Loss"

class GameState:
    """
    Manages the overall state of the Minesweeper game including game status,
    timing, and game statistics.
    """
    
    def __init__(self, mine_count=10):
        """
        Initialize a new game state.
        
        Inputs: mine_count (int) - Number of mines in the game (default 10)
        Outputs: None (constructor)
        """
        # Original implementation - game state tracking
        self.status = GameStatus.PLAYING
        self.mine_count = mine_count
        
        # Game statistics
        self.cells_revealed = 0
        self.flags_placed = 0
        self.first_click_made = False
    
    def start_game(self):
        """
        Start the game and set initial state.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation
        self.status = GameStatus.PLAYING
        self.first_click_made = False
    
    def end_game(self, won=False):
        """
        End the game and record final state.
        
        Inputs: won (bool) - True if player won, False if lost
        Outputs: None
        """
        # Original implementation
        self.status = GameStatus.WON if won else GameStatus.LOST
    
    def is_game_active(self):
        """
        Check if the game is currently active (being played).
        
        Inputs: None
        Outputs: bool - True if game is active, False if won or lost
        """
        # Original implementation
        return self.status == GameStatus.PLAYING
    
    def get_status_text(self):
        """
        Get the current game status as a text string.
        
        Inputs: None
        Outputs: str - Current game status
        """
        # Original implementation
        return self.status.value
    
    def update_statistics(self, cells_revealed, flags_placed):
        """
        Update game statistics.
        
        Inputs: cells_revealed (int) - Number of cells currently revealed
                flags_placed (int) - Number of flags currently placed
        Outputs: None
        """
        # Original implementation
        self.cells_revealed = cells_revealed
        self.flags_placed = flags_placed
    
    def get_remaining_mines(self):
        """
        Get the number of mines remaining to be flagged.
        
        Inputs: None
        Outputs: int - Number of mines minus flags placed
        """
        # Original implementation
        return self.mine_count - self.flags_placed
    
    def mark_first_click(self):
        """
        Mark that the first click has been made.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation
        self.first_click_made = True
    
    def reset(self, mine_count=None):
        """
        Reset the game state for a new game.
        
        Inputs: mine_count (int, optional) - New mine count, uses current if None
        Outputs: None
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
        Get comprehensive game information as a dictionary.
        
        Inputs: None
        Outputs: dict - Game information including status and statistics
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
        String representation of the game state for debugging.
        
        Inputs: None
        Outputs: str - String representation
        """
        # Original implementation for debugging
        info = self.get_game_info()
        return (f"GameState(status={info['status']}, "
                f"mines={info['mine_count']}, remaining={info['remaining_mines']}, "
                f"revealed={info['cells_revealed']}, flags={info['flags_placed']})")