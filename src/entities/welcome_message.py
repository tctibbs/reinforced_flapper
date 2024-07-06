"""Module for the welcome message entity."""

from ..utils import GameConfig
from .entity import Entity


class WelcomeMessage(Entity):
    """Welcome message entity.

    Attributes:
        config: Game configuration.
    """

    def __init__(self, config: GameConfig) -> None:
        image = config.images.welcome_message
        super().__init__(
            config=config,
            image=image,
            x=(config.window.width - image.get_width()) // 2,
            y=int(config.window.height * 0.12),
        )

    def tick(self) -> None:
        """Update the welcome message."""
        pass
