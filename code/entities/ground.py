"""Scrolling ground entity."""

import pygame

from ..assets.loader import AssetLoader


class Ground:
    """Infinitely scrolling ground using tiled copies of the ground image."""

    def __init__(self, asset_loader: AssetLoader, y: int) -> None:
        self._image = asset_loader.load_image("scenario/scenario-ground.png")
        self._width = self._image.get_width()
        self._scroll_x = 0.0
        self._y = y

    def update(self, speed: float) -> None:
        # Keep a continuous modular offset to prevent seams/flicker.
        self._scroll_x = (self._scroll_x + speed) % self._width

    def draw(self, surface: pygame.Surface) -> None:
        x_start = -int(self._scroll_x)
        tile_count = surface.get_width() // self._width + 3
        for i in range(tile_count):
            surface.blit(self._image, (x_start + i * self._width, self._y))
