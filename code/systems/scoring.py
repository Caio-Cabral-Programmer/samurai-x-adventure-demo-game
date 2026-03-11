"""Score tracking system."""

from ..core.config import OBSTACLE_SCORE, BIRD_SCORE, CHECKPOINT_INTERVAL


class ScoreManager:
    """Tracks the current score and checkpoint milestones."""

    def __init__(self) -> None:
        self._score = 0
        self._last_checkpoint = 0

    @property
    def score(self) -> int:
        return self._score

    def add_obstacle_points(self) -> None:
        self._score += OBSTACLE_SCORE

    def add_bird_points(self) -> None:
        self._score += BIRD_SCORE

    def check_checkpoint(self) -> bool:
        """Return True if a new checkpoint milestone was reached."""
        current = self._score // CHECKPOINT_INTERVAL
        if current > self._last_checkpoint:
            self._last_checkpoint = current
            return True
        return False

    def reset(self) -> None:
        self._score = 0
        self._last_checkpoint = 0
