import pygame
import sys
from board import Board
from gamestate import GameState, GameStatus

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
    
    def _get_cell_from_mouse(self, mouse_pos):
        """
        Convert mouse position to grid coordinates.
        
        Inputs: mouse_pos (tuple) - Mouse position (x, y)
        Outputs: tuple - Grid coordinates (row, col) or None if outside grid
        """
        # Original implementation - coordinate conversion
        x, y = mouse_pos
        
        # Check if click is within game grid area
        if (0 <= x < self.WINDOW_WIDTH and 
            self.INFO_HEIGHT <= y < self.WINDOW_HEIGHT):
            
            col = x // self.CELL_SIZE
            row = (y - self.INFO_HEIGHT) // self.CELL_SIZE
            
            if 0 <= row < self.GRID_HEIGHT and 0 <= col < self.GRID_WIDTH:
                return (row, col)
        
        return None
    
    def _handle_cell_click(self, row, col, is_right_click=False):
        """
        Handle a click on a specific cell.
        
        Inputs: row (int) - Grid row (0-9)
                col (int) - Grid column (0-9)
                is_right_click (bool) - True for right-click (flag), False for left-click (reveal)
        Outputs: None
        """
        # Original implementation - click handling logic
        if not self.game_state.is_game_active():
            return
        
        if is_right_click:
            # Right click toggles flag
            if self.board.toggle_flag(row, col):
                self._update_game_statistics()
                # Check for victory after flagging
                if self.board.is_game_won():
                    self.game_state.end_game(won=True)
                    self.show_end_screen = True
        else:
            # Left click reveals cell
            if not self.game_state.first_click_made:
                self.game_state.mark_first_click()
            
            mine_hit = self.board.reveal_cell(row, col)
            self._update_game_statistics()
            
            if mine_hit:
                # Game over - reveal all mines
                self.board.reveal_all_mines()
                self.game_state.end_game(won=False)
                self.show_end_screen = True
            elif self.board.is_game_won():
                # Victory condition
                self.game_state.end_game(won=True)
                self.show_end_screen = True
    
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
    
    def _draw_cell(self, row, col):
        """
        Draw a single cell on the screen.
        
        Inputs: row (int) - Grid row (0-9)
                col (int) - Grid column (0-9)
        Outputs: None
        """
        # Original implementation - cell rendering
        if not self.board:
            return
            
        cell = self.board.get_cell(row, col)
        if not cell:
            return
        
        # Calculate screen position
        x = col * self.CELL_SIZE
        y = row * self.CELL_SIZE + self.INFO_HEIGHT
        rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
        
        # Choose cell color based on state
        if cell.is_revealed:
            if cell.is_mine:
                color = self.COLORS['cell_mine']
            else:
                color = self.COLORS['cell_revealed']
        else:
            color = self.COLORS['cell_covered']
        
        # Draw cell background
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.COLORS['border'], rect, 1)
        
        # Draw cell content
        if cell.is_flagged and not cell.is_revealed:
            # Draw flag
            flag_text = self.font.render('F', True, self.COLORS['text'])
            text_rect = flag_text.get_rect(center=rect.center)
            self.screen.blit(flag_text, text_rect)
        elif cell.is_revealed:
            if cell.is_mine:
                # Draw mine
                mine_text = self.font.render('*', True, self.COLORS['text'])
                text_rect = mine_text.get_rect(center=rect.center)
                self.screen.blit(mine_text, text_rect)
            elif cell.adjacent_mines > 0:
                # Draw number with appropriate color
                number_color = self.COLORS['number_colors'].get(
                    cell.adjacent_mines, self.COLORS['text'])
                number_text = self.font.render(str(cell.adjacent_mines), True, number_color)
                text_rect = number_text.get_rect(center=rect.center)
                self.screen.blit(number_text, text_rect)
    
    def _draw_info_panel(self):
        """
        Draw the information panel showing game status and statistics.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - UI panel rendering
        if not self.game_state:
            return
            
        info_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, self.INFO_HEIGHT)
        pygame.draw.rect(self.screen, self.COLORS['background'], info_rect)
        
        # Game status
        status_text = self.font.render(f"Status: {self.game_state.get_status_text()}", 
                                     True, self.COLORS['text'])
        self.screen.blit(status_text, (10, 10))
        
        # Remaining mines
        mines_remaining = self.game_state.get_remaining_mines()
        mines_text = self.font.render(f"Mines: {mines_remaining}", 
                                    True, self.COLORS['text'])
        self.screen.blit(mines_text, (10, 35))
        
        # Instructions
        if not self.game_state.first_click_made:
            instruction_text = self.small_font.render("Left click: Reveal | Right click: Flag", 
                                                    True, self.COLORS['text'])
            self.screen.blit(instruction_text, (150, 10))
        
        # Column labels (A-J)
        for col in range(self.GRID_WIDTH):
            label = chr(ord('A') + col)
            label_text = self.small_font.render(label, True, self.COLORS['text'])
            x = col * self.CELL_SIZE + self.CELL_SIZE // 2 - label_text.get_width() // 2
            self.screen.blit(label_text, (x, self.INFO_HEIGHT - 20))
    
    def _draw_row_labels(self):
        """
        Draw row labels (1-10) on the left side of the grid.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - row label rendering
        for row in range(self.GRID_HEIGHT):
            label = str(row + 1)
            label_text = self.small_font.render(label, True, self.COLORS['text'])
            y = row * self.CELL_SIZE + self.INFO_HEIGHT + self.CELL_SIZE // 2 - label_text.get_height() // 2
            # Draw label to the left of the grid (requires expanding window width slightly)
            # For now, we'll skip row labels to maintain the specified window size
            pass
    
    def _draw_end_screen(self):
        """
        Draw the win/loss screen overlay with mine count adjustment.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - end screen overlay
        if not self.game_state:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Get game status
        status = self.game_state.get_status_text()
        is_win = "Victory" in status
        
        # Main message
        title_color = (0, 255, 0) if is_win else (255, 0, 0)
        title_text = pygame.font.Font(None, 48).render(status, True, title_color)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Mine count adjustment
        mine_text = self.font.render(f"Current mines: {self.mine_count}", True, (255, 255, 255))
        mine_rect = mine_text.get_rect(center=(self.WINDOW_WIDTH // 2, 200))
        self.screen.blit(mine_text, mine_rect)
        
        # Instructions - different for win vs loss
        if is_win:
            instructions = [
                "Press SPACE to play again",
                "Press UP/DOWN arrows to adjust mines (10-20)",
                "Press ESC to quit"
            ]
        else:
            instructions = [
                "Press SPACE to continue to setup",
                "Press R to retry with same settings",
                "Press ESC to quit"
            ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, (255, 255, 255))
            inst_rect = inst_text.get_rect(center=(self.WINDOW_WIDTH // 2, 250 + i * 25))
            self.screen.blit(inst_text, inst_rect)
    
    def _draw_start_screen(self):
        """
        Draw the start screen with instructions and mine count adjustment.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - start screen
        # Clear background
        self.screen.fill((64, 64, 64))  # Dark gray background
        
        # Title
        title_text = pygame.font.Font(None, 64).render("MINESWEEPER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font.render("EECS 581 Project 1", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(self.WINDOW_WIDTH // 2, 120))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Mine count selection
        mine_text = pygame.font.Font(None, 36).render(f"Mines: {self.mine_count}", True, (255, 255, 0))
        mine_rect = mine_text.get_rect(center=(self.WINDOW_WIDTH // 2, 180))
        self.screen.blit(mine_text, mine_rect)
        
        # Instructions
        instructions = [
            "HOW TO PLAY:",
            "• Left click to reveal cells",
            "• Right click to flag suspected mines",
            "• Avoid clicking on mines!",
            "• Flag all mines to win",
            "",
            "CONTROLS:",
            "• UP/DOWN arrows: Adjust mine count",
            "• SPACE: Start game",
            "• ESC: Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction == "HOW TO PLAY:" or instruction == "CONTROLS:":
                color = (255, 255, 0)  # Yellow for headers
                font = self.font
            elif instruction == "":
                continue  # Skip empty lines
            else:
                color = (255, 255, 255)  # White for regular text
                font = self.small_font
            
            inst_text = font.render(instruction, True, color)
            inst_rect = inst_text.get_rect(center=(self.WINDOW_WIDTH // 2, 220 + i * 20))
            self.screen.blit(inst_text, inst_rect)
    
    def _draw_game(self):
        """
        Draw the complete game interface.
        
        Inputs: None
        Outputs: None
        """
        # Original implementation - complete rendering
        if self.show_start_screen:
            self._draw_start_screen()
        else:
            self.screen.fill(self.COLORS['background'])
            
            # Draw information panel
            self._draw_info_panel()
            
            # Draw all cells
            for row in range(self.GRID_HEIGHT):
                for col in range(self.GRID_WIDTH):
                    self._draw_cell(row, col)
            
            # Draw end screen overlay if game is over
            if self.show_end_screen:
                self._draw_end_screen()
        
        pygame.display.flip()
    
    def _handle_events(self):
        """
        Handle all Pygame events including mouse clicks and keyboard input.
        
        Inputs: None
        Outputs: bool - True to continue game loop, False to quit
        """
        # Original implementation - event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.show_start_screen:
                        # Start game from start screen
                        self._start_new_game()
                    elif self.show_end_screen and self.game_state:
                        # Handle end screen space press
                        status = self.game_state.get_status_text()
                        if "Victory" in status:
                            # Win: start new game
                            self._start_new_game()
                        else:
                            # Loss: go to start screen
                            self.show_end_screen = False
                            self.show_start_screen = True
                    else:
                        # During gameplay: restart
                        self._start_new_game()
                elif event.key == pygame.K_r:
                    if self.show_end_screen and self.game_state and "Loss" in self.game_state.get_status_text():
                        # Retry with same settings after loss
                        self._start_new_game()
                    elif not self.show_end_screen and not self.show_start_screen:
                        # Reset during gameplay
                        self._start_new_game()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_UP:
                    # Increase mine count (works in start screen or end screen for wins)
                    if (self.show_start_screen or 
                        (self.show_end_screen and self.game_state and "Victory" in self.game_state.get_status_text())):
                        if self.mine_count < 20:
                            self.mine_count += 1
                elif event.key == pygame.K_MINUS or event.key == pygame.K_DOWN:
                    # Decrease mine count (works in start screen or end screen for wins)
                    if (self.show_start_screen or 
                        (self.show_end_screen and self.game_state and "Victory" in self.game_state.get_status_text())):
                        if self.mine_count > 10:
                            self.mine_count -= 1
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.show_end_screen and not self.show_start_screen:
                cell_coords = self._get_cell_from_mouse(event.pos)
                if cell_coords:
                    row, col = cell_coords
                    is_right_click = event.button == 3  # Right mouse button
                    self._handle_cell_click(row, col, is_right_click)
        
        return True
    
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
            
            # Draw game
            self._draw_game()
            
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