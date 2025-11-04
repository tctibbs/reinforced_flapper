"""Module for the floor entity."""

from src.entities.entity import Entity
from src.utils import GameConfig


class Floor(Entity):
    """Floor entity.

    Attributes:
        vel_x: Velocity of the floor.
        x_extra: Extra width of the floor.
    """

    def __init__(self, config: GameConfig) -> None:
        """Initialize the floor."""
        super().__init__(config, config.images.base, 0, config.window.vh)
        self.vel_x = 4
        self.x_extra = self.w - config.window.w

    def stop(self) -> None:
        """Stop the floor movement."""
        self.vel_x = 0

    def tick(self) -> None:
        """Update the floor position."""
        self.x = -((-self.x + self.vel_x) % self.x_extra)
