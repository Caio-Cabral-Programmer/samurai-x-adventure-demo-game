"""Collision detection system."""

import pygame


class CollisionSystem:
    """Checks mask-based collisions between the player and enemy groups."""

    @staticmethod
    def check(player, obstacle_group, bird_group) -> bool:
        for sprite in obstacle_group:
            if pygame.sprite.collide_mask(player, sprite):
                return True
        for sprite in bird_group:
            if pygame.sprite.collide_mask(player, sprite):
                return True
        return False
