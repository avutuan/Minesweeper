
"""
Module: minesweeper.py
Description: Main entry point and game loop for the Minesweeper application. Handles initialization, event loop, and coordination between core logic, input, and rendering.
Author: Changwen Gong
Creation Date: September 17, 2025
External Sources: N/A - Original Code
"""

import copy
import multiprocessing
import os
import queue
import sys
from pathlib import Path

import pygame
from core.board import Board
from core.gamestate import GameState
from input_output.input_controller import InputController
from input_output.renderer import Renderer
from themes import THEMES

# attempt to import optional webview integration for side-by-side YouTube window
try:
    import webview
except ImportError:  # pragma: no cover - handled at runtime
    webview = None

# THE WEB
# https://youtu.be/XD3nq0eECz4
# SHORTS
# https://youtube.com/shorts
DEFAULT_SHORTS_URL = "https://youtube.com/shorts"
DEFAULT_STANDARD_URL = "https://youtu.be/XD3nq0eECz4"


def _prompt_for_youtube_selection():
    """Prompt the user for which YouTube experience to launch."""
    print("Choose the YouTube content to display alongside Minesweeper:")
    print("  0) None (default)")
    print("  1) YouTube Shorts")
    print("  2) Standard YouTube video")
    try:
        selection = input("Selection [0]: ").strip()
    except EOFError:
        selection = ""

    if selection == "2":
        return "YouTube Video", DEFAULT_STANDARD_URL
    elif selection == "1":
        return "YouTube Shorts", DEFAULT_SHORTS_URL
    return None, None


def _launch_browser_window(stop_event, message_queue, position, size, window_title, url):
    """Start the PyWebView browser window in a standalone process."""
    if webview is None:
        return

    width, height = size
    pos_x, pos_y = position

    browser_window = webview.create_window(
        window_title,
        url=url,
        width=width,
        height=height,
        x=pos_x,
        y=pos_y,
        resizable=True,
    )

    def on_closed():
        try:
            message_queue.put_nowait("closed")
        except Exception:
            pass
        stop_event.set()

    if hasattr(browser_window, "events") and hasattr(browser_window.events, "closed"):
        browser_window.events.closed += on_closed

    def monitor_stop():
        stop_event.wait()
        if hasattr(webview, "destroy_window"):
            try:
                webview.destroy_window(browser_window)
            except Exception:
                pass

    webview.start(monitor_stop)
    try:
        message_queue.put_nowait("terminated")
    except Exception:
        pass


class MinesweeperGame:
    """
    Description: Main Minesweeper game class using Pygame for graphical interface. Coordinates user interface, input processing, and game loop between Board and GameState classes.
    Author: Changwen Gong
    Creation Date: September 17, 2025
    External Sources: N/A - Original Code
    """
    
    def __init__(
        self,
        window_position=None,
        browser_queue=None,
        browser_process=None,
        browser_stop_event=None,
        browser_window_title=None,
        browser_window_url=None,
    ):
        """
        Description: Initialize the Minesweeper game with Pygame and default settings.
        Args: None
        Returns: None
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Initialize Pygame and set up game constants.
        if window_position:
            os.environ["SDL_VIDEO_WINDOW_POS"] = f"{window_position[0]},{window_position[1]}"

        pygame.init()

        # Set up game constants for grid and UI layout.
        self.CELL_SIZE = 40
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 10
        self.INFO_HEIGHT = 80

        # Calculate window dimensions based on grid and info panel.
        self.WINDOW_WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.WINDOW_HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE + self.INFO_HEIGHT

        # Track game state for start/end screens.
        self.show_end_screen = False
        self.show_start_screen = True

        # Initialize Pygame components
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Minesweeper - EECS 581 Project 1")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Initialize game components
        self.mine_count = 10  # Default mine count
        self.mode = "classic" # classic, easy, medium, hard
        self.board = None
        self.game_state = None
        self.delayed_events = []
        
        # Initialize I/O controllers
        self.browser_queue = browser_queue
        self.browser_process = browser_process
        self.browser_stop_event = browser_stop_event
        self.browser_window_title = browser_window_title
        self.browser_window_url = browser_window_url

        self.themes = THEMES
        self.theme_names = list(self.themes.keys())
        self.current_theme_index = 0
        self.current_theme_name = ""
        self.theme_description = ""
        self.theme_ui = {}
        self.COLORS = {}
        self.set_theme(self.theme_names[self.current_theme_index], announce=False)

        self.input_controller = InputController(self)
        self.renderer = Renderer(self)

        self._sound_load_warnings = set()
        self._sound_play_warnings = set()
        self.mine_hit_sound = self._load_sound("heheheha.mp3", "mine hit")
        self.normal_click_sound = self._load_sound("fahh.mp3", "click")
        self.flag_sound = self._load_sound("sixseven.mp3", "flag")
        # Don't start game immediately - show start screen first

    def _load_sound(self, file_name, label):
        sound_path = Path(__file__).resolve().parent.parent / file_name
        if not sound_path.exists():
            if label not in self._sound_load_warnings:
                print(f"{label.title()} sound not found at {sound_path}")
                self._sound_load_warnings.add(label)
            return None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            return pygame.mixer.Sound(str(sound_path))
        except Exception as sound_error:
            if label not in self._sound_load_warnings:
                print(f"Unable to load {label} sound: {sound_error}")
                self._sound_load_warnings.add(label)
            return None

    def set_theme(self, theme_name, announce=True):
        if theme_name not in self.themes:
            print(f"Theme '{theme_name}' not found.")
            return

        theme = self.themes[theme_name]
        self.COLORS = copy.deepcopy(theme.get("colors", {}))
        self.theme_ui = copy.deepcopy(theme.get("ui", {}))
        self.current_theme_name = theme_name
        self.theme_description = theme.get("description", "")
        self.current_theme_index = self.theme_names.index(theme_name)

        if announce:
            description = f" - {self.theme_description}" if self.theme_description else ""
            print(f"Theme set to {theme_name}{description}")

    def cycle_theme(self, direction=1):
        if not self.theme_names:
            return
        self.current_theme_index = (self.current_theme_index + direction) % len(self.theme_names)
        next_theme = self.theme_names[self.current_theme_index]
        self.set_theme(next_theme)

    def _start_new_game(self, mode):
        """
        Description: Start a new game by resetting board and game state.
        Args: None
        Returns: None
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Reset board and game state for a new session.
        
        self.board = Board(self.mine_count)
        self.game_state = GameState(self.mine_count, mode, self)
        self.show_end_screen = False
        self.show_start_screen = False
    
    def _update_game_statistics(self):
        """
        Description: Update game state with current board statistics (revealed cells, flags placed).
        Args: None
        Returns: None
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Update statistics in GameState from Board state.
        self.game_state.update_statistics(
            self.board.revealed_cells,
            self.board.get_flag_count()
        )
    
    def _handle_events(self):
        """
        Description: Handle all Pygame events by delegating to the InputController.
        Args: None
        Returns: bool - True to continue game loop, False to quit
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Delegate event handling to InputController.
        return self.input_controller.handle_events()
    
    def delay_event(self, delay, callback, update):
        """
        Description: Call a function on a delay
        Args: delay - Time in seconds
            callback - Function to call
            update - Function to call while updating
        Returns: None
        Author: Alejandro Sandoval
        Creation Date: October 2, 2025
        External Sources: N/A - Original Code
        """
        self.delayed_events.append({"time": 0, "delay": delay, "callback": callback, "update": update})
    
    def _update(self, delta_time):
        """
        Description: Update any animations or timed functions.
        Args: delta_time - Time elapsed since last update
        Returns: None
        Author: Alejandro Sandoval
        Creation Date: October 2, 2025
        External Sources: N/A - Original Code
        """
        for i in range(len(self.delayed_events)-1, -1, -1):
            event = self.delayed_events[i]
            event["time"] += delta_time
            event["update"](event["time"])
            if event["time"] > event["delay"]:
                event["callback"]()
                del self.delayed_events[i]
    
    def run(self):
        """
        Description: Main game loop - runs until player quits. Handles event processing, rendering, and frame rate control.
        Args: None
        Returns: None
        Author: Changwen Gong
        Creation Date: September 17, 2025
        External Sources: N/A - Original Code
        """
        # Print game instructions to console for user reference.
        running = True
        print("Minesweeper Game Started!")
        print("Controls:")
        print("- Left click: Reveal cell")
        print("- Right click: Toggle flag")
        print("- SPACE or 1 key: Start new game")
        print("- 2 key: Start new game VS. AI (Easy)")
        print("- 3 key: Start new game VS. AI (Medium)")
        print("- 4 key: Start new game VS. AI (Hard)")
        print("- R key: Reset game (during play)")
        print("- UP/DOWN arrows: Adjust mine count (10-20)")
        print("- +/- keys: Also adjust mine count")
        print("- ESC: Quit game")
        description_suffix = f" - {self.theme_description}" if self.theme_description else ""
        print(f"Current theme: {self.current_theme_name}{description_suffix}")
        print("- Press T to cycle theme (hold Shift for previous)")
        if (self.browser_window_url is not None):
            print(f"Web window: {self.browser_window_title} -> {self.browser_window_url}")

        # Main event loop for game execution.
        while running:
            # Control frame rate for smooth gameplay.
            delta_time = self.clock.tick(60) / 1000.0

            # Update animations
            self._update(delta_time)

            # Handle events from user input and system.
            running = self._handle_events()

            # Draw game using renderer to update UI.
            self.renderer.draw_game()

            # Monitor browser lifecycle messages.
            if self.browser_queue is not None:
                try:
                    while True:
                        message = self.browser_queue.get_nowait()
                        if message == "closed":
                            running = False
                            break
                except queue.Empty:
                    pass

            if self.browser_process is not None and not self.browser_process.is_alive():
                running = False

        # Clean up and exit Pygame when game ends.
        if webview is not None and hasattr(webview, "destroy_window"):
            try:
                for window in list(getattr(webview, "windows", [])):
                    webview.destroy_window(window)
            except Exception:
                pass

        if self.browser_stop_event is not None:
            self.browser_stop_event.set()

        pygame.quit()
        return

    def stop(self):
        """
        Description: Request the game loop to stop by posting a QUIT event.
        """
        if pygame.get_init():
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        if self.browser_stop_event is not None:
            self.browser_stop_event.set()

    def _play_sound(self, sound, label):
        if sound is None:
            return
        try:
            sound.play()
        except Exception as play_error:
            if label not in self._sound_play_warnings:
                print(f"Unable to play {label} sound: {play_error}")
                self._sound_play_warnings.add(label)

    def play_mine_hit_sound(self):
        """Play the mine hit sound if it was successfully loaded."""
        self._play_sound(self.mine_hit_sound, "mine hit")

    def play_normal_click_sound(self):
        """Play the sound associated with revealing a cell."""
        self._play_sound(self.normal_click_sound, "click")

    def play_flag_sound(self):
        """Play the sound associated with placing a flag."""
        self._play_sound(self.flag_sound, "flag")

def main():
    """
    Description: Main function to start the Minesweeper game. Handles instantiation and error handling.
    Args: None
    Returns: None
    Author: Changwen Gong
    Creation Date: September 17, 2025
    External Sources: N/A - Original Code
    """
    # Entry point for launching the game application.
    try:
        browser_process = None
        browser_queue = None
        browser_stop_event = None

        if webview is not None:
            video_title, video_url = _prompt_for_youtube_selection()
            if video_url is not None:
                print(f"Launching {video_title} window at {video_url}")

        game_window_position = (50, 50)
        game = MinesweeperGame(
            window_position=game_window_position,
            browser_window_title=video_title,
            browser_window_url=video_url,
        )

        if video_url is not None:
            webview_width = max(480, game.WINDOW_WIDTH)
            webview_height = game.WINDOW_HEIGHT
            browser_position_x = game_window_position[0] + game.WINDOW_WIDTH + 20
            browser_position_y = game_window_position[1]

            browser_queue = multiprocessing.Queue()
            browser_stop_event = multiprocessing.Event()

            browser_process = multiprocessing.Process(
                target=_launch_browser_window,
                args=(
                    browser_stop_event,
                    browser_queue,
                    (browser_position_x, browser_position_y),
                    (webview_width, webview_height),
                    video_title,
                    video_url,
                ),
                name="MinesweeperWebView",
            )
            browser_process.start()

            game.browser_queue = browser_queue
            game.browser_process = browser_process
            game.browser_stop_event = browser_stop_event

        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        pygame.quit()
        sys.exit(1)
    finally:
        if browser_stop_event is not None:
            browser_stop_event.set()
        if browser_process is not None:
            browser_process.join(timeout=3)
            if browser_process.is_alive():
                browser_process.terminate()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    # Run the main function if this script is executed directly.
    main()
