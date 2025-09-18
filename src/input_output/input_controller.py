from config import SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT, CELL_SIZE
import pygame

class InputController:
    """Maps mouse/keyboard events to high-level game Intents."""
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"action": "QUIT"}

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return {"action": "QUIT"}
                if event.key == pygame.K_r:
                    return {"action": "RESTART"}

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < HEADER_HEIGHT: # Ignore clicks in the HUD area
                    continue
                
                r = (y - HEADER_HEIGHT) // CELL_SIZE
                c = x // CELL_SIZE
                
                if event.button == 1: # Left click
                    return {"action": "REVEAL", "pos": (r, c)}
                if event.button == 3: # Right click
                    return {"action": "FLAG", "pos": (r, c)}
        
        return None # No relevant input