"""
Module: input_controller.py
Description: Handles user input events and dispatches actions to the game logic (Board, GameState).
Author: Raj Kaura
Creation Date: September 18, 2025
External Sources: N/A - Original Code
"""
import pygame
import sys

class InputController:
    """
    Description: Handles all input events for the Minesweeper game. Processes mouse clicks, keyboard input, and coordinates game state changes based on user interactions.
    Author: Raj Kaura
    Creation Date: September 18, 2025
    External Sources: N/A - Original Code
    """
    
    def __init__(self, game):
        """
        Description: Initialize the InputController with a reference to the main game.
        Args:
            game (MinesweeperGame): Reference to the main game instance
        Returns: None
        Author: Raj Kaura
        Creation Date: September 18, 2025
        External Sources: N/A - Original Code
        """
        self.game = game
    
    def get_cell_from_mouse(self, mouse_pos):
        """
        Description: Convert mouse position to grid coordinates.
        Args:
            mouse_pos (tuple): Mouse position (x, y)
        Returns: tuple - Grid coordinates (row, col) or None if outside grid
        Author: Raj Kaura
        Creation Date: September 18, 2025
        External Sources: N/A - Original Code
        """
        x, y = mouse_pos
        
        # Check if click is within game grid area
        if (0 <= x < self.game.WINDOW_WIDTH and 
            self.game.INFO_HEIGHT <= y < self.game.WINDOW_HEIGHT):
            
            col = x // self.game.CELL_SIZE
            row = (y - self.game.INFO_HEIGHT) // self.game.CELL_SIZE
            
            if 0 <= row < self.game.GRID_HEIGHT and 0 <= col < self.game.GRID_WIDTH:
                return (row, col)
        
        return None
    
    def handle_cell_click(self, row, col, is_right_click=False):
        """
        Description: Handle a click on a specific cell (reveal or flag).
        Args:
            row (int): Grid row (0-9)
            col (int): Grid column (0-9)
            is_right_click (bool): True for right-click (flag), False for left-click (reveal)
        Returns: None
        Author: Raj Kaura
        Creation Date: September 18, 2025
        External Sources: N/A - Original Code
        """
        if not self.game.game_state.is_game_active():
            return
        
        if is_right_click:
            cell = self.game.board.grid[row][col]
            if not cell.is_revealed:
                if cell.is_flagged:
                    # Unflagging always allowed
                    if self.game.board.toggle_flag(row, col):
                        self.game.game_state.flags_left += 1
                        self.game._update_game_statistics()
                else:
                    # Only allow flagging if flags_left > 0
                    if self.game.game_state.flags_left > 0:
                        if self.game.board.toggle_flag(row, col):
                            self.game.game_state.flags_left -= 1
                            self.game._update_game_statistics()
                            # Check for victory after flagging
                            if self.game.board.is_game_won():
                                self.game.game_state.end_game(won=True)
                                self.game.show_end_screen = True
        else:
            # Left click reveals cell
            if not self.game.game_state.first_click_made:
                self.game.game_state.mark_first_click()
            
            mine_hit = self.game.board.reveal_cell(row, col)
            self.game._update_game_statistics()
            
            if mine_hit:
                # Game over - reveal all mines
                self.game.board.reveal_all_mines()
                self.game.game_state.end_game(won=False)
                self.game.show_end_screen = True
            elif self.game.board.is_game_won():
                # Victory condition
                self.game.game_state.end_game(won=True)
                self.game.show_end_screen = True
    
    def handle_events(self):
        """
        Description: Handle all Pygame events including mouse clicks and keyboard input.
        Args: None
        Returns: bool - True to continue game loop, False to quit
        Author: Raj Kaura
        Creation Date: September 18, 2025
        External Sources: N/A - Original Code
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.game.show_start_screen:
                        # Start game from start screen
                        self.game._start_new_game()
                    elif self.game.show_end_screen and self.game.game_state:
                        # Handle end screen space press
                        status = self.game.game_state.get_status_text()
                        if "Victory" in status:
                            # Win: start new game
                            self.game._start_new_game()
                        else:
                            # Loss: go to start screen
                            self.game.show_end_screen = False
                            self.game.show_start_screen = True
                    else:
                        # During gameplay: restart
                        self.game._start_new_game()
                elif event.key == pygame.K_r:
                    if self.game.show_end_screen and self.game.game_state and "Loss" in self.game.game_state.get_status_text():
                        # Retry with same settings after loss
                        self.game._start_new_game()
                    elif not self.game.show_end_screen and not self.game.show_start_screen:
                        # Reset during gameplay
                        self.game._start_new_game()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_UP:
                    # Increase mine count (works in start screen or end screen for wins)
                    if (self.game.show_start_screen or 
                        (self.game.show_end_screen and self.game.game_state and "Victory" in self.game.game_state.get_status_text())):
                        if self.game.mine_count < 20:
                            self.game.mine_count += 1
                elif event.key == pygame.K_MINUS or event.key == pygame.K_DOWN:
                    # Decrease mine count (works in start screen or end screen for wins)
                    if (self.game.show_start_screen or 
                        (self.game.show_end_screen and self.game.game_state and "Victory" in self.game.game_state.get_status_text())):
                        if self.game.mine_count > 10:
                            self.game.mine_count -= 1
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game.show_end_screen and not self.game.show_start_screen:
                cell_coords = self.get_cell_from_mouse(event.pos)
                if cell_coords:
                    row, col = cell_coords
                    is_right_click = event.button == 3  # Right mouse button
                    self.handle_cell_click(row, col, is_right_click)
        
        return True