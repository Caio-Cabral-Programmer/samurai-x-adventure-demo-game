"""Game over overlay rendering."""

import pygame

from ..core.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD, GRAY


class GameOverRenderer:
    """Renders the game over overlay with score and restart instructions."""

    def __init__(self) -> None:
        self._font_large = pygame.font.Font(None, 48)
        self._font_medium = pygame.font.Font(None, 28)
        self._font_small = pygame.font.Font(None, 22)

        self._overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        self._overlay.fill((0, 0, 0, 120))

    def render(self, surface: pygame.Surface, score: int) -> None:
        surface.blit(self._overlay, (0, 0))

        # Game Over title
        title = self._font_large.render("GAME OVER", True, GOLD)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        # Final score
        score_text = self._font_medium.render(
            f"Score: {score:05d}", True, WHITE
        )
        surface.blit(
            score_text,
            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 120),
        )

        # Instructions
        restart = self._font_small.render(
            "Press SPACE to restart", True, GRAY
        )
        surface.blit(
            restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 180)
        )

        menu = self._font_small.render(
            "Press ESCAPE for menu", True, GRAY
        )
        surface.blit(
            menu, (SCREEN_WIDTH // 2 - menu.get_width() // 2, 200)
        )
