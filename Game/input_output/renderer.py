"""
Module: renderer.py
Description: Handles all rendering and drawing of the Minesweeper game UI, including board, info panel, and end/start screens.
Author: John Tran
Creation Date: September 16, 2025
External Sources: N/A - Original Code
"""

import pygame

class Renderer:
    """
    Description: Handles all rendering and drawing operations for the Minesweeper game. Manages the visual representation of the game board, UI elements, and screen states (start screen, game screen, end screen).
    Author: John Tran
    Creation Date: September 16, 2025
    External Sources: N/A - Original Code
    """
    
    def __init__(self, game):
        """
        Description: Initialize the renderer with a reference to the main game.
        Args:
            game (MinesweeperGame): Reference to the main game instance
        Returns: None
        Author: John Tran
        Creation Date: September 16, 2025
        External Sources: N/A - Original Code
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
        Description: Draw the information panel (mine count, flags, timer, etc.).
        Args: None
        Returns: None
        Author: John Tran
        Creation Date: September 16, 2025
        External Sources: N/A - Original Code
        """
        if not self.game.game_state:
            return
            
        info_rect = pygame.Rect(0, 0, self.game.WINDOW_WIDTH, self.game.INFO_HEIGHT)
        info_color = self.game.theme_ui.get('info_background', self.game.COLORS['background'])
        pygame.draw.rect(self.game.screen, info_color, info_rect)
        
        # Game status
        status_text = self.game.font.render(f"Status: {self.game.game_state.get_status_text()}", True, self.game.COLORS['text'])
        self.game.screen.blit(status_text, (10, 10))
        
        # Turn
        current_player = self.game.game_state.current_player
        if self.game.game_state.ai_thinking_timer > 0:
            for _dot in range(int(self.game.game_state.ai_thinking_timer*4)):
                current_player += "."
        turn_text = self.game.font.render(f"Turn: {current_player}", True, self.game.COLORS['text'])
        self.game.screen.blit(turn_text, (200, 35))
        
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
        
        theme_text = self.game.small_font.render(
            f"Theme: {self.game.current_theme_name}",
            True,
            self.game.COLORS['text']
        )
        theme_rect = theme_text.get_rect(topright=(self.game.WINDOW_WIDTH - 10, 10))
        self.game.screen.blit(theme_text, theme_rect)

        theme_hint = self.game.small_font.render(
            "Press T to cycle", True, self.game.COLORS['text']
        )
        hint_rect = theme_hint.get_rect(topright=(self.game.WINDOW_WIDTH - 10, 30))
        self.game.screen.blit(theme_hint, hint_rect)

        # Column labels (A-J)
        for col in range(self.game.GRID_WIDTH):
            label = chr(ord('A') + col)
            label_text = self.game.small_font.render(label, True, self.game.COLORS['text'])
            x = col * self.game.CELL_SIZE + self.game.CELL_SIZE // 2 - label_text.get_width() // 2
            self.game.screen.blit(label_text, (x, self.game.INFO_HEIGHT - 20))
    
    def draw_row_labels(self):
        """
        Description: Draw row labels (1-10) on the left side of the grid.
        Args: None
        Returns: None
        Author: John Tran
        Creation Date: September 16, 2025
        External Sources: N/A - Original Code
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
        Description: Draw the end screen UI (win/loss).
        Args: None
        Returns: None
        Author: John Tran
        Creation Date: September 16, 2025
        External Sources: N/A - Original Code
        """
        if not self.game.game_state:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.WINDOW_WIDTH, self.game.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(self.game.theme_ui.get('overlay_background', (0, 0, 0)))
        self.game.screen.blit(overlay, (0, 0))
        
        # Get game status
        status = self.game.game_state.get_status_text()
        is_win = "Victory" in status
        
        # Main message
        title_color = (self.game.theme_ui.get('win_text', (0, 255, 0))
                       if is_win else self.game.theme_ui.get('loss_text', (255, 0, 0)))
        title_text = pygame.font.Font(None, 48).render(status, True, title_color)
        title_rect = title_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 150))
        self.game.screen.blit(title_text, title_rect)

        # Mine count adjustment
        mine_text_color = self.game.theme_ui.get('mine_text', (255, 255, 255))
        mine_text = self.game.font.render(f"Current mines: {self.game.mine_count}", True, mine_text_color)
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
            inst_text = self.game.small_font.render(
                instruction,
                True,
                self.game.theme_ui.get('start_text', (255, 255, 255))
            )
            inst_rect = inst_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 250 + i * 25))
            self.game.screen.blit(inst_text, inst_rect)
    
    def draw_start_screen(self):
        """
        Description: Draw the start screen UI.
        Args: None
        Returns: None
        Author: John Tran
        Creation Date: September 16, 2025
        External Sources: N/A - Original Code
        """
        # Clear background
        ui = self.game.theme_ui
        self.game.screen.fill(ui.get('start_background', self.game.COLORS['background']))

        # Title
        title_text = pygame.font.Font(None, 64).render(
            "MINESWEEPER",
            True,
            ui.get('start_title', self.game.COLORS['text'])
        )
        title_rect = title_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 80))
        self.game.screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_text = self.game.font.render(
            "EECS 581 Project 1",
            True,
            ui.get('start_subtitle', self.game.COLORS['text'])
        )
        subtitle_rect = subtitle_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 120))
        self.game.screen.blit(subtitle_text, subtitle_rect)

        # Mine count selection
        mine_text = pygame.font.Font(None, 36).render(
            f"Mines: {self.game.mine_count}",
            True,
            ui.get('accent', self.game.COLORS['text'])
        )
        mine_rect = mine_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 160))
        self.game.screen.blit(mine_text, mine_rect)

        # Theme display
        theme_display = self.game.font.render(
            f"Theme: {self.game.current_theme_name}",
            True,
            ui.get('start_header', self.game.COLORS['text'])
        )
        theme_rect = theme_display.get_rect(center=(self.game.WINDOW_WIDTH // 2, 190))
        self.game.screen.blit(theme_display, theme_rect)

        if self.game.theme_description:
            desc_text = self.game.small_font.render(
                self.game.theme_description,
                True,
                ui.get('start_text', self.game.COLORS['text'])
            )
            desc_rect = desc_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 210))
            self.game.screen.blit(desc_text, desc_rect)

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
            "• SPACE or 1 key: Start game",
            "• 2 key: Start game VS. AI (Easy)",
            "• 3 key: Start game VS. AI (Medium)",
            "• 4 key: Start game VS. AI (Hard) ",
            "• T key: Cycle theme (Shift+T for previous)",
            "• ESC: Quit"
        ]

        for i, instruction in enumerate(instructions):
            if instruction == "HOW TO PLAY:" or instruction == "CONTROLS:":
                color = ui.get('start_header', self.game.COLORS['text'])
                font = self.game.font
            elif instruction == "":
                continue  # Skip empty lines
            else:
                color = ui.get('start_text', self.game.COLORS['text'])
                font = self.game.small_font
            
            inst_text = font.render(instruction, True, color)
            inst_rect = inst_text.get_rect(center=(self.game.WINDOW_WIDTH // 2, 240 + i * 20))
            self.game.screen.blit(inst_text, inst_rect)
    
    def draw_game(self):
        """
        Description: Draw the complete game interface.
        Args: None
        Returns: None
        Author: John Tran
        Creation Date: September 16, 2025
        External Sources: N/A - Original Code
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
