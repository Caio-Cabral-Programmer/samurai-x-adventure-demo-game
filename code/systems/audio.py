"""Audio management system for music and sound effects."""

import pygame

from ..assets.loader import AssetLoader
from ..core.config import MENU_MUSIC_VOLUME, GAME_MUSIC_VOLUME


class AudioManager:
    """Handles background music and sound effect playback."""

    def __init__(self, asset_loader: AssetLoader) -> None:
        self._jump_sfx = asset_loader.load_sound("sounds/jump-song.wav")
        self._die_sfx = asset_loader.load_sound("sounds/die-song.wav")
        self._checkpoint_sfx = asset_loader.load_sound("sounds/checkPoint-song.wav")

        self._menu_music_path = asset_loader.get_music_path(
            "sounds/main-menu-song.mp3"
        )
        self._game_music_path = asset_loader.get_music_path("sounds/game-music.mp3")
        self._current_music: str = ""

    def play_menu_music(self) -> None:
        if self._current_music != self._menu_music_path:
            pygame.mixer.music.load(self._menu_music_path)
            pygame.mixer.music.set_volume(MENU_MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
            self._current_music = self._menu_music_path

    def play_game_music(self) -> None:
        if self._current_music != self._game_music_path:
            pygame.mixer.music.load(self._game_music_path)
            pygame.mixer.music.set_volume(GAME_MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
            self._current_music = self._game_music_path

    def stop_music(self) -> None:
        pygame.mixer.music.stop()
        self._current_music = ""

    def play_jump(self) -> None:
        self._jump_sfx.play()

    def play_die(self) -> None:
        self._die_sfx.play()

    def play_checkpoint(self) -> None:
        self._checkpoint_sfx.play()
