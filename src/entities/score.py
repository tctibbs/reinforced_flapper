"""Module for the Score entity."""

import pygame

from ..utils import GameConfig
from .entity import Entity


class Score(Entity):
    """Score entity.

    Attributes:
        y: Y-coordinate of the score.
        score: Current score.
    """

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.y = self.config.window.height * 0.1
        self.score = 0

    def reset(self) -> None:
        """Resets the score to zero."""
        self.score = 0

    def add(self) -> None:
        """Adds one to the score."""
        self.score += 1
        self.config.sounds.point.play()

    @property
    def rect(self) -> pygame.Rect:
        """Returns the rect of the score."""
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.numbers[digit] for digit in score_digits]
        w = sum(image.get_width() for image in images)
        x = (self.config.window.width - w) / 2
        h = max(image.get_height() for image in images)
        return pygame.Rect(x, self.y, w, h)

    def tick(self) -> None:
        """Updates the score."""
        pass

    def render(self) -> None:
        """displays score in center of screen"""
        score_digits = [int(x) for x in list(str(self.score))]
        images = [self.config.images.numbers[digit] for digit in score_digits]
        digits_width = sum(image.get_width() for image in images)
        x_offset = (self.config.window.width - digits_width) / 2

        for image in images:
            self.config.screen.blit(image, (x_offset, self.y))
            x_offset += image.get_width()
