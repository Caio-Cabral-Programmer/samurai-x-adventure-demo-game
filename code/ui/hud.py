"""In-game HUD rendering (score display)."""

import pygame

from ..core.config import SCREEN_WIDTH, WHITE, GOLD


class HUDRenderer:
    """Renders the score and high score during gameplay."""

    def __init__(self) -> None:
        self._font = pygame.font.Font(None, 24)

    def render(
        self, surface: pygame.Surface, score: int, high_score: int
    ) -> None:
        score_text = f"Score: {score:05d}"
        score_surf = self._font.render(score_text, True, WHITE)
        surface.blit(score_surf, (SCREEN_WIDTH - 140, 10))

        if high_score > 0:
            hi_text = f"HI: {high_score:05d}"
            hi_surf = self._font.render(hi_text, True, GOLD)
            surface.blit(hi_surf, (SCREEN_WIDTH - 260, 10))
