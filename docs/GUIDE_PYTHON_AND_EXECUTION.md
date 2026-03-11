# Python Environment and Execution Guide for Samurai X Adventure

## 1. Quick Project Overview

This project is a 2D endless-runner game built with Pygame.

- Entry point: main.py
- Main source code: code/
- Visual and audio assets: assets/
- Main dependency: pygame

Important: run commands from the repository root folder (samurai-x-adventure-demo-game), so relative asset paths resolve correctly.

## 2. Recommended Python Version

Current verified environment:

- python --version -> Python 3.13.5
- py --version -> Python 3.13.5
- Active executable -> C:\Python313\python.exe

Also validated:

- pip is available and working
- pygame 2.6.1 is installed and imports correctly

Should you upgrade Python now?

Short answer: no, not required for this project.

Reasons:

- The game already runs correctly on Python 3.13.5.
- pygame works in the current environment.
- Unnecessary upgrades may introduce avoidable incompatibilities.

## 3. venv vs .venv (Professional Convention)

Use .venv at the repository root.

Why .venv is the standard in most Python teams:

- Common and recognizable convention
- Hidden directory by default
- Easy to ignore in Git
- Well-supported by VS Code interpreter detection

Summary:

- venv and .venv are technically equivalent
- .venv is the preferred professional naming convention

## 4. Setup and Run (Windows + PowerShell)

From the project root:

```powershell
python -m venv .venv
```

Activate virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, allow it for the current session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the game:

```powershell
python main.py
```

Deactivate environment when done:

```powershell
deactivate
```

## 5. Setup and Run (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
deactivate
```

## 6. Recommended .gitignore Entries

Ensure your virtual environment and Python cache files are not committed:

```gitignore
.venv/
__pycache__/
*.pyc
samurai_scores.db
```

## 7. Useful Diagnostic Commands

```powershell
python --version
py --version
python -m pip --version
python -c "import pygame; print(pygame.__version__)"
python -c "import sqlite3; print('sqlite ok')"
```

## 8. Build an Executable (.exe) for Distribution

You can package the game for users without Python installed.

Install PyInstaller in your active .venv:

```powershell
python -m pip install pyinstaller
```

Build command (Windows):

```powershell
pyinstaller --onefile --noconsole --add-data "assets;assets" --name "SamuraiXAdventure" main.py
```

Output location:

- dist/SamuraiXAdventure.exe

Flag summary:

- --onefile: create a single executable
- --noconsole: hide terminal window for a GUI game
- --add-data "assets;assets": include game assets in the package
- --name "SamuraiXAdventure": set executable name

Notes:

- On macOS/Linux, use a colon in add-data: --add-data "assets:assets"
- If the executable cannot find assets, update path resolution in code/core/config.py for frozen mode (sys._MEIPASS)

## 9. Current Technical Reality of This Repository

- objects.py exists only as a legacy placeholder and is not used by the running game.
- Active architecture is package-based under code/.
- main.py is intentionally minimal and only starts Game().
- requirements.txt currently pins pygame==2.6.1.

## 10. Final Checklist

Before running or sharing the game, verify this sequence:

1. Python is installed and recognized
2. .venv is created and activated
3. Dependencies installed from requirements.txt
4. Game runs with python main.py
5. Optional: executable created with PyInstaller
