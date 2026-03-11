# Samurai X Adventure — Project Architecture & Code Guide

This document provides a complete, in-depth explanation of the Samurai X Adventure codebase. It is written for both **beginners** (who want to understand how a real game is structured) and **experienced developers** (who want to quickly navigate the design decisions and patterns used).

---

## Table of Contents

1. [High-Level Overview](#1-high-level-overview)
2. [Project Structure](#2-project-structure)
3. [Entry Point — main.py](#3-entry-point--mainpy)
4. [The Game Class — code/game.py](#4-the-game-class--codegamepy)
5. [Configuration — code/core/config.py](#5-configuration--codecoreconfigpy)
6. [Database — code/core/database.py](#6-database--codecoredatabasepy)
7. [Asset Loading — code/assets/loader.py](#7-asset-loading--codeassetsloaderpy)
8. [Entities](#8-entities)
   - 8.1 [Player — code/entities/player.py](#81-player--codeentitiesplayerpy)
   - 8.2 [Ground — code/entities/ground.py](#82-ground--codeentitiesgroundpy)
   - 8.3 [Obstacle — code/entities/obstacle.py](#83-obstacle--codeentitiesobstaclepy)
   - 8.4 [Bird — code/entities/bird.py](#84-bird--codeentitiesbirdpy)
   - 8.5 [Cloud — code/entities/cloud.py](#85-cloud--codeentitiescloudpy)
   - 8.6 [Tree — code/entities/tree.py](#86-tree--codeentitiestreepy)
9. [Systems](#9-systems)
   - 9.1 [Audio — code/systems/audio.py](#91-audio--codesystemsaudiopy)
   - 9.2 [Collision — code/systems/collision.py](#92-collision--codesystemscollisionpy)
   - 9.3 [Scoring — code/systems/scoring.py](#93-scoring--codesystemsscoringpy)
   - 9.4 [Spawner — code/systems/spawner.py](#94-spawner--codesystemsspawnerpy)
10. [User Interface](#10-user-interface)
    - 10.1 [Menu — code/ui/menu.py](#101-menu--codeuimenupy)
    - 10.2 [HUD — code/ui/hud.py](#102-hud--codeuihudpy)
    - 10.3 [Game Over — code/ui/game_over.py](#103-game-over--codeuigame_overpy)
11. [Design Patterns Used](#11-design-patterns-used)
12. [Key Python & Pygame Concepts](#12-key-python--pygame-concepts)
13. [Data Flow Diagrams](#13-data-flow-diagrams)
14. [Glossary](#14-glossary)

---

## 1. High-Level Overview

Samurai X Adventure is a **2D endless-runner** game. The player controls a samurai who runs forward automatically. The player's only actions are **jumping** (to avoid ground obstacles) and **ducking** (to avoid flying birds or tall obstacles). The game progressively increases in difficulty by:

- Increasing the scroll speed (everything moves faster).
- Decreasing the interval between enemy spawns (more enemies appear).

The game is built with:

- **Python 3.10+** as the programming language.
- **Pygame 2.6** as the game engine / rendering library.
- **SQLite** (via Python's built-in `sqlite3` module) for persistent score storage.

### How the game works at a glance

```
Player starts the game
        │
        ▼
   ┌─────────┐
   │  MENU   │ ◄─── Player sees title, controls, scoring info
   └────┬────┘
        │ "Start Game"
        ▼
  ┌───────────┐
  │NAME_SELECT│ ◄─── Player types or selects a name
  └─────┬─────┘
        │ Enter
        ▼
   ┌─────────┐
   │ PLAYING │ ◄─── Samurai runs, player jumps/ducks to avoid enemies
   └────┬────┘
        │ Collision with enemy
        ▼
  ┌───────────┐
  │ GAME_OVER │ ◄─── Death animation plays, score is saved to database
  └─────┬─────┘
        │ Space → restart  /  Escape → menu
        ▼
  (back to PLAYING or MENU)
```

---

## 2. Project Structure

```
samurai-x-adventure-demo-game/
│
├── main.py                       # Minimal entry point
├── objects.py                    # Legacy file (no longer used)
├── requirements.txt              # Python dependencies (pygame==2.6.1)
│
├── code/                         # All game source code
│   ├── __init__.py               # Makes code/ a Python package
│   ├── game.py                   # Main Game class (orchestrator)
│   │
│   ├── core/                     # Core infrastructure
│   │   ├── config.py             # Constants, paths, settings
│   │   └── database.py           # SQLite score persistence
│   │
│   ├── assets/                   # Asset management
│   │   └── loader.py             # Image/sound loading with caching
│   │
│   ├── entities/                 # Game objects
│   │   ├── player.py             # Samurai character
│   │   ├── ground.py             # Scrolling ground tiles
│   │   ├── obstacle.py           # Ground-level obstacles
│   │   ├── bird.py               # Flying bird enemies
│   │   ├── cloud.py              # Background clouds
│   │   └── tree.py               # Midground trees
│   │
│   ├── systems/                  # Game logic systems
│   │   ├── audio.py              # Music and sound effects
│   │   ├── collision.py          # Pixel-perfect collision detection
│   │   ├── scoring.py            # Score tracking and milestones
│   │   └── spawner.py            # Entity spawning and difficulty
│   │
│   └── ui/                       # User interface
│       ├── menu.py               # Main menu, name input, scoreboard
│       ├── hud.py                # In-game score display
│       └── game_over.py          # Game over overlay
│
├── assets/                       # Game assets (images and sounds)
│   ├── samurai-run/              # 8 running animation frames
│   ├── samurai-jump/             # 12 jumping animation frames
│   ├── samurai-bent-down/        # 2 ducking animation frames
│   ├── samurai-dead/             # 3 death animation frames
│   ├── samurai-idle/             # 1 idle frame (unused)
│   ├── obstacles/                # 14 obstacle sprite types
│   ├── bird/                     # 6 bird animation frames
│   ├── scenario/                 # Ground tile, clouds, trees, backgrounds
│   └── sounds/                   # Music tracks and sound effects
│
└── docs/                         # Documentation
```

### Why this structure?

The project follows a **modular architecture** inspired by professional game development practices:

- **Separation of concerns**: Each module handles exactly one responsibility.
- **Package organization**: Related modules are grouped into sub-packages (`core/`, `entities/`, `systems/`, `ui/`).
- **No logic in the entry point**: `main.py` only creates and starts the game. This makes the codebase testable and reusable.

---

## 3. Entry Point — main.py

```python
from code.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
```

### What's happening here?

- `from code.game import Game` — Imports the `Game` class from the `code` package.
- `if __name__ == "__main__":` — A Python idiom that ensures this code only runs when the file is executed directly (not when imported as a module).
- `game = Game()` — Creates the game instance, which initializes Pygame, loads assets, sets up systems, and prepares the window.
- `game.run()` — Starts the main game loop, which runs until the player quits.

### For beginners

The `__name__` guard is a Python best practice. When you run `python main.py`, Python sets `__name__` to `"__main__"`. If another file imports `main`, `__name__` would be `"main"` instead, and the game wouldn't auto-start. This pattern keeps the entry point clean and prevents accidental execution.

---

## 4. The Game Class — code/game.py

This is the **heart of the application**. It contains the game loop, state machine, event handling, and rendering orchestration.

### 4.1 GameState Enum

```python
class GameState(Enum):
    MENU = "menu"
    NAME_SELECT = "name_select"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    SCOREBOARD = "scoreboard"
```

An `Enum` is used instead of string constants to prevent typos and enable IDE autocompletion. The game transitions between these states based on player actions.

### 4.2 State Machine Transitions

```
MENU ──── "Start Game" ────► NAME_SELECT ──── Enter ────► PLAYING
  │                                                          │
  │ "View Scores"                                   Collision detected
  ▼                                                          │
SCOREBOARD ◄── Escape ──── GAME_OVER ◄──────────────────────┘
  │                            │
  │ Any key                    │ Space
  ▼                            ▼
MENU                       PLAYING (restart)
```

Each state has its own:
- **Event handler** — What happens when the player presses keys.
- **Update logic** — How the game world changes each frame.
- **Render logic** — What gets drawn to the screen.

### 4.3 The Game Loop

The game loop follows the standard pattern used in virtually all real-time games:

```
while running:
    1. Handle events (input)
    2. Update game state (logic)
    3. Render (draw)
    4. Tick clock (maintain FPS)
```

Here is a simplified view of how it works:

```python
def run(self):
    while self._running:
        self._handle_events()   # Process keyboard/mouse input
        self._update()          # Update positions, check collisions
        self._render()          # Draw everything to the screen
        self._clock.tick(FPS)   # Cap at 60 FPS
```

### 4.4 Event Handling

The `_handle_events` method processes Pygame events (key presses, window close, etc.) and routes them based on the current `GameState`:

- **MENU**: Arrow keys navigate the menu. Enter selects an option. Escape quits.
- **NAME_SELECT**: Typing adds characters to the name. Arrow keys scroll through previously used names. Enter confirms. Backspace deletes.
- **PLAYING**: Space/Up jumps (only if grounded). Down ducks (only if grounded). Escape returns to menu.
- **GAME_OVER**: Space restarts (after death animation completes). Escape goes to menu.
- **SCOREBOARD**: Any key returns to menu.

### 4.5 Update Logic (PLAYING state)

Every frame during gameplay:

1. **Spawner ticks** — Checks if it's time to spawn a new enemy, cloud, or tree.
2. **Difficulty scaling** — Every 100 frames, speed increases by 0.1 and the spawn interval decreases by 0.5 (minimum 30).
3. **Entity updates** — Each entity moves based on current speed, with parallax factors applied.
4. **Collision check** — Tests the player's mask against all enemy masks.
5. **Scoring** — Awards points when an enemy's right edge passes behind the player's left edge.
6. **Checkpoint** — If the score crosses a 100-point threshold, a milestone sound plays.

### 4.6 Rendering Order

The rendering order creates the **parallax depth effect**:

```
Layer 0 (farthest) : Sky background color (SKY_BLUE fill)
Layer 1             : Clouds (scroll at 30% of game speed)
Layer 2             : Trees (scroll at 50% of game speed)
Layer 3             : Ground tiles (scroll at 100% of game speed)
Layer 4             : Obstacles (scroll at 100% of game speed)
Layer 5             : Birds (scroll at game speed - 1)
Layer 6 (closest)   : Player (fixed X position)
Layer 7 (overlay)   : HUD (score display)
```

Objects farther away scroll slower, creating a convincing illusion of depth in a 2D world.

### 4.7 Key Instance Variables

| Variable | Type | Purpose |
|---|---|---|
| `_state` | `GameState` | Current game state |
| `_speed` | `float` | Current scroll speed (starts at 5.0) |
| `_frame_counter` | `int` | Global frame counter for spawning/difficulty |
| `_enemy_interval` | `float` | Frames between enemy spawns (starts at 100, min 30) |
| `_player_name` | `str` | Current player's name |
| `_score_saved` | `bool` | Prevents saving the same score twice |
| `_player` | `Player` | The samurai character |
| `_obstacle_group` | `pygame.sprite.Group` | All active obstacles |
| `_bird_group` | `pygame.sprite.Group` | All active birds |
| `_cloud_group` | `pygame.sprite.Group` | All active clouds |
| `_tree_group` | `pygame.sprite.Group` | All active trees |

---

## 5. Configuration — code/core/config.py

This file centralizes **every magic number** in the project. Instead of scattering `800`, `300`, `60`, etc., throughout the codebase, they are all defined here as named constants.

### Why centralize constants?

1. **Readability** — `SCREEN_WIDTH` is immediately understandable; `800` is not.
2. **Maintainability** — Changing the screen size means editing one file, not searching the entire project.
3. **Discoverability** — New developers can look here to understand the game's configuration at a glance.

### Organization of Constants

The constants are grouped by category:

#### Paths

```python
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
DB_PATH = ROOT_DIR / "samurai_scores.db"
```

`pathlib.Path` is used instead of string concatenation. This makes paths cross-platform (works on Windows, macOS, and Linux) and avoids issues with forward vs. backward slashes.

`ROOT_DIR` is computed dynamically: starting from `config.py`'s location (`code/core/config.py`), it goes up three levels to reach the project root.

#### Screen & Performance

```python
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
FPS = 60
```

#### Colors (RGB tuples)

```python
SKY_BLUE = (197, 226, 243)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
```

#### Player Settings

```python
PLAYER_X = 60                # Fixed horizontal position
PLAYER_BASE_Y = 262          # Ground level (bottom of sprite)
PLAYER_RUN_SIZE = (52, 58)   # Sprite dimensions while running
PLAYER_DUCK_SIZE = (70, 38)  # Wider and shorter when ducking
PLAYER_JUMP_HEIGHT = 15      # Initial upward velocity (pixels/frame)
PLAYER_GRAVITY = 1           # Downward acceleration (pixels/frame²)
```

#### Animation Frame Counts & Speeds

```python
PLAYER_RUN_FRAME_COUNT = 8    # 8 images in the run animation
RUN_ANIM_SPEED = 4            # Advance one frame every 4 game frames
```

**Animation speed** controls how fast sprites change. At 60 FPS with `RUN_ANIM_SPEED = 4`, the run animation cycles at 15 sprite changes per second, creating smooth running motion.

#### Spawning & Difficulty

```python
ENEMY_SPAWN_INTERVAL = 100     # Frames between enemy spawns (initial)
MIN_ENEMY_INTERVAL = 30        # Minimum frames between spawns (max difficulty)
INITIAL_SPEED = 5              # Starting scroll speed
SPEED_INCREMENT = 0.1          # Speed increase per milestone
SPEED_INCREASE_INTERVAL = 100  # Frames between speed increases
ENEMY_INTERVAL_DECREASE = 0.5  # Spawn interval reduction per milestone
```

---

## 6. Database — code/core/database.py

The `Database` class manages persistent score storage using SQLite.

### Schema

```sql
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);
```

Two tables are used:
- **players** — Stores unique player names. Using a separate table avoids duplicating the player name for every score entry.
- **scores** — Stores each game result with a timestamp. Links to `players` via `player_id`.

### Key Methods

**`get_or_create_player(name: str) -> int`**

Checks if a player already exists. If so, returns their ID. If not, inserts a new row and returns the new ID. This uses `INSERT OR IGNORE` to safely handle duplicates.

**`save_score(player_name: str, score: int)`**

Combines `get_or_create_player` and an `INSERT INTO scores` to save a game result in one call.

**`get_top_scores(limit: int = 10)`**

Returns the top scores ordered by score descending, joining with the `players` table to retrieve names. This powers the scoreboard screen.

**`get_player_names() -> list[str]`**

Returns all player names from the database. Used by the name selection screen to show previously used names.

### WAL Mode

The database is opened with `journal_mode=WAL` (Write-Ahead Logging). This improves concurrent read/write performance, although for a single-player game the main benefit is robustness against crashes during writes.

### For beginners

SQLite is a lightweight database that stores everything in a single file (`samurai_scores.db`). Unlike MySQL or PostgreSQL, it requires no server — Python's built-in `sqlite3` module handles it directly. The file is created automatically on first run and excluded from version control via `.gitignore`.

---

## 7. Asset Loading — code/assets/loader.py

The `AssetLoader` class handles all image and sound loading with a caching layer.

### Why caching matters

Loading an image from disk involves reading bytes, decoding the image format, and creating a Pygame surface. Doing this every frame would be extremely slow. The `AssetLoader` loads each asset **once** and stores it in a dictionary. Subsequent requests for the same asset return the cached version instantly.

### Image Loading

```python
def load_image(self, relative_path: str, size: tuple[int, int] | None = None) -> pygame.Surface:
```

- Loads an image from `assets/{relative_path}`.
- Optionally scales it to `size`.
- Calls `convert_alpha()` for rendering performance (pre-multiplies alpha channel).
- Caches by `"{path}_{size}"` — so the same image at different sizes is cached separately.

### Animation Sequence Loading

```python
def load_image_sequence(self, folder: str, prefix: str, count: int, size: tuple) -> list[pygame.Surface]:
```

Loads numbered frames like `samurai-run/samurai-run-1.png` through `samurai-run-8.png`. Returns a list of surfaces used for sprite animation.

### Sound Loading

```python
def load_sound(self, relative_path: str) -> pygame.mixer.Sound:
```

Loads a sound effect file and caches it. Used for jump, death, and checkpoint sounds.

### Music Path Resolution

```python
def get_music_path(self, relative_path: str) -> str:
```

Returns the absolute path to a music file. Pygame's `mixer.music` module requires a file path (not a Sound object), so this method provides that without loading the file into memory.

### For beginners

Think of the `AssetLoader` as a library: the first time you check out a book (load an image), it's fetched from the shelf (disk). After that, you keep it on your desk (cache), so looking at it again is instant. This is the **Cache pattern** — a fundamental optimization in game development.

---

## 8. Entities

Entities are the **game objects** — things you can see and interact with. Each entity is responsible for its own appearance and movement.

### 8.1 Player — code/entities/player.py

The Player class is the most complex entity. It models the samurai character with multiple animation states and physics.

#### State Management

The player has four visual states:

| State | Trigger | Animation | Behavior |
|---|---|---|---|
| **Running** | Default (no input) | 8 frames, cycles continuously | Fixed position |
| **Jumping** | Space or Up Arrow | 12 frames, plays once | Rises and falls with gravity |
| **Ducking** | Down Arrow (while grounded) | 2 frames, cycles while held | Shorter hitbox, wider sprite |
| **Dead** | Collision detected | 3 frames, plays once | Falls to ground if airborne |

#### Physics Model

The player uses a simple but effective physics model:

```
Position:   y += velocity
Velocity:   velocity += gravity    (gravity = 1 pixel/frame²)
Jump:       velocity = -15         (instant upward impulse)
Landing:    if y >= base_y → y = base_y, velocity = 0
```

This creates a natural-looking parabolic jump arc. The jump height is determined by the initial velocity (`-15`), and gravity pulls the player back down at a rate of 1 pixel per frame squared.

#### Animation System

Each animation state has:
- A list of **frames** (Pygame surfaces)
- An **animation speed** (game frames per sprite frame change)
- A **frame index** counter

The `_animate` method advances through the frame list:

```python
def _animate(self, frames: list, speed: int):
    self._anim_counter += 1
    if self._anim_counter >= speed:
        self._anim_counter = 0
        self._frame_index = (self._frame_index + 1) % len(frames)
    self.image = frames[self._frame_index]
```

The modulo operator (`%`) makes the animation loop. For the death animation, looping stops when the last frame is reached.

#### Collision Mask

After each animation frame change, the player's collision mask is regenerated:

```python
self.mask = pygame.mask.from_surface(self.image)
```

A **mask** is a pixel-level representation of which pixels are opaque. This enables pixel-perfect collision detection — the game only registers a hit when actual visible pixels overlap, not just bounding rectangles.

#### Size-Changing Animations

When the player switches between running (`52×58`) and ducking (`70×38`), the sprite dimensions change. The `rect` is recalculated to keep the player anchored at the correct ground position, preventing visual "jumps" when switching states.

### 8.2 Ground — code/entities/ground.py

The ground creates the illusion of infinite scrolling.

#### How Infinite Scrolling Works

The ground uses a simple but elegant technique:

```python
self._scroll_x = (self._scroll_x + speed) % self._width
```

The `%` (modulo) operator keeps `_scroll_x` within `[0, tile_width)`. This means the offset wraps around seamlessly — when the first tile scrolls completely off-screen, the math automatically resets, creating a perfect loop.

#### Rendering Multiple Tiles

```python
def draw(self, surface):
    x = -int(self._scroll_x)
    tiles_needed = screen_width // tile_width + 3
    for i in range(tiles_needed):
        surface.blit(self._image, (x + i * self._width, self._y))
```

Multiple copies of the ground tile are drawn side by side. The `+3` buffer ensures there's always enough tiles to cover the screen, even during fast scrolling.

#### Not a Sprite

Unlike other entities, `Ground` does **not** extend `pygame.sprite.Sprite`. It doesn't need collision detection or group management — it's purely visual. This is an example of choosing the simplest appropriate abstraction.

### 8.3 Obstacle — code/entities/obstacle.py

Obstacles are ground-level hazards that the player must jump over.

#### Key Properties

- **Sprite type**: Random selection from 14 obstacle images.
- **Scale**: Each obstacle is rendered at 65% of its original size (`OBSTACLE_SCALE = 0.65`).
- **Position**: Spawns at the right edge of the screen, aligned to `Y = 265` (ground level).
- **Movement**: Scrolls left at the current game speed.
- **Lifecycle**: Automatically removed (`kill()`) when it leaves the screen (`rect.right <= 0`).

#### Scored Flag

Each obstacle has a `scored` boolean:

```python
# In the game update loop:
if not obstacle.scored and obstacle.rect.right < player.rect.left:
    obstacle.scored = True
    score_manager.add_obstacle_points()  # +10 points
```

This ensures points are awarded exactly once per obstacle, at the moment it passes behind the player.

### 8.4 Bird — code/entities/bird.py

Birds are flying enemies that require the player to duck.

#### Differences from Obstacles

| Aspect | Obstacle | Bird |
|---|---|---|
| Position | Ground level (Y=265) | Air level (Y=200 or 220) |
| Animation | Static sprite | 6-frame wing flapping |
| Score value | +10 | +20 (harder to dodge) |
| Scroll speed | Full game speed | Game speed - 1 (slightly slower) |
| Spawn rate | 90% of enemies | 10% of enemies |

#### Two Flight Paths

Birds spawn at one of two heights (`BIRD_Y_OPTIONS = [200, 220]`). This creates variety — some birds require a well-timed duck, while others might need the player to stay ducked longer.

### 8.5 Cloud — code/entities/cloud.py

Clouds are purely decorative background elements.

#### Parallax Speed

Clouds scroll at 30% of the game speed (`CLOUD_SPEED_FACTOR = 0.3`). Because they move slower than the foreground, they appear to be far away, creating a sense of depth. This technique is called **parallax scrolling**.

#### Spawn Details

- **3 different cloud sprites** for visual variety.
- Spawned every 150 frames.
- Positioned at random heights between Y=20 and Y=100.
- 5 clouds are spawned at game start to fill the sky immediately.

### 8.6 Tree — code/entities/tree.py

Trees are midground decorative elements, positioned between the clouds and the ground.

#### Parallax Speed

Trees scroll at 50% of the game speed (`TREE_SPEED_FACTOR = 0.5`). Faster than clouds but slower than the ground, placing them visually between the background and foreground layers.

#### Spawn Details

- **6 different tree sprites** for variety.
- Spawned every 200 frames.
- Anchored at Y=245 (just above the ground tiles).
- 3 trees are spawned at game start.

---

## 9. Systems

Systems contain **game logic** that operates on multiple entities or manages cross-cutting concerns. They do not have visual representations.

### 9.1 Audio — code/systems/audio.py

The `AudioManager` handles all music and sound effects.

#### Music Management

The game has two music tracks with very different purposes:

| Track | State | Volume | Purpose |
|---|---|---|---|
| Menu music | MENU, NAME_SELECT, SCOREBOARD | 50% | Energetic, sets the mood |
| Game music | PLAYING, GAME_OVER | 15% | Quiet, doesn't distract from gameplay |

#### Smart Switching

The `AudioManager` tracks which music is currently playing (`_current_music`). If you call `play_menu_music()` when menu music is already playing, it does nothing. This prevents restarting the track when transitioning between menu-related states.

#### Sound Effects

Three sound effects are loaded via the `AssetLoader`:

| Effect | File | Trigger |
|---|---|---|
| Jump | `jump-song.wav` | Player presses Space/Up |
| Death | `die-song.wav` | Collision detected |
| Checkpoint | `checkPoint-song.wav` | Score crosses 100-point milestone |

#### For beginners

Pygame has two audio systems:
- **`pygame.mixer.music`** — For background music. Only one track can play at a time. It streams from disk, saving memory.
- **`pygame.mixer.Sound`** — For sound effects. Multiple sounds can play simultaneously. The entire file is loaded into memory for instant playback.

### 9.2 Collision — code/systems/collision.py

The `CollisionSystem` provides pixel-perfect collision detection.

#### How Mask-Based Collision Works

```python
@staticmethod
def check(player, obstacle_group, bird_group) -> bool:
    for enemy in list(obstacle_group) + list(bird_group):
        if pygame.sprite.collide_mask(player, enemy):
            return True
    return False
```

1. **Bounding box pre-check** — Pygame first checks if the rectangular bounding boxes overlap. If they don't, there's no collision (fast rejection).
2. **Mask comparison** — If boxes overlap, Pygame compares the actual pixel masks. A collision is registered only if **opaque pixels** from both sprites overlap.

#### Why not use rectangle collision?

Consider a bird sprite with outstretched wings. Its rectangular bounding box is much larger than the visible pixels. With rectangle collision, the player would "die" when passing near the tips of invisible pixels. Mask collision is more fair and accurate.

#### Static Method

`check` is a `@staticmethod` — it doesn't use any instance state. This is a design choice that makes it clear the method is a pure function: given the same inputs, it always produces the same output.

### 9.3 Scoring — code/systems/scoring.py

The `ScoreManager` tracks the player's score and detects milestone checkpoints.

#### Point System

| Event | Points |
|---|---|
| Obstacle passes player | +10 |
| Bird passes player | +20 |

Points are awarded when the enemy's right edge passes the player's left edge. This feels natural — you've "survived" the obstacle.

#### Checkpoint Detection

```python
def check_checkpoint(self) -> bool:
    current_checkpoint = self._score // 100
    if current_checkpoint > self._last_checkpoint:
        self._last_checkpoint = current_checkpoint
        return True
    return False
```

Integer division (`//`) maps the score to a checkpoint number: 0–99 → 0, 100–199 → 1, 200–299 → 2, etc. When the checkpoint number increases, a milestone was crossed.

This approach is elegant because it handles all milestones with a single comparison, regardless of how many points were added in one frame.

### 9.4 Spawner — code/systems/spawner.py

The `Spawner` is responsible for creating new entities at the right time.

#### Spawning Schedule

| Entity | Interval | Behavior |
|---|---|---|
| **Enemies** | Dynamic (100→30 frames) | 10% chance of bird, 90% obstacle |
| **Clouds** | Every 150 frames | Always one cloud |
| **Trees** | Every 200 frames | Always one tree |

#### Enemy Selection

```python
if random.randint(1, 10) == 5:
    # Spawn a bird (10% probability)
else:
    # Spawn an obstacle (90% probability)
```

The `random.randint(1, 10) == 5` check gives a 10% probability for birds. Any single value from 1–10 would work — choosing 5 is arbitrary but consistent.

#### Difficulty Progression

The enemy spawn interval decreases over time:

```
Frame    0: enemy every 100 frames (~1.67 seconds)
Frame  200: enemy every 99  frames
Frame 1400: enemy every 30  frames (~0.5 seconds) ← max difficulty
```

Combined with increasing scroll speed, this creates a natural difficulty curve that starts gentle and becomes intense.

#### Factory Behavior

The spawner acts as a **Factory** — it creates entity instances without the caller needing to know the creation details (which sprite, which position, which animation). The Game class simply calls `spawner.tick()` and gets new entities added to the appropriate groups.

---

## 10. User Interface

The UI layer handles everything the player sees that isn't a game entity — menus, overlays, and score displays.

### 10.1 Menu — code/ui/menu.py

The `MenuRenderer` handles three different screens:

#### Main Menu

```
┌──────────────────────────────────────┐
│         Samurai X  (gold, 52px)      │
│                                      │
│       > Start Game                   │
│         View Scores                  │
│         Exit                         │
│                                      │
│  Controls:            Scoring:       │
│  Space/Up - Jump      Obstacle: +10  │
│  Down - Duck          Bird: +20      │
│  Space - Restart                     │
│  Escape/Q - Quit                     │
└──────────────────────────────────────┘
```

The currently selected option is highlighted. Arrow keys move the selection, Enter confirms.

#### Name Selection Screen

Shows a text input field and a list of previously used names from the database. Players can type a new name or use arrow keys to select an existing one. Maximum name length is 15 characters.

#### Scoreboard

Displays the top 10 scores in a table format with rank, player name, score, and date. The #1 score is highlighted in gold.

### 10.2 HUD — code/ui/hud.py

The `HUDRenderer` draws the current score in the top-right corner during gameplay:

```
                                Score: 00345
                                HI: 05120
```

- Current score in white.
- High score in gold (only shown if greater than 0).
- Zero-padded to 5 digits for consistent alignment.

### 10.3 Game Over — code/ui/game_over.py

The `GameOverRenderer` displays a semi-transparent overlay after the death animation finishes:

```
┌──────────────────────────────────────┐
│  ████████████████████████████████████│
│  ██                              ████│
│  ██      GAME OVER  (gold)       ████│
│  ██                              ████│
│  ██    Score: 01234  (white)     ████│
│  ██                              ████│
│  ██  Press SPACE to restart      ████│
│  ██  Press ESCAPE for menu       ████│
│  ██                              ████│
│  ████████████████████████████████████│
└──────────────────────────────────────┘
```

The overlay uses a surface with alpha transparency (alpha=120), creating a darkening effect over the frozen game scene.

---

## 11. Design Patterns Used

This project employs several well-known software design patterns. Here's where and why each is used.

### State Pattern

**Where:** `GameState` enum + state-dependent methods in `Game`.

**How:** The Game class checks `self._state` to determine which handler, update, and render methods to call. Each state has its own behavior without complex if/else chains.

**Benefit:** Adding a new state (e.g., PAUSED) requires adding a new enum value and its corresponding handlers — no need to modify existing state logic.

### Factory Pattern

**Where:** `Spawner` class.

**How:** The spawner creates `Obstacle`, `Bird`, `Cloud`, and `Tree` instances without the Game class knowing the construction details (sprite selection, positioning, scaling).

**Benefit:** The Game class stays clean. Changing how obstacles are created (e.g., adding weighted spawn rates) only affects the `Spawner`.

### Observer/Event Pattern (Lightweight)

**Where:** Score checkpoint detection + audio trigger.

**How:** After the score changes, the Game class checks `score_manager.check_checkpoint()`. If true, it calls `audio.play_checkpoint()`. The ScoreManager doesn't know about audio — the Game class connects them.

**Benefit:** The scoring system and audio system are completely independent. They can be tested, modified, or replaced without affecting each other.

### Cache Pattern

**Where:** `AssetLoader`.

**How:** A dictionary stores loaded assets keyed by path and size. Repeated requests return the cached version without disk I/O.

**Benefit:** Loading a sprite set of 8 images once at startup instead of every frame makes the game run at 60 FPS instead of grinding to a halt.

### Composition over Inheritance

**Where:** The `Game` class composes systems (`AudioManager`, `CollisionSystem`, `ScoreManager`, `Spawner`, etc.) instead of inheriting from them.

**How:** Each system is a separate class instance owned by the Game. The Game delegates work to the appropriate system.

**Benefit:** Systems are independent, testable, and replaceable. The Game class orchestrates without being tightly coupled to any specific implementation.

---

## 12. Key Python & Pygame Concepts

This section explains Python and Pygame concepts used throughout the codebase for developers who may be new to them.

### 12.1 Python Concepts

#### Type Hints

```python
def save_score(self, player_name: str, score: int) -> None:
```

Type hints document expected types. They don't enforce anything at runtime but enable IDE autocompletion, error detection, and serve as documentation. This project uses them consistently for all public methods.

#### Pathlib

```python
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
```

`pathlib.Path` provides object-oriented filesystem paths. The `/` operator joins path components cross-platform:

```python
ASSETS_DIR = ROOT_DIR / "assets"  # Works on Windows AND Linux
```

Compare with the fragile alternative: `os.path.join(ROOT_DIR, "assets")`.

#### Enum

```python
class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
```

Enums create a fixed set of named constants. Using `GameState.MENU` instead of the string `"menu"` catches typos at development time (your IDE underlines undefined values) rather than at runtime.

#### Context Managers (with statement)

```python
# Not used explicitly in this codebase, but the Database class
# could benefit from it for connection management.
```

#### List Comprehension

```python
# Example from the codebase:
frames = [loader.load_image(f"{folder}/{prefix}-{i}.png", size) for i in range(1, count + 1)]
```

A concise way to create lists by transforming each element. Equivalent to a `for` loop that appends to an empty list, but more Pythonic and often faster.

#### The `__init__.py` File

Every directory under `code/` contains an `__init__.py` file. This tells Python the directory is a **package** that can be imported:

```python
from code.game import Game          # This only works because code/__init__.py exists
from code.core.config import FPS    # Works because code/core/__init__.py exists
```

The `__init__.py` files are empty in this project — they exist solely to enable imports.

### 12.2 Pygame Concepts

#### Surface

A `Surface` is Pygame's fundamental image type — a 2D array of pixels. The screen itself is a surface. Sprites are surfaces. Everything visual is a surface.

```python
screen = pygame.display.set_mode((800, 300))  # Creates the main surface
image = pygame.image.load("file.png")         # Loads an image as a surface
screen.blit(image, (x, y))                    # Draws one surface onto another
```

#### convert_alpha()

```python
image = pygame.image.load("file.png").convert_alpha()
```

Converts an image to the display's pixel format with alpha (transparency) support. Without this, Pygame does a format conversion **every time** the image is drawn, which is slow. With it, drawing is a fast memory copy.

**Rule of thumb:** Always call `convert_alpha()` after loading an image.

#### Sprite and Group

```python
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ...    # Required: the sprite's appearance
        self.rect = ...     # Required: position and size
        self.mask = ...     # Optional: pixel-perfect collision mask
```

`pygame.sprite.Sprite` provides:
- Automatic lifecycle management via `kill()` (removes from all groups).
- Standardized `update()` method called by groups.
- Built-in collision detection functions.

`pygame.sprite.Group` manages collections of sprites:  
```python
group = pygame.sprite.Group()
group.add(obstacle)        # Add a sprite
group.update(speed)        # Calls update() on every sprite
group.draw(screen)         # Draws every sprite to a surface
# Sprites that call self.kill() are automatically removed
```

#### Mask Collision

```python
mask = pygame.mask.from_surface(sprite.image)
collision = pygame.sprite.collide_mask(sprite_a, sprite_b)
```

A mask is a bitmap where each bit represents whether a pixel is opaque (1) or transparent (0). Two sprites collide only when their opaque pixels overlap in screen space. This is more accurate than rectangle collision for irregularly-shaped sprites.

#### Clock and FPS

```python
clock = pygame.time.Clock()
clock.tick(60)  # Limits the game loop to 60 iterations per second
```

Without `tick()`, the game loop would run as fast as possible, making the game unplayable on fast hardware and inconsistent across machines. The clock ensures consistent timing.

#### Event System

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            player.jump()
```

Pygame collects all input events (keyboard, mouse, window) into a queue. The game processes this queue once per frame. `KEYDOWN` fires once when a key is pressed. `pygame.key.get_pressed()` returns continuously-held keys.

---

## 13. Data Flow Diagrams

### Input → State Change Flow

```
Keyboard Event
      │
      ▼
 Game._handle_events()
      │
      ├── MENU State ──► Navigate options / Change state
      ├── NAME_SELECT ──► Type name / Select from list
      ├── PLAYING ──► Jump (set vel) / Duck (change anim) / Menu
      ├── GAME_OVER ──► Restart / Menu
      └── SCOREBOARD ──► Return to menu
```

### Frame Update Flow (PLAYING)

```
Game._update_playing()
      │
      ├── 1. Spawner.tick()
      │       └── Creates new Obstacle / Bird / Cloud / Tree
      │
      ├── 2. Difficulty Scaling
      │       ├── _speed += 0.1    (every 100 frames)
      │       └── _enemy_interval -= 0.5  (min 30)
      │
      ├── 3. Entity Updates
      │       ├── Ground.update(speed)           → scroll tiles
      │       ├── Clouds.update(speed * 0.3)     → slow parallax
      │       ├── Trees.update(speed * 0.5)      → mid parallax
      │       ├── Obstacles.update(speed)        → full speed
      │       ├── Birds.update(speed)            → full speed - 1
      │       └── Player.update(jump, duck)      → physics + animation
      │
      ├── 4. CollisionSystem.check()
      │       └── If collision → Player.die() + Game Over
      │
      └── 5. Scoring
              ├── Check each enemy: passed player? → Award points
              └── Check checkpoint → Play SFX
```

### Rendering Pipeline

```
Screen Fill (SKY_BLUE)
      │
      ▼
Cloud Group .draw()        ← Layer 1 (30% speed)
      │
      ▼
Tree Group .draw()         ← Layer 2 (50% speed)
      │
      ▼
Ground .draw()             ← Layer 3 (100% speed)
      │
      ▼
Obstacle Group .draw()     ← Layer 4 (100% speed)
      │
      ▼
Bird Group .draw()         ← Layer 5 (speed - 1)
      │
      ▼
Player .draw()             ← Layer 6 (fixed position)
      │
      ▼
HUD .render()              ← Layer 7 (overlay)
      │
      ▼
pygame.display.flip()      ← Push frame to screen
```

### Score Persistence Flow

```
Player dies
      │
      ▼
Game saves score ──► Database.save_score(name, score)
                          │
                          ├── get_or_create_player(name) → player_id
                          └── INSERT INTO scores (player_id, score)
                                     │
                                     ▼
                             samurai_scores.db  (SQLite file)
                                     │
                                     ▼ (later)
                             Database.get_top_scores(10)
                                     │
                                     ▼
                             Scoreboard Screen
```

---

## 14. Glossary

| Term | Definition |
|---|---|
| **Blit** | "Block Image Transfer" — Pygame's operation to draw one surface onto another. |
| **Cache** | A storage layer that keeps previously computed results for fast reuse. |
| **Collision Mask** | A pixel-level bitmap of a sprite's opaque pixels, used for accurate collision detection. |
| **Enum** | A Python class that defines a set of named constant values. |
| **FPS** | Frames Per Second — how many times the game loop executes per second (60 in this game). |
| **Game Loop** | The core loop of any game: process input → update state → render → repeat. |
| **Parallax** | A visual technique where layers scroll at different speeds to simulate depth. |
| **Rect** | A Pygame rectangle object that stores position (x, y) and size (width, height). |
| **Sprite** | A 2D image that can move and be drawn. In Pygame, a class with `image`, `rect`, and optionally `mask`. |
| **Sprite Group** | A Pygame container that manages a collection of sprites and provides batch operations (update, draw, collision). |
| **State Machine** | A design where an object can be in one of several states, with defined transitions between them. |
| **Surface** | Pygame's fundamental 2D pixel array. Everything visual (screen, images, text) is a surface. |
| **Type Hint** | Python annotation (e.g., `def func(x: int) -> str`) that documents expected types without runtime enforcement. |
| **Virtual Environment (.venv)** | An isolated Python installation that keeps project dependencies separate from the system Python. |
| **WAL (Write-Ahead Logging)** | An SQLite journaling mode that improves write performance and crash resilience. |
