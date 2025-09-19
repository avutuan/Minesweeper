import random
from core.cell import Cell

class Board:
    """
    Manages the Minesweeper game board including mine placement, cell management,
    and game logic for revealing cells and checking win conditions.
    """
    
    def __init__(self, mine_count=10):
        """
        Initialize a new 10x10 Minesweeper board.
        
        Inputs: mine_count (int) - Number of mines to place (10-20, default 10)
        Outputs: None (constructor)
        """
        # Original implementation - board configuration
        self.ROWS = 10
        self.COLS = 10
        self.mine_count = max(10, min(20, mine_count))  # Ensure mine count is between 10-20
        self.first_click = True  # Track if this is the first click
        
        # Initialize 2D grid of Cell objects
        self.grid = [[Cell() for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        # Track game statistics
        self.revealed_cells = 0
        self.total_safe_cells = self.ROWS * self.COLS - self.mine_count
    
    def place_mines(self, safe_row, safe_col):
        """
        Randomly place mines on the board, avoiding the first clicked cell and its neighbors.
        
        Inputs: safe_row (int) - Row of first clicked cell (0-9)
                safe_col (int) - Column of first clicked cell (0-9)
        Outputs: None
        """
        # Original implementation - random mine placement with safe zone
        # Create list of safe cells (first clicked cell and all adjacent cells)
        safe_cells = set()
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = safe_row + dr, safe_col + dc
                if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLS:
                    safe_cells.add((new_row, new_col))
        
        mines_placed = 0
        while mines_placed < self.mine_count:
            row = random.randint(0, self.ROWS - 1)
            col = random.randint(0, self.COLS - 1)
            
            # Avoid placing mine in safe zone or if cell already has mine
            if (row, col) in safe_cells or self.grid[row][col].is_mine:
                continue
            
            self.grid[row][col].set_mine()
            mines_placed += 1
        
        # Calculate adjacent mine counts for all cells
        self._calculate_adjacent_mines()
    
    def _calculate_adjacent_mines(self):
        """
        Calculate the number of adjacent mines for each cell.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - adjacent mine calculation
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if not self.grid[row][col].is_mine:
                    count = self._count_adjacent_mines(row, col)
                    self.grid[row][col].set_adjacent_mines(count)
    
    def _count_adjacent_mines(self, row, col):
        """
        Count mines in the 8 cells adjacent to the given position.
        
        Inputs: row (int) - Row position (0-9)
                col (int) - Column position (0-9)
        Outputs: int - Number of adjacent mines (0-8)
        """
        # Original implementation - count mines in 3x3 grid around cell
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:  # Skip the cell itself
                    continue
                
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.ROWS and 
                    0 <= new_col < self.COLS and 
                    self.grid[new_row][new_col].is_mine):
                    count += 1
        
        return count
    
    def reveal_cell(self, row, col):
        """
        Reveal a cell and potentially trigger recursive revealing.
        
        Inputs: row (int) - Row position (0-9)
                col (int) - Column position (0-9)
        Outputs: bool - True if mine was hit (game over), False otherwise
        """
        # Original implementation - cell revealing logic
        if not (0 <= row < self.ROWS and 0 <= col < self.COLS):
            return False
        
        cell = self.grid[row][col]
        
        # Handle first click - place mines after first click to ensure safety
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
        
        # Cannot reveal flagged or already revealed cells
        if cell.is_flagged or cell.is_revealed:
            return False
        
        # Reveal the cell
        cell.reveal()
        self.revealed_cells += 1
        
        # Check if mine was hit
        if cell.is_mine:
            return True  # Game over
        
        # If cell has no adjacent mines, recursively reveal adjacent cells
        if cell.adjacent_mines == 0:
            self._reveal_adjacent_cells(row, col)
        
        return False  # Safe cell revealed
    
    def _reveal_adjacent_cells(self, row, col):
        """
        Recursively reveal adjacent cells when a cell with 0 adjacent mines is revealed.
        
        Inputs: row (int) - Row position of cell with 0 adjacent mines
                col (int) - Column position of cell with 0 adjacent mines
        Outputs: None
        """
        # Original implementation - recursive revealing
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:  # Skip the cell itself
                    continue
                
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.ROWS and 
                    0 <= new_col < self.COLS):
                    
                    adjacent_cell = self.grid[new_row][new_col]
                    if (not adjacent_cell.is_revealed and 
                        not adjacent_cell.is_flagged and 
                        not adjacent_cell.is_mine):
                        
                        adjacent_cell.reveal()
                        self.revealed_cells += 1
                        
                        # Continue recursion if this cell also has 0 adjacent mines
                        if adjacent_cell.adjacent_mines == 0:
                            self._reveal_adjacent_cells(new_row, new_col)
    
    def toggle_flag(self, row, col):
        """
        Toggle the flag state of a cell. Only allow flagging if not revealed. Unflagging always allowed.
        Inputs: row (int) - Row position (0-9)
                col (int) - Column position (0-9)
        Outputs: bool - True if flag was toggled, False otherwise
        """
        if not (0 <= row < self.ROWS and 0 <= col < self.COLS):
            return False
        cell = self.grid[row][col]
        if cell.is_revealed:
            return False
        # Toggle flag
        cell.is_flagged = not cell.is_flagged
        return True
    
    def get_flag_count(self):
        """
        Count the number of flags currently placed on the board.
        
        Inputs: None
        Outputs: int - Number of flags placed
        """
        # Original implementation - count flags
        count = 0
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col].is_flagged:
                    count += 1
        return count
    
    def get_remaining_mines(self):
        """
        Get the number of remaining mines (total mines minus flags placed).
        
        Inputs: None
        Outputs: int - Number of remaining mines to flag
        """
        # Original implementation
        return self.mine_count - self.get_flag_count()
    
    def is_game_won(self):
        """
        Check if the game has been won (all non-mine cells revealed).
        Inputs: None
        Outputs: bool - True if game is won, False otherwise
        """
        # Win if all non-mine cells are revealed
        return self.revealed_cells == self.total_safe_cells
    
    def reveal_all_mines(self):
        """
        Reveal all mines on the board (called when game is lost).
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - reveal mines on game over
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col].is_mine:
                    self.grid[row][col].is_revealed = True
    
    def get_cell(self, row, col):
        """
        Get the cell at the specified position.
        
        Inputs: row (int) - Row position (0-9)
                col (int) - Column position (0-9)
        Outputs: Cell object or None if position is invalid
        """
        # Original implementation
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return self.grid[row][col]
        return None
    
    def get_board_state(self):
        """
        Get a string representation of the current board state for debugging.
        
        Inputs: None
        Outputs: str - String representation of the board
        """
        # Original implementation for debugging
        result = "  A B C D E F G H I J\n"
        for row in range(self.ROWS):
            result += f"{row + 1:2} "
            for col in range(self.COLS):
                result += self.grid[row][col].get_display_value() + " "
            result += "\n"
        return result