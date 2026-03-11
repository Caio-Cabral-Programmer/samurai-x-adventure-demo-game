"""Background cloud entity."""

import random

import pygame

from ..assets.loader import AssetLoader
from ..core.config import CLOUD_SIZE, CLOUD_COUNT


class Cloud(pygame.sprite.Sprite):
    """A background cloud that scrolls slowly for parallax effect."""

    def __init__(self, x: int, y: int, asset_loader: AssetLoader) -> None:
        super().__init__()

        cloud_type = random.randint(1, CLOUD_COUNT)
        self.image = asset_loader.load_image(
            f"scenario/scenario-cloud-{cloud_type}.png", CLOUD_SIZE
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed: float) -> None:
        self.rect.x -= max(1, int(speed))
        if self.rect.right <= 0:
            self.kill()
