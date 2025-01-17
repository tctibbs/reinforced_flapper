"""Module for pipe entities."""

import random
from typing import List

from ..utils import GameConfig
from .entity import Entity


class Pipe(Entity):
    """Pipe entity.

    Attributes:
        vel_x: Velocity of the pipe.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vel_x = -5

    def tick(self) -> None:
        """Update the pipe."""
        self.x += self.vel_x

    def render(self) -> None:
        """Render the pipe."""
        return super().render()


class Pipes(Entity):
    """Pipes entity.

    Attributes:
        pipe_gap: Gap between the pipes.
        top: Top of the screen.
        bottom: Bottom of the screen.
        upper: List of upper pipes.
        lower: List of lower pipes.
    """

    upper: List[Pipe]
    lower: List[Pipe]

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.pipe_gap = 120
        self.top = 0
        self.bottom = self.config.window.viewport_height
        self.upper = []
        self.lower = []
        self.spawn_initial_pipes()

    def tick(self) -> None:
        """Update the pipes."""
        if self.can_spawn_pipes():
            self.spawn_new_pipes()
        self.remove_old_pipes()

        for up_pipe, low_pipe in zip(self.upper, self.lower):
            up_pipe.tick()
            low_pipe.tick()

    def stop(self) -> None:
        """Stop the pipes."""
        for pipe in self.upper + self.lower:
            pipe.vel_x = 0

    def can_spawn_pipes(self) -> bool:
        """Check if new pipes can be spawned."""
        last = self.upper[-1]
        if not last:
            return True

        return self.config.window.width - (last.x + last.w) > last.w * 2.5

    def spawn_new_pipes(self) -> None:
        """Spawn new pipes."""
        # add new pipe when first pipe is about to touch left of screen
        upper, lower = self.make_random_pipes()
        self.upper.append(upper)
        self.lower.append(lower)

    def remove_old_pipes(self) -> None:
        """Remove old pipes."""
        # remove first pipe if its out of the screen
        for pipe in self.upper:
            if pipe.x < -pipe.w:
                self.upper.remove(pipe)

        for pipe in self.lower:
            if pipe.x < -pipe.w:
                self.lower.remove(pipe)

    def spawn_initial_pipes(self) -> None:
        """Spawn initial pipes."""
        upper_1, lower_1 = self.make_random_pipes()
        upper_1.x = self.config.window.width + upper_1.w * 3
        lower_1.x = self.config.window.width + upper_1.w * 3
        self.upper.append(upper_1)
        self.lower.append(lower_1)

        upper_2, lower_2 = self.make_random_pipes()
        upper_2.x = upper_1.x + upper_1.w * 3.5
        lower_2.x = upper_1.x + upper_1.w * 3.5
        self.upper.append(upper_2)
        self.lower.append(lower_2)

    def make_random_pipes(self) -> List[Pipe]:
        """Returns a randomly generated pipe."""
        # y of gap between upper and lower pipe
        base_y = self.config.window.viewport_height

        gap_y = random.randrange(0, int(base_y * 0.6 - self.pipe_gap))
        gap_y += int(base_y * 0.2)
        pipe_height = self.config.images.pipe[0].get_height()
        pipe_x = self.config.window.width + 10

        upper_pipe = Pipe(
            self.config,
            self.config.images.pipe[0],
            pipe_x,
            gap_y - pipe_height,
        )

        lower_pipe = Pipe(
            self.config,
            self.config.images.pipe[1],
            pipe_x,
            gap_y + self.pipe_gap,
        )

        return upper_pipe, lower_pipe

    def render(self) -> None:
        """Render the pipes."""
        for up_pipe, low_pipe in zip(self.upper, self.lower):
            up_pipe.render()
            low_pipe.render()
