# Difficulty settings: (rows, cols, num_mines)
DIFFICULTY = {
    "easy": (9, 9, 10),
    "medium": (16, 16, 40),
    "hard": (16, 30, 99)
}

# Select difficulty
ROWS, COLS, NUM_MINES = DIFFICULTY["easy"]

# Visuals
CELL_SIZE = 30
HEADER_HEIGHT = 60
SCREEN_WIDTH = COLS * CELL_SIZE + 32
SCREEN_HEIGHT = ROWS * CELL_SIZE + HEADER_HEIGHT + 32

# Colors
COLOR_BG = (192, 192, 192)
COLOR_HIDDEN = (180, 180, 180)
COLOR_REVEALED = (210, 210, 210)
COLOR_BORDER_LIGHT = (255, 255, 255)
COLOR_BORDER_DARK = (128, 128, 128)
COLOR_TEXT = (0, 0, 0)
COLOR_MINE = (255, 0, 0)
COLOR_OVERLAY_LOSS = (255, 0, 0, 128)
COLOR_OVERLAY_WIN = (0, 255, 0, 128)
NUMBER_COLORS = {
    1: (0, 0, 255),    # Blue
    2: (0, 128, 0),    # Green
    3: (255, 0, 0),    # Red
    4: (0, 0, 128),    # Dark Blue
    5: (128, 0, 0),    # Dark Red
    6: (0, 128, 128),  # Teal
    7: (0, 0, 0),      # Black
    8: (128, 128, 128) # Grey
}
