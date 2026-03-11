"""Centralized asset loading and caching service."""

from pathlib import Path
from typing import Optional

import pygame


class AssetLoader:
    """Loads and caches images and sounds from the assets directory."""

    def __init__(self, assets_dir: Path) -> None:
        self._assets_dir = assets_dir
        self._image_cache: dict[str, pygame.Surface] = {}
        self._sound_cache: dict[str, pygame.mixer.Sound] = {}

    def load_image(
        self,
        relative_path: str,
        size: Optional[tuple[int, int]] = None,
    ) -> pygame.Surface:
        cache_key = f"{relative_path}_{size}"
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]

        full_path = self._assets_dir / relative_path
        image = pygame.image.load(str(full_path)).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)

        self._image_cache[cache_key] = image
        return image

    def load_image_sequence(
        self,
        folder: str,
        prefix: str,
        count: int,
        size: Optional[tuple[int, int]] = None,
    ) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []
        for i in range(1, count + 1):
            path = f"{folder}/{prefix}-{i}.png"
            frames.append(self.load_image(path, size))
        return frames

    def load_sound(self, relative_path: str) -> pygame.mixer.Sound:
        if relative_path in self._sound_cache:
            return self._sound_cache[relative_path]

        full_path = self._assets_dir / relative_path
        sound = pygame.mixer.Sound(str(full_path))
        self._sound_cache[relative_path] = sound
        return sound

    def get_music_path(self, relative_path: str) -> str:
        return str(self._assets_dir / relative_path)
