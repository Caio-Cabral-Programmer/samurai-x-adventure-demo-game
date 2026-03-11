"""Player (Samurai) entity with run, jump, duck, and death animations."""

import pygame

from ..assets.loader import AssetLoader
from ..core.config import (
    PLAYER_X,
    PLAYER_BASE_Y,
    PLAYER_RUN_SIZE,
    PLAYER_DUCK_SIZE,
    PLAYER_JUMP_HEIGHT,
    PLAYER_GRAVITY,
    PLAYER_RUN_FRAME_COUNT,
    PLAYER_DUCK_FRAME_COUNT,
    PLAYER_DEAD_FRAME_COUNT,
    PLAYER_JUMP_FRAME_COUNT,
    RUN_ANIM_SPEED,
    DUCK_ANIM_SPEED,
    DEAD_ANIM_SPEED,
    JUMP_ANIM_SPEED,
)


class Player:
    """Samurai player character with state-based animation and physics."""

    def __init__(self, asset_loader: AssetLoader) -> None:
        self._x = PLAYER_X
        self._base_y = PLAYER_BASE_Y

        # Load animation frames
        self._run_frames = asset_loader.load_image_sequence(
            "samurai-run", "samurai-run", PLAYER_RUN_FRAME_COUNT, PLAYER_RUN_SIZE
        )
        self._duck_frames = asset_loader.load_image_sequence(
            "samurai-bent-down",
            "samurai-bent-down",
            PLAYER_DUCK_FRAME_COUNT,
            PLAYER_DUCK_SIZE,
        )
        self._dead_frames = asset_loader.load_image_sequence(
            "samurai-dead", "samurai-dead", PLAYER_DEAD_FRAME_COUNT
        )
        self._jump_frames = [
            pygame.transform.scale(frame, PLAYER_RUN_SIZE)
            for frame in asset_loader.load_image_sequence(
                "samurai-jump", "samurai-jump", PLAYER_JUMP_FRAME_COUNT
            )
        ]

        self._vel: float = 0
        self._is_jumping = False
        self.alive = True

        self._anim_index = 0
        self._anim_counter = 0
        self._death_anim_done = False

        self.image = self._run_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = self._x
        self.rect.bottom = self._base_y
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self) -> None:
        self._vel = 0
        self._is_jumping = False
        self.alive = True
        self._anim_index = 0
        self._anim_counter = 0
        self._death_anim_done = False

        self.image = self._run_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = self._x
        self.rect.bottom = self._base_y
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def is_death_animation_done(self) -> bool:
        return self._death_anim_done

    def die(self) -> None:
        self.alive = False
        self._anim_index = 0
        self._anim_counter = 0
        self._death_anim_done = False

    def update(self, jump: bool, duck: bool) -> None:
        if self.alive:
            self._update_alive(jump, duck)
        else:
            self._update_dead()

    def _update_alive(self, jump: bool, duck: bool) -> None:
        # Jumping physics
        if not self._is_jumping and jump:
            self._vel = -PLAYER_JUMP_HEIGHT
            self._is_jumping = True
            self._anim_index = 0
            self._anim_counter = 0

        self._vel += PLAYER_GRAVITY
        if self._vel >= PLAYER_JUMP_HEIGHT:
            self._vel = PLAYER_JUMP_HEIGHT

        self.rect.y += int(self._vel)
        if self.rect.bottom > self._base_y:
            self.rect.bottom = self._base_y
            self._is_jumping = False

        # Animation selection — preserve Y position during jump
        current_bottom = self.rect.bottom
        if duck and not self._is_jumping:
            self._animate(self._duck_frames, DUCK_ANIM_SPEED)
        elif self._is_jumping:
            self._animate(self._jump_frames, JUMP_ANIM_SPEED)
            self.rect.bottom = current_bottom
        else:
            self._animate(self._run_frames, RUN_ANIM_SPEED)

        self.mask = pygame.mask.from_surface(self.image)

    def _update_dead(self) -> None:
        if self._death_anim_done:
            return

        # Fall to ground if airborne
        if self.rect.bottom < self._base_y:
            self._vel += PLAYER_GRAVITY
            self.rect.y += int(self._vel)
            if self.rect.bottom >= self._base_y:
                self.rect.bottom = self._base_y

        self._anim_counter += 1
        if self._anim_counter >= DEAD_ANIM_SPEED:
            self._anim_counter = 0
            if self._anim_index < len(self._dead_frames) - 1:
                self._anim_index += 1
            else:
                self._death_anim_done = True

        self.image = self._dead_frames[self._anim_index]
        self.rect = self.image.get_rect()
        self.rect.x = self._x
        self.rect.bottom = self._base_y

    def _animate(
        self, frames: list[pygame.Surface], speed: int
    ) -> None:
        self._anim_counter += 1
        if self._anim_counter >= speed:
            self._anim_index = (self._anim_index + 1) % len(frames)
            self.image = frames[self._anim_index]
            self.rect = self.image.get_rect()
            self.rect.x = self._x
            self.rect.bottom = self._base_y
            self._anim_counter = 0

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
