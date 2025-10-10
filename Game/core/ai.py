"""
Module: ai.py
Description: Implements AI logic for Minesweeper gameplay with multiple difficulty levels (easy, medium, hard).
Author: Alejandro Sandoval
Creation Date: October 3, 2025
External Sources: N/A - Original Code
"""
import random

class AI():
    def __init__(self, mode, board, game):
        """
        Description: AI logic
        Args: None
        Returns: None
        Author: Alejandro Sandoval
        Creation Date: October 3, 2025
        External Sources: N/A - Original Code
        """
        self.ai_mode = mode
        self.board = board
        self.game = game

    def move(self):
        """
        Description: AI logic for uncovering cells for the three difficulties
        Args: None
        Returns: None
        Author: Alejandro Sandoval
        Creation Date: October 3, 2025
        External Sources: N/A - Original Code
        """
        if self.ai_mode == "medium" or self.ai_mode == "hard":
            # flagging and revealing based on numbers
            for row in range(self.game.board.ROWS):
                for col in range(self.game.board.COLS):
                    cell = self.game.board.get_cell(row, col)
                    if cell.is_revealed and cell.adjacent_mines > 0:
                        neighbors = self.game.board.get_hidden_neighbors(row, col)
                        flagged_neighbors = [n for n in neighbors if n.is_flagged]
                        unflagged_neighbors = [n for n in neighbors if not n.is_flagged]
                        
                        # if the number of hidden neighbors of a revealed cell equals that cell’s number, the AI should flag all hidden neighbors.
                        if len(neighbors) == cell.adjacent_mines and unflagged_neighbors and self.game.game_state.flags_left > 0:
                            for neighbor in neighbors:
                                if self.game.game_state.flags_left > 0:
                                    self.game.board.toggle_flag(neighbor.row, neighbor.col)
                        # if the number of flagged neighbors of a revealed cell equals that cell’s number, the AI should open all other hidden neighbors
                        if len(flagged_neighbors) == cell.adjacent_mines and unflagged_neighbors:
                            neighbor = unflagged_neighbors[random.randint(0, len(unflagged_neighbors)-1)]
                            mine_hit = self.game.board.reveal_cell(neighbor.row, neighbor.col)
                            if mine_hit:
                                return "loss"
                            return
        if self.ai_mode == "hard":
            # 1-2-1 pattern
            # Horizontal
            for row in range(self.game.board.ROWS):
                for col in range(self.game.board.COLS - 2):
                    cell1 = self.game.board.get_cell(row, col)
                    cell2 = self.game.board.get_cell(row, col + 1)
                    cell3 = self.game.board.get_cell(row, col + 2)
                    
                    if (cell1.is_revealed and cell1.adjacent_mines == 1 and
                        cell2.is_revealed and cell2.adjacent_mines == 2 and
                        cell3.is_revealed and cell3.adjacent_mines == 1):
                        for i in range(-1, 2, 2): # above and below
                            if 0 <= row+i < self.game.board.ROWS:
                                cell1s = self.game.board.get_cell(row+i, col)
                                cell2s = self.game.board.get_cell(row+i, col + 1)
                                cell3s = self.game.board.get_cell(row+1, col + 2)
                                # Flag mines
                                if not cell1s.is_revealed and self.game.game_state.flags_left > 0:
                                    self.game.board.toggle_flag(cell1s.row, cell1s.col)
                                if not cell3s.is_revealed and self.game.game_state.flags_left > 0:
                                    self.game.board.toggle_flag(cell3s.row, cell3s.col)
                                # Uncover safe space.
                                if cell2s and not cell2s.is_revealed:
                                    mine_hit = self.game.board.reveal_cell(cell2s.row, cell2s.col)
                                    if mine_hit:
                                        return "loss"
                                    return
            # Vertical
            for row in range(self.game.board.ROWS - 2):
                for col in range(self.game.board.COLS):
                    cell1 = self.game.board.get_cell(row, col)
                    cell2 = self.game.board.get_cell(row + 1, col)
                    cell3 = self.game.board.get_cell(row + 2, col)
                    
                    if (cell1.is_revealed and cell1.adjacent_mines == 1 and
                        cell2.is_revealed and cell2.adjacent_mines == 2 and
                        cell3.is_revealed and cell3.adjacent_mines == 1):
                        for i in range(-1, 2, 2): # left and right
                            if 0 <= col+i < self.game.board.COLS:
                                cell1s = self.game.board.get_cell(row, col + i)
                                cell2s = self.game.board.get_cell(row + 1, col + i)
                                cell3s = self.game.board.get_cell(row + 2, col + i)
                                # Flag mines
                                if not cell1s.is_revealed and self.game.game_state.flags_left > 0:
                                    self.game.board.toggle_flag(cell1s.row, cell1s.col)
                                if not cell3s.is_revealed and self.game.game_state.flags_left > 0:
                                    self.game.board.toggle_flag(cell3s.row, cell3s.col)
                                # Uncover safe space.
                                if cell2s and not cell2s.is_revealed:
                                    mine_hit = self.game.board.reveal_cell(cell2s.row, cell2s.col)
                                    if mine_hit:
                                        return "loss"
                                    return

            # Random safe click
            covered_cells = self.game.board.get_covered_cells()
            no_mine_cells = [n for n in neighbors if n.is_mine]
            if no_mine_cells:
                cell = no_mine_cells[random.randint(0, len(no_mine_cells)-1)]
                self.game.board.reveal_cell(cell.row, cell.col)
                return
        
        # pick random cell
        covered_cells = self.game.board.get_covered_cells()
        cell = covered_cells[random.randint(0, len(covered_cells)-1)]
        mine_hit = self.game.board.reveal_cell(cell.row, cell.col)
        if mine_hit:
            return "loss"