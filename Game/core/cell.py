"""
Module: cell.py
Description: Represents a single cell in the Minesweeper grid, managing mine, flag, reveal state, and adjacent mine count.
Author: Kevinh Nguyen
Creation Date: September 14, 2025
External Sources: N/A - Original Code
"""
class Cell:
    """
    Description: Represents a single cell in the Minesweeper grid, managing mine, flag, reveal state, and adjacent mine count.
    Author: Kevinh Nguyen
    Creation Date: September 14, 2025
    External Sources: N/A - Original Code
    """
    
    def __init__(self):
        """
        Description: Initialize a new cell with default values (no mine, not revealed, not flagged, 0 adjacent mines).
        Args: None
        Returns: None
        Author: Kevinh Nguyen
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - cell state tracking
        self.is_mine = False          # True if this cell contains a mine
        self.is_revealed = False      # True if this cell has been uncovered
        self.is_flagged = False       # True if this cell has been flagged by player
        self.adjacent_mines = 0       # Count of mines in adjacent cells (0-8)
    
    def set_mine(self):
        """
        Description: Mark this cell as containing a mine.
        Args: None
        Returns: None
        Author: Kevinh Nguyen
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        self.is_mine = True
    
    def reveal(self):
        """
        Description: Reveal this cell (uncover it). Cannot reveal if flagged.
        Args: None
        Returns: bool - True if cell was successfully revealed, False if flagged
        Author: Kevinh Nguyen
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - cannot reveal flagged cells
        if self.is_flagged:
            return False
        self.is_revealed = True
        return True
    
    def toggle_flag(self):
        """
        Description: Toggle the flag state of this cell. Cannot flag if already revealed.
        Args: None
        Returns: bool - True if cell was successfully flagged/unflagged, False if already revealed
        Author: Kevinh Nguyen
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - cannot flag revealed cells
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        return True
    
    def set_adjacent_mines(self, count):
        """
        Description: Set the number of adjacent mines for this cell.
        Args:
            count (int): Number of adjacent mines (0-8)
        Returns: None
        Author: Kevinh Nguyen
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation with bounds checking
        if 0 <= count <= 8:
            self.adjacent_mines = count
    
    def get_display_value(self):
        """
        Description: Get the display value for this cell based on its current state (flag, mine, number, or covered).
        Args: None
        Returns: str - Character to display for this cell
        Author: Kevinh Nguyen
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
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
        Description: String representation of the cell for debugging.
        Args: None
        Returns: str - String representation
        Author: Kevinh Nguyen
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
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