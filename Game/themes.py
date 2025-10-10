"""Theme definitions for Minesweeper UI styling."""

def _numbers_classic():
    return {
        1: (0, 0, 255),
        2: (0, 128, 0),
        3: (255, 0, 0),
        4: (0, 0, 128),
        5: (128, 0, 0),
        6: (0, 128, 128),
        7: (0, 0, 0),
        8: (128, 128, 128),
    }


def _numbers_ocean():
    return {
        1: (20, 80, 160),
        2: (10, 120, 100),
        3: (200, 70, 90),
        4: (40, 40, 140),
        5: (150, 60, 60),
        6: (20, 150, 140),
        7: (30, 50, 70),
        8: (80, 100, 120),
    }


def _numbers_midnight():
    return {
        1: (120, 180, 255),
        2: (140, 230, 170),
        3: (255, 140, 140),
        4: (160, 140, 255),
        5: (255, 200, 150),
        6: (120, 210, 255),
        7: (240, 240, 250),
        8: (180, 200, 220),
    }


def _numbers_pastel():
    return {
        1: (90, 140, 200),
        2: (120, 190, 120),
        3: (230, 150, 160),
        4: (160, 140, 210),
        5: (210, 130, 160),
        6: (140, 200, 200),
        7: (160, 160, 160),
        8: (180, 180, 180),
    }


THEMES = {
    "Classic": {
        "description": "Neutral Windows-inspired palette.",
        "colors": {
            "background": (192, 192, 192),
            "cell_covered": (160, 160, 160),
            "cell_revealed": (224, 224, 224),
            "cell_mine": (255, 0, 0),
            "cell_flag": (255, 255, 0),
            "border": (128, 128, 128),
            "text": (0, 0, 0),
            "number_colors": _numbers_classic(),
        },
        "ui": {
            "info_background": (182, 182, 182),
            "start_background": (64, 64, 64),
            "start_title": (255, 255, 255),
            "start_subtitle": (220, 220, 220),
            "start_header": (255, 255, 0),
            "start_text": (255, 255, 255),
            "mine_text": (255, 255, 255),
            "accent": (255, 215, 0),
            "overlay_background": (0, 0, 0),
            "win_text": (0, 255, 0),
            "loss_text": (255, 0, 0),
        },
    },
    "Ocean": {
        "description": "Bright blues with seafoam highlights.",
        "colors": {
            "background": (205, 230, 240),
            "cell_covered": (70, 130, 180),
            "cell_revealed": (235, 248, 252),
            "cell_mine": (220, 60, 80),
            "cell_flag": (255, 255, 255),
            "border": (40, 90, 120),
            "text": (20, 50, 70),
            "number_colors": _numbers_ocean(),
        },
        "ui": {
            "info_background": (180, 210, 225),
            "start_background": (20, 60, 100),
            "start_title": (245, 255, 255),
            "start_subtitle": (200, 230, 245),
            "start_header": (255, 245, 200),
            "start_text": (225, 240, 250),
            "mine_text": (230, 245, 255),
            "accent": (60, 160, 200),
            "overlay_background": (10, 30, 50),
            "win_text": (120, 255, 220),
            "loss_text": (255, 150, 160),
        },
    },
    "Midnight": {
        "description": "Low-light palette with neon numbers.",
        "colors": {
            "background": (30, 30, 45),
            "cell_covered": (60, 60, 90),
            "cell_revealed": (42, 42, 60),
            "cell_mine": (255, 90, 110),
            "cell_flag": (255, 210, 80),
            "border": (110, 110, 150),
            "text": (230, 230, 245),
            "number_colors": _numbers_midnight(),
        },
        "ui": {
            "info_background": (50, 50, 70),
            "start_background": (20, 20, 30),
            "start_title": (255, 220, 160),
            "start_subtitle": (200, 200, 220),
            "start_header": (255, 200, 120),
            "start_text": (220, 220, 235),
            "mine_text": (235, 235, 245),
            "accent": (120, 200, 255),
            "overlay_background": (5, 5, 10),
            "win_text": (150, 255, 190),
            "loss_text": (255, 140, 160),
        },
    },
    "Pastel": {
        "description": "Soft pastel tones for a relaxed vibe.",
        "colors": {
            "background": (245, 240, 245),
            "cell_covered": (220, 205, 230),
            "cell_revealed": (255, 252, 255),
            "cell_mine": (255, 140, 150),
            "cell_flag": (255, 210, 125),
            "border": (200, 185, 210),
            "text": (90, 90, 110),
            "number_colors": _numbers_pastel(),
        },
        "ui": {
            "info_background": (235, 225, 240),
            "start_background": (230, 215, 235),
            "start_title": (120, 90, 150),
            "start_subtitle": (150, 120, 180),
            "start_header": (180, 110, 160),
            "start_text": (110, 80, 140),
            "mine_text": (110, 80, 140),
            "accent": (200, 140, 190),
            "overlay_background": (120, 90, 130),
            "win_text": (140, 200, 150),
            "loss_text": (210, 120, 140),
        },
    },
}

