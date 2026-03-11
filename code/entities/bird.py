"""Flying bird enemy entity."""

import pygame

from ..assets.loader import AssetLoader
from ..core.config import BIRD_SIZE, BIRD_FRAME_COUNT


class Bird(pygame.sprite.Sprite):
    """An animated bird that flies across the screen."""

    def __init__(self, x: int, y: int, asset_loader: AssetLoader) -> None:
        super().__init__()

        self._frames = asset_loader.load_image_sequence(
            "bird", "bird", BIRD_FRAME_COUNT, BIRD_SIZE
        )
        self._index = 0
        self._counter = 0

        self.image = self._frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.scored = False

    def update(self, speed: float) -> None:
        self.rect.x -= int(speed)
        if self.rect.right <= 0:
            self.kill()

        self._counter += 1
        if self._counter >= 6:
            self._index = (self._index + 1) % len(self._frames)
            self.image = self._frames[self._index]
            self._counter = 0

        self.mask = pygame.mask.from_surface(self.image)
