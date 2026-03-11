"""Background tree entity."""

import random

import pygame

from ..assets.loader import AssetLoader
from ..core.config import TREE_COUNT


class Tree(pygame.sprite.Sprite):
    """A midground tree that scrolls for parallax depth between clouds and ground."""

    def __init__(self, x: int, y_bottom: int, asset_loader: AssetLoader) -> None:
        super().__init__()

        tree_type = random.randint(1, TREE_COUNT)
        self.image = asset_loader.load_image(
            f"scenario/scenario-tree-{tree_type}.png"
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y_bottom

    def update(self, speed: float) -> None:
        self.rect.x -= max(1, int(speed))
        if self.rect.right <= 0:
            self.kill()
