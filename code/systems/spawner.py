"""Entity spawning system."""

import random

from ..assets.loader import AssetLoader
from ..core.config import (
    SCREEN_WIDTH,
    CLOUD_Y_RANGE,
    TREE_BASE_Y,
    BIRD_Y_OPTIONS,
    CLOUD_SPAWN_INTERVAL,
    TREE_SPAWN_INTERVAL,
    OBSTACLE_COUNT,
)
from ..entities.obstacle import Obstacle
from ..entities.bird import Bird
from ..entities.cloud import Cloud
from ..entities.tree import Tree


class Spawner:
    """Spawns enemies and environment decorations based on frame timing."""

    def __init__(self, asset_loader: AssetLoader) -> None:
        self._asset_loader = asset_loader

    def tick(
        self,
        frame: int,
        enemy_interval: float,
        obstacle_group,
        bird_group,
        cloud_group,
        tree_group,
    ) -> None:
        interval = max(1, int(enemy_interval))
        if frame % interval == 0:
            self._spawn_enemy(obstacle_group, bird_group)

        if frame % CLOUD_SPAWN_INTERVAL == 0:
            self._spawn_cloud(cloud_group)

        if frame % TREE_SPAWN_INTERVAL == 0:
            self._spawn_tree(tree_group)

    def _spawn_enemy(self, obstacle_group, bird_group) -> None:
        if random.randint(1, 10) == 5:
            y = random.choice(BIRD_Y_OPTIONS)
            bird = Bird(SCREEN_WIDTH, y, self._asset_loader)
            bird_group.add(bird)
        else:
            obstacle_type = random.randint(1, OBSTACLE_COUNT)
            obstacle = Obstacle(obstacle_type, self._asset_loader)
            obstacle_group.add(obstacle)

    def _spawn_cloud(self, cloud_group) -> None:
        x = SCREEN_WIDTH + random.randint(0, 100)
        y = random.randint(*CLOUD_Y_RANGE)
        cloud = Cloud(x, y, self._asset_loader)
        cloud_group.add(cloud)

    def _spawn_tree(self, tree_group) -> None:
        x = SCREEN_WIDTH + random.randint(0, 50)
        tree = Tree(x, TREE_BASE_Y, self._asset_loader)
        tree_group.add(tree)
