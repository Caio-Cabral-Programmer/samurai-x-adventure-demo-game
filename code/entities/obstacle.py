"""Ground obstacle entity."""

import pygame

from ..assets.loader import AssetLoader
from ..core.config import SCREEN_WIDTH, OBSTACLE_BOTTOM_Y, OBSTACLE_SCALE


class Obstacle(pygame.sprite.Sprite):
    """A ground-level obstacle that scrolls left."""

    def __init__(self, obstacle_type: int, asset_loader: AssetLoader) -> None:
        super().__init__()

        img = asset_loader.load_image(f"obstacles/obstacle-{obstacle_type}.png")
        w, h = img.get_size()
        self.image = pygame.transform.scale(
            img, (int(w * OBSTACLE_SCALE), int(h * OBSTACLE_SCALE))
        )
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + 10
        self.rect.bottom = OBSTACLE_BOTTOM_Y
        self.mask = pygame.mask.from_surface(self.image)
        self.scored = False

    def update(self, speed: float) -> None:
        self.rect.x -= int(speed)
        if self.rect.right <= 0:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)
