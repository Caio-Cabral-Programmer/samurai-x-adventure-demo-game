# Samurai X

<p align='center'>
  <img src='assets\app-1.png' width=620 height=218>
</p>

<p align='center'>
  <img src='assets\app-2.png' width=620 height=218>
</p>

<p align='center'>
  <img src='assets\app-3.png' width=620 height=218>
</p>

## About the Game

**Samurai X** is a 2D endless-runner game built with Python and Pygame. You play as a samurai running through a forest, dodging obstacles on the ground and birds in the sky. The game gets progressively harder as your score increases — enemies spawn faster and the world scrolls quicker.

### Key Features

- **Endless runner gameplay** with increasing difficulty over time.
- **Pixel-perfect collision detection** using sprite masks.
- **Parallax scrolling** with multiple layers (clouds, trees, ground) for depth.
- **Persistent scoreboard** — player names and scores are saved to a local SQLite database.
- **Multiple animations** — the samurai runs, jumps, ducks, and has a death animation.
- **14 different obstacle types** and **6 bird animation frames** for visual variety.
- **Dynamic music and sound effects** — separate tracks for menu and gameplay, plus SFX for jumps, death, and score milestones.

---

## How to Play

### Objective

Run as far as you can! Dodge ground obstacles and flying birds to survive and earn the highest score.

### Scoring

| Event | Points |
|---|---|
| Pass an obstacle | +10 |
| Pass a bird | +20 |

A checkpoint sound plays every 100 points.

### Controls

| Key | Action |
|---|---|
| **Space** or **Up Arrow** | Jump |
| **Down Arrow** | Duck |
| **Space** (on Game Over) | Restart the game |
| **Escape** or **Q** | Return to menu / Quit |
| **Up / Down Arrows** | Navigate menus |
| **Enter** | Confirm selection |
| **Backspace** | Delete character (name input) |

### Game Flow

1. **Main Menu** — Choose "Start Game", "View Scores", or "Exit".
2. **Name Selection** — Type a new name or select from previously used names.
3. **Gameplay** — Run, jump, and duck to avoid enemies. Score increases as enemies pass behind you.
4. **Game Over** — A death animation plays, then your score is saved. Press Space to play again or Escape to return to the menu.
5. **Scoreboard** — View the top 10 scores of all time.

---

## Technical Setup

### Prerequisites

- **Python 3.10+** (tested with Python 3.13.5)
- **pip** (Python package manager, included with Python)
- **Git** (optional, for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/Caio-Cabral-Programmer/samurai-x-adventure-demo-game.git
cd samurai-x-adventure-demo-game
```

### 2. Create a Virtual Environment

Using a virtual environment (`.venv`) keeps project dependencies isolated from your system Python.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> If you see an execution policy error, run this first (for the current session only):
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\.venv\Scripts\Activate.ps1
> ```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When the virtual environment is active, you will see `(.venv)` at the beginning of your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

The only dependency is `pygame==2.6.1`.

### 4. Run the Game

```bash
python main.py
```

### 5. Deactivate the Virtual Environment

When you are done:

```bash
deactivate
```

---

## Building a Standalone Executable (.exe)

You can package the game into a single `.exe` file so others can play it without installing Python.

### Using PyInstaller

**1. Install PyInstaller** (inside your virtual environment):

```bash
pip install pyinstaller
```

**2. Build the executable:**

```bash
pyinstaller --onefile --noconsole --add-data "assets;assets" --name "SamuraiX" main.py
```

| Flag | Purpose |
|---|---|
| `--onefile` | Packages everything into a single `.exe` file |
| `--noconsole` | Hides the console window (game-only window) |
| `--add-data "assets;assets"` | Includes the `assets/` folder with images and sounds |
| `--name "SamuraiX"` | Sets the name of the output executable |

> **Note for macOS/Linux:** Replace the semicolon `;` with a colon `:` in `--add-data`:
> ```bash
> pyinstaller --onefile --noconsole --add-data "assets:assets" --name "SamuraiX" main.py
> ```

**3. Find the executable:**

The built file will be in the `dist/` folder:

```
dist/
  SamuraiX.exe
```

**4. Distribute:**

Send the `SamuraiX.exe` file to anyone — they do not need Python or Pygame installed. The SQLite database (`samurai_scores.db`) will be created automatically on the first run.

> **Important:** If the game uses `pathlib.Path` or relative paths for assets, PyInstaller may require adjusting the base path at runtime. If you encounter "file not found" errors when running the `.exe`, you may need to update `config.py` to detect the PyInstaller bundle path:
>
> ```python
> import sys
> from pathlib import Path
>
> if getattr(sys, 'frozen', False):
>     ROOT_DIR = Path(sys._MEIPASS)
> else:
>     ROOT_DIR = Path(__file__).resolve().parent.parent.parent
> ```

---

## Project Structure

```
main.py                    # Entry point (minimal)
requirements.txt           # Python dependencies
code/
  game.py                  # Main Game class (state machine, loop, rendering)
  core/
    config.py              # All constants, paths, screen/entity settings
    database.py            # SQLite database for player scores
  assets/
    loader.py              # Centralized image/sound loading with caching
  entities/
    player.py              # Player (Samurai) — run/jump/duck/death
    obstacle.py            # Ground-level obstacles
    bird.py                # Flying bird enemies
    ground.py              # Scrolling ground
    cloud.py               # Background clouds (parallax)
    tree.py                # Midground trees (parallax)
  systems/
    audio.py               # Music and SFX management
    collision.py           # Mask-based collision detection
    scoring.py             # Score tracking with milestones
    spawner.py             # Entity spawning with difficulty scaling
  ui/
    menu.py                # Main menu, name selection, scoreboard
    hud.py                 # In-game score display
    game_over.py           # Game over overlay
assets/                    # Images and sounds
docs/                      # Documentation
```

For a detailed explanation of the architecture, design patterns, and code, see [docs/PROJECT_ARCHITECTURE.md](docs/PROJECT_ARCHITECTURE.md).

---

## License

This project is for educational and demonstration purposes.