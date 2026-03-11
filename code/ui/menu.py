"""Main menu, name selection, and scoreboard rendering."""

import pygame

from ..assets.loader import AssetLoader
from ..core.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    GOLD,
    GRAY,
    OBSTACLE_SCORE,
    BIRD_SCORE,
    CREATED_BY_TEXT,
)


class MenuRenderer:
    """Renders the main menu, player name selection, and scoreboard screens."""

    MENU_OPTIONS = ["Start Game", "View Scores", "Exit"]

    def __init__(self, asset_loader: AssetLoader) -> None:
        self._bg = asset_loader.load_image(
            "scenario/scenario-forest-complete.png", (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self._overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        self._overlay.fill((0, 0, 0, 150))

        self._font_title = pygame.font.Font(None, 52)
        self._font_option = pygame.font.Font(None, 30)
        self._font_small = pygame.font.Font(None, 22)
        self._font_input = pygame.font.Font(None, 28)

    def render_menu(self, surface: pygame.Surface, selection: int) -> None:
        surface.blit(self._bg, (0, 0))
        surface.blit(self._overlay, (0, 0))

        # Title
        title = self._font_title.render("Samurai X", True, GOLD)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 18))

        # Menu options
        for i, option in enumerate(self.MENU_OPTIONS):
            prefix = "> " if i == selection else "  "
            color = GOLD if i == selection else WHITE
            text = self._font_option.render(f"{prefix}{option}", True, color)
            surface.blit(text, (SCREEN_WIDTH // 2 - 80, 80 + i * 35))

        # Controls (left column)
        controls = [
            "Controls:",
            "  Space / Up Arrow - Jump",
            "  Down Arrow - Duck",
            "  Space on game over - Restart",
            "  Escape / Q - Quit",
        ]
        y = 190
        for line in controls:
            text = self._font_small.render(line, True, GRAY)
            surface.blit(text, (30, y))
            y += 18

        # Scoring info (right column)
        scoring = [
            "Scoring:",
            f"  Pass an obstacle: +{OBSTACLE_SCORE} pts",
            f"  Pass a bird: +{BIRD_SCORE} pts",
        ]
        y = 190
        for line in scoring:
            text = self._font_small.render(line, True, GRAY)
            surface.blit(text, (SCREEN_WIDTH - 260, y))
            y += 18

        credit = self._font_small.render(CREATED_BY_TEXT, True, GRAY)
        surface.blit(
            credit,
            (SCREEN_WIDTH // 2 - credit.get_width() // 2, SCREEN_HEIGHT - 22),
        )

    def render_name_select(
        self,
        surface: pygame.Surface,
        name_input: str,
        existing_names: list[str],
        selected_index: int,
    ) -> None:
        surface.blit(self._bg, (0, 0))
        surface.blit(self._overlay, (0, 0))

        # Title
        title = self._font_option.render("Choose Your Name", True, GOLD)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        # Input field label
        label = self._font_small.render("Type a new name:", True, GRAY)
        surface.blit(label, (SCREEN_WIDTH // 2 - 150, 60))

        # Input field box
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 80, 300, 32)
        pygame.draw.rect(surface, WHITE, input_rect, 2)

        display_text = name_input + "|"
        input_surface = self._font_input.render(display_text, True, WHITE)
        surface.blit(input_surface, (input_rect.x + 8, input_rect.y + 5))

        # Existing players
        if existing_names:
            label2 = self._font_small.render(
                "Or select with Up/Down arrows:", True, GRAY
            )
            surface.blit(label2, (SCREEN_WIDTH // 2 - 150, 125))

            max_visible = 6
            start = max(0, selected_index - max_visible + 1)
            for i, name in enumerate(existing_names[start : start + max_visible]):
                actual_index = start + i
                prefix = "> " if actual_index == selected_index else "  "
                color = GOLD if actual_index == selected_index else WHITE
                text = self._font_small.render(f"{prefix}{name}", True, color)
                surface.blit(text, (SCREEN_WIDTH // 2 - 140, 148 + i * 20))

        # Instructions
        instr = self._font_small.render(
            "Press ENTER to confirm  |  Press ESCAPE to go back", True, GRAY
        )
        surface.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, 275))

    def render_scoreboard(
        self, surface: pygame.Surface, scores: list
    ) -> None:
        surface.blit(self._bg, (0, 0))
        surface.blit(self._overlay, (0, 0))

        # Title
        title = self._font_title.render("Top Scores", True, GOLD)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 15))

        if not scores:
            no_scores = self._font_option.render("No scores yet!", True, WHITE)
            surface.blit(
                no_scores,
                (SCREEN_WIDTH // 2 - no_scores.get_width() // 2, 120),
            )
        else:
            # Header
            header = self._font_small.render(
                f"{'Rank':<6}{'Player':<18}{'Score':<10}{'Date'}", True, GOLD
            )
            surface.blit(header, (120, 55))

            for i, (name, score, date) in enumerate(scores):
                date_str = str(date)[:10] if date else ""
                line = f"{i + 1:<6}{name:<18}{score:<10}{date_str}"
                color = GOLD if i == 0 else WHITE
                text = self._font_small.render(line, True, color)
                surface.blit(text, (120, 78 + i * 22))

        # Instructions
        instr = self._font_small.render("Press any key to go back", True, GRAY)
        surface.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, 275))
