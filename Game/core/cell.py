class Cell:
    """
    Represents a single cell in the Minesweeper grid.
    
    This class manages the state of an individual cell including whether it contains
    a mine, is flagged, is revealed, and how many adjacent mines it has.
    """
    
    def __init__(self):
        """
        Initialize a new cell with default values.
        
        Inputs: None
        Outputs: None (constructor)
        """
        # Original implementation - cell state tracking
        self.is_mine = False          # True if this cell contains a mine
        self.is_revealed = False      # True if this cell has been uncovered
        self.is_flagged = False       # True if this cell has been flagged by player
        self.adjacent_mines = 0       # Count of mines in adjacent cells (0-8)
    
    def set_mine(self):
        """
        Mark this cell as containing a mine.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation
        self.is_mine = True
    
    def reveal(self):
        """
        Reveal this cell (uncover it).
        
        Inputs: None
        Outputs: bool - True if cell was successfully revealed, False if flagged
        """
        # Original implementation - cannot reveal flagged cells
        if self.is_flagged:
            return False
        self.is_revealed = True
        return True
    
    def toggle_flag(self):
        """
        Toggle the flag state of this cell.
        
        Inputs: None
        Outputs: bool - True if cell was successfully flagged/unflagged, False if already revealed
        """
        # Original implementation - cannot flag revealed cells
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        return True
    
    def set_adjacent_mines(self, count):
        """
        Set the number of adjacent mines for this cell.
        
        Inputs: count (int) - Number of adjacent mines (0-8)
        Outputs: None
        """
        # Original implementation with bounds checking
        if 0 <= count <= 8:
            self.adjacent_mines = count
    
    def get_display_value(self):
        """
        Get the display value for this cell based on its current state.
        
        Inputs: None
        Outputs: str - Character to display for this cell
        """
        # Original implementation - display logic based on cell state
        if not self.is_revealed:
            if self.is_flagged:
                return 'F'  # Flagged cell
            else:
                return ' '  # Covered cell
        else:
            if self.is_mine:
                return '*'  # Revealed mine
            elif self.adjacent_mines == 0:
                return ' '  # Empty cell (no adjacent mines)
            else:
                return str(self.adjacent_mines)  # Number of adjacent mines
    
    def __str__(self):
        """
        String representation of the cell for debugging.
        
        Inputs: None
        Outputs: str - String representation
        """
        # Original implementation for debugging purposes
        state = []
        if self.is_mine:
            state.append("MINE")
        if self.is_revealed:
            state.append("REVEALED")
        if self.is_flagged:
            state.append("FLAGGED")
        state.append(f"ADJ:{self.adjacent_mines}")
        return f"Cell({', '.join(state)})"