**1. Overview**  

This project builds upon a previously developed Minesweeper game by introducing a smart AI to play against. The AI module allows users to select between Easy, Medium, and Hard difficulty modes, each mode progressively increasing the decision-making logic.
Key enhancement features include:
Turn-based player vs. AI gameplay
Rule-based AI solver with adjustable difficulty
Automated flagging and revealing of cells
Integration with existing game state and UI
Modular architecture for future AI improvements
The original Minesweeper core was responsible for rendering, user interaction, and board logic. We it extended to support AI-driven moves while maintaining compatibility with manual play.

**2. High-Level Architecture**  

The enhanced system continues to follow a Model-View-Controller (MVC) pattern, extended with a new AI logic layer integrated into the controller.
Model: Board, Cell, and GameState handle game data and rules
View: Rendering/UI layer displays the grid, flags, and messages
Controller: Manages user input and alternates control between player and AI
AI Logic (New): Autonomous decision-making module that interacts with the controller and board

**3. Component Breakdown**  

AI Module (ai.py)
Responsibility:
 Implements all AI logic and decision-making processes. The AI interacts directly with the Board and GameState to make moves autonomously.


Key Functionality:

AI.__init__(mode, board, game): Initializes AI instance with difficulty and references to the board and game state.
AI.move(): Determines and executes one move per turn.


Easy: Randomly selects from covered cells.
Medium: Uses deterministic logic based on adjacent revealed numbers.
Hard: Incorporates probabilistic reasoning and multiple-cell pattern detection.


Interactions:
Reads current board and cell states.
Sends reveal or flag actions to the game controller.
Receives updates from GameState after executing moves.

Board and Cell Modules (board.py, cell.py)
Responsibility:
 Maintain all cell data, mine placement, and adjacency logic. Provide utility functions for the AI to analyze and interact with the board.


Key Functionality (New Enhancements):


get_covered_cells(): Returns a list of all unrevealed, unflagged cells.
get_hidden_neighbors(row, col): Returns covered neighbors for logic-based AI reasoning.


Interactions:

Communicates with both the AI module and the GameState to validate moves and update game progress.

GameState Module (gamestate.py)
Responsibility:
 Orchestrates the gameplay flow between the player, AI, and game board. Tracks current turn, win/loss state, and overall progress.


Key Functionality (Enhancements):


next_turn(): Alternates between player and AI turns.
ai_move(): Executes the AI’s move and processes results.
ai_update(time, delay): Manages turn timing and delayed AI animations.


Interactions:
Controls when AI logic executes.
Updates UI elements after AI actions.
Monitors and reports game-ending conditions.

Renderer and HUD (renderer.py, hud.py)
Responsibility:
 Display game visuals, messages, and AI activity updates. The HUD shows flag counts, difficulty mode, and current turn.


Key Functionality:
Renders animations for AI moves.
Updates status messages like “AI’s Turn” or “You Lost!”
Reflects changes from both player and AI moves.


Interactions:

Receives updated state data from GameState.
Refreshes visual components accordingly.

Main Controller (minesweeper.py)
Responsibility:
 Initializes the entire system, manages user interface events, and bridges communication between human input and AI-driven actions.


Key Functionality:
Launches game setup and difficulty selection.
Coordinates the main event loop.
Triggers alternating turns between player and AI.


Interactions:

Delegates logic to GameState.
Calls AI move execution when applicable.
Updates the renderer for each frame.

**4. Data Flow**  

Scenario: It is the AI’s turn to play a move.
Steps:
GameState.next_turn() detects that it’s the AI’s turn.
It triggers the AI’s move() method.
AI.move() analyzes the Board using get_covered_cells() or get_hidden_neighbors().


The AI selects a cell to reveal or flag.
Board updates the corresponding Cell state.
GameState checks for win/loss conditions and updates statistics.
The Renderer updates the display to reflect the new move.
Control returns to the player’s turn.

**5. Key Data Structures**  

AI
Fields:

mode: Current difficulty level (Easy, Medium, Hard)
board: Reference to game board object
game: Reference to game state manager


Purpose: Stores configuration and runtime logic for automated gameplay.


Board
Fields:

grid: 2D list of Cell objects
mine_count: Number of total mines
flags_left: Remaining flags


Purpose: Maintains mine distribution and adjacency data for both AI and player turns.

GameState
Fields:


turn: Indicates current player (Human or AI)
status: Game condition (PLAYING, WON, LOST)
ai_instance: Reference to active AI object


Purpose: Central hub for managing turns, status, and synchronization between components.

**6. How to Extend the System**  

Architectural Principles
Preserve separation between logic (Model), input (Controller), and display (View).
Keep the AI modular so new strategies can be introduced easily.
Maintain clear interfaces between AI, Board, and GameState.


Example Extension: Machine Learning-Based AI
To add on to the current program for predictive or adaptive gameplay:
Add a new module ai_ml.py for data-driven decision-making.
Record previous moves and game outcomes for reinforcement learning.
Update GameState to include logging for AI performance metrics

