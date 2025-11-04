"""Module defining the Entity class."""

from abc import ABC, abstractmethod
from typing import Any

import pygame

from src.utils import GameConfig, get_hit_mask, pixel_collision


class Entity(ABC):
    """Entity class.

    Attributes:
        config: Game configuration.
        image: Image of the entity.
        x: X-coordinate of the entity.
        y: Y-coordinate of the entity.
        w: Width of the entity.
        h: Height of the entity.
        hit_mask: Hit mask of the entity.
    """

    def __init__(
        self,
        config: GameConfig,
        image: pygame.Surface | None = None,
        x: int = 0,
        y: int = 0,
        w: int | None = None,
        h: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the entity with configuration and positioning."""
        self.config = config
        self.x = x
        self.y = y
        if w or h:
            self.w = w or config.window.ratio * h
            self.h = h or w / config.window.ratio
            self.image = pygame.transform.scale(image, (self.w, self.h))
        else:
            self.image = image
            self.w = image.get_width() if image else 0
            self.h = image.get_height() if image else 0

        self.hit_mask = get_hit_mask(image) if image else None
        self.__dict__.update(kwargs)

    def update_image(self, image: pygame.Surface, w: int | None = None, h: int | None = None) -> None:
        """Update the image of the entity."""
        self.image = image
        self.hit_mask = get_hit_mask(image)
        self.w = w or (image.get_width() if image else 0)
        self.h = h or (image.get_height() if image else 0)

    @property
    def cx(self) -> float:
        """Returns the center x-coordinate of the entity."""
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        """Returns the center y-coordinate of the entity."""
        return self.y + self.h / 2

    @property
    def rect(self) -> pygame.Rect:
        """Returns the rect of the entity."""
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def collide(self, other: "Entity") -> bool:
        """Returns a boolean indicating whether the entity collides with another entity."""
        if not self.hit_mask or not other.hit_mask:
            return self.rect.colliderect(other.rect)
        return pixel_collision(self.rect, other.rect, self.hit_mask, other.hit_mask)

    @abstractmethod
    def tick(self) -> None:
        """Updates the entity."""
        # Update entity logic here, if any

    def render(self) -> None:
        """Draws the entity on the screen."""
        if self.image:
            self.config.screen.blit(self.image, self.rect)
        if self.config.debug:
            pygame.draw.rect(self.config.screen, (255, 0, 0), self.rect, 1)
            # write x and y at top of rect
            font = pygame.font.SysFont("Arial", 13, True)
            text = font.render(
                f"{self.x:.1f}, {self.y:.1f}, {self.w:.1f}, {self.h:.1f}",
                True,
                (255, 255, 255),
            )
            self.config.screen.blit(
                text,
                (
                    self.rect.x + self.rect.w / 2 - text.get_width() / 2,
                    self.rect.y - text.get_height(),
                ),
            )
