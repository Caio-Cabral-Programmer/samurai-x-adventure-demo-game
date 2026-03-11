"""Scrolling ground entity."""

import pygame

from ..assets.loader import AssetLoader


class Ground:
    """Infinitely scrolling ground using two tiled copies of the ground image."""

    def __init__(self, asset_loader: AssetLoader, y: int) -> None:
        self._image = asset_loader.load_image("scenario/scenario-ground.png")
        self._width = self._image.get_width()
        self._x1 = 0
        self._x2 = self._width
        self._y = y

    def update(self, speed: float) -> None:
        self._x1 -= speed
        self._x2 -= speed

        if self._x1 <= -self._width:
            self._x1 += 2 * self._width
        if self._x2 <= -self._width:
            self._x2 += 2 * self._width

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._image, (int(self._x1), self._y))
        surface.blit(self._image, (int(self._x2), self._y))
