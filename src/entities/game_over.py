"""Module for the GameOver entity."""

from ..utils import GameConfig
from .entity import Entity


class GameOver(Entity):
    """Game over entity.

    Attributes:
        config: Game configuration.
    """

    def __init__(self, config: GameConfig) -> None:
        super().__init__(
            config=config,
            image=config.images.game_over,
            x=(config.window.width - config.images.game_over.get_width()) // 2,
            y=int(config.window.height * 0.2),
        )

    def tick(self) -> None:
        """Update the game over screen."""
        pass
