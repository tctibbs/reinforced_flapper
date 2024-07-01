"""Module for the Background class."""
from ..utils import GameConfig
from .entity import Entity


class Background(Entity):
    """Background entity.

    Attributes:
        config: Game configuration.
    """
    def __init__(self, config: GameConfig) -> None:
        super().__init__(
            config,
            config.images.background,
            0,
            0,
            config.window.width,
            config.window.height,
        )
