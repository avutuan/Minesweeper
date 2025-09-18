import pygame

class Renderer:
    """
    Handles all rendering and drawing operations for the Minesweeper game.
    
    Manages the visual representation of the game board, UI elements,
    and screen states (start screen, game screen, end screen).
    """
    
    def __init__(self, game):
        """
        Initialize the Renderer with a reference to the main game.
        
        Inputs: game (MinesweeperGame) - Reference to the main game instance
        Outputs: None (constructor)
        """
        self.game = game
    
    def draw_cell(self, row, col):
        """
        Draw a single cell on the screen.
        
        Inputs: row (int) - Grid row (0-9)
                col (int) - Grid column (0-9)
        Outputs: None
        """
        if not self.game.board:
            return
            
        cell = self.game.board.get_cell(row, col)
        if not cell:
            return
        
        # Calculate screen position
        x = col * self.game.CELL_SIZE
        y = row * self.game.CELL_SIZE + self.game.INFO_HEIGHT
        rect = pygame.Rect(x, y, self.game.CELL_SIZE, self.game.CELL_SIZE)
        
        # Choose cell color based on state
        if cell.is_revealed:
            if cell.is_mine:
                color = self.game.COLORS['cell_mine']
            else:
                color = self.game.COLORS['cell_revealed']
        else:
            color = self.game.COLORS['cell_covered']
        
        # Draw cell background
        pygame.draw.rect(self.game.screen, color, rect)
        pygame.draw.rect(self.game.screen, self.game.COLORS['border'], rect, 1)
        
        # Draw cell content
        if cell.is_flagged and not cell.is_revealed:
            # Draw flag
            flag_text = self.game.font.render('F', True, self.game.COLORS['text'])
            text_rect = flag_text.get_rect(center=rect.center)
            self.game.screen.blit(flag_text, text_rect)
        elif cell.is_revealed:
            if cell.is_mine:
                # Draw mine
                mine_text = self.game.font.render('*', True, self.game.COLORS['text'])
                text_rect = mine_text.get_rect(center=rect.center)
                self.game.screen.blit(mine_text, text_rect)
            elif cell.adjacent_mines > 0:
                # Draw number with appropriate color
                number_color = self.game.COLORS['number_colors'].get(
                    cell.adjacent_mines, self.game.COLORS['text'])
                number_text = self.game.font.render(str(cell.adjacent_mines), True, number_color)
                text_rect = number_text.get_rect(center=rect.center)
                self.game.screen.blit(number_text, text_rect)
    
    def draw_info_panel(self):
        """
        Draw the information panel showing game status and statistics.
        
        Inputs: None
        Outputs: None
        """
        if not self.game.game_state:
            return
            
        info_rect = pygame.Rect(0, 0, self.game.WINDOW_WIDTH, self.game.INFO_HEIGHT)
        pygame.draw.rect(self.game.screen, self.game.COLORS['background'], info_rect)
        
        # Game status
        status_text = self.game.font.render(f"Status: {self.game.game_state.get_status_text()}", 
                                         True, self.game.COLORS['text'])
        self.game.screen.blit(status_text, (10, 10))
        
        # Remaining mines
        mines_remaining = self.game.game_state.get_remaining_mines()
        mines_text = self.game.font.render(f"Mines: {mines_remaining}", 
                                        True, self.game.COLORS['text'])
        self.game.screen.blit(mines_text, (10, 35))
        
        # Instructions
        if not self.game.game_state.first_click_made:
            instruction_text = self.game.small_font.render("Left click: Reveal | Right click: Flag", 
                                                        True, self.game.COLORS['text'])
            self.game.screen.blit(instruction_text, (150, 10))
        
        # Column labels (A-J)
        for col in range(self.game.GRID_WIDTH):
            label = chr(ord('A') + col)
            label_text = self.game.small_font.render(label, True, self.game.COLORS['text'])
            x = col * self.game.CELL_SIZE + self.game.CELL_SIZE // 2 - label_text.get_width() // 2
            self.game.screen.blit(label_text, (x, self.game.INFO_HEIGHT - 20))
    
    def draw_row_labels(self):
        """
        Draw row labels (1-10) on the left side of the grid.
        
        Inputs: None
        Outputs: None
        """
        for row in range(self.game.GRID_HEIGHT):
            label = str(row + 1)
            label_text = self.game.small_font.render(label, True, self.game.COLORS['text'])
            y = row * self.game.CELL_SIZE + self.game.INFO_HEIGHT + self.game.CELL_SIZE // 2 - label_text.get_height() // 2
            # Draw label to the left of the grid (requires expanding window width slightly)
            # For now, we'll skip row labels to maintain the specified window size
            pass
    
    def draw_end_screen(self):
        """
        Draw the win/loss screen overlay with mine count adjustment.
        
        Inputs: None
        Outputs: None
        """
        if not self.game.game_state:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.WINDOW_WIDTH, self.game.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.game.screen.blit(overlay, (0, 0))
        
        # Get game status
        status = self.game.game_state.get_status_text()
        is_win = "Victory" in status
        
        # Main message
        title_color = (0, 255, 0) if is_win else (255, 0, 0)
        title_text = pygame.font.Font(None, 48).render(status, True, title_color)
        title_rect = title_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 150))
        self.game.screen.blit(title_text, title_rect)
        
        # Mine count adjustment
        mine_text = self.game.font.render(f"Current mines: {self.game.mine_count}", True, (255, 255, 255))
        mine_rect = mine_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 200))
        self.game.screen.blit(mine_text, mine_rect)
        
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
            inst_text = self.game.small_font.render(instruction, True, (255, 255, 255))
            inst_rect = inst_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 250 + i * 25))
            self.game.screen.blit(inst_text, inst_rect)
    
    def draw_start_screen(self):
        """
        Draw the start screen with instructions and mine count adjustment.
        
        Inputs: None
        Outputs: None
        """
        # Clear background
        self.game.screen.fill((64, 64, 64))  # Dark gray background
        
        # Title
        title_text = pygame.font.Font(None, 64).render("MINESWEEPER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 80))
        self.game.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.game.font.render("EECS 581 Project 1", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 120))
        self.game.screen.blit(subtitle_text, subtitle_rect)
        
        # Mine count selection
        mine_text = pygame.font.Font(None, 36).render(f"Mines: {self.game.mine_count}", True, (255, 255, 0))
        mine_rect = mine_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 180))
        self.game.screen.blit(mine_text, mine_rect)
        
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
                font = self.game.font
            elif instruction == "":
                continue  # Skip empty lines
            else:
                color = (255, 255, 255)  # White for regular text
                font = self.game.small_font
            
            inst_text = font.render(instruction, True, color)
            inst_rect = inst_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 220 + i * 20))
            self.game.screen.blit(inst_text, inst_rect)
    
    def draw_game(self):
        """
        Draw the complete game interface.
        
        Inputs: None
        Outputs: None
        """
        if self.game.show_start_screen:
            self.draw_start_screen()
        else:
            self.game.screen.fill(self.game.COLORS['background'])
            
            # Draw information panel
            self.draw_info_panel()
            
            # Draw all cells
            for row in range(self.game.GRID_HEIGHT):
                for col in range(self.game.GRID_WIDTH):
                    self.draw_cell(row, col)
            
            # Draw end screen overlay if game is over
            if self.game.show_end_screen:
                self.draw_end_screen()
        
        pygame.display.flip()