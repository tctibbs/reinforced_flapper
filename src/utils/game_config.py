"""Game configuration."""

import os

import pygame

from .images import Images
from .sounds import Sounds
from .window import Window


class GameConfig:
    """Game configuration.

    Attributes:
        screen: Pygame screen.
        clock: Pygame clock.
        fps: Frames per second.
        window: Game window.
        images: Game images.
        sounds: Game sounds.
        debug: Debug mode.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        fps: int,
        window: Window,
        images: Images,
        sounds: Sounds,
    ) -> None:
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.window = window
        self.images = images
        self.sounds = sounds
        self.debug = os.environ.get("DEBUG", False)

    def tick(self) -> None:
        """Tick the game clock."""
        self.clock.tick(self.fps)
