"""Module for the Background class."""

from src.entities.entity import Entity
from src.utils import GameConfig


class Background(Entity):
    """Background entity.

    Attributes:
        config: Game configuration.
    """

    def __init__(self, config: GameConfig) -> None:
        """Initialize the background."""
        super().__init__(
            config,
            config.images.background,
            0,
            0,
            config.window.width,
            config.window.height,
        )

    def tick(self) -> None:
        """Update the background."""
