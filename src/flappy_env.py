"""Flappy Bird Gymnasium environment for reinforcement learning."""

import sys
from typing import ClassVar

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from src.entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from src.utils import GameConfig, Images, Sounds, Window


class FlappyBirdEnv(gym.Env):
    """Custom Gym Environment for Flappy Bird."""

    metadata: ClassVar[dict[str, list[str]]] = {"render.modes": ["human"]}

    def __init__(self) -> None:
        """Initialize the Flappy Bird environment."""
        super().__init__()

        # Define action and observation space
        # Actions: 0 = no flap, 1 = flap
        self.action_space = spaces.Discrete(2)

        # Observation space: Define as needed
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(288, 512, 3), dtype=np.uint8
        )

        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )

    def reset(self) -> np.ndarray:
        """Reset the environment state."""
        self.background = Background(self.config)
        self.floor = Floor(self.config)
        self.player = Player(self.config)
        self.welcome_message = WelcomeMessage(self.config)
        self.game_over_message = GameOver(self.config)
        self.pipes = Pipes(self.config)
        self.score = Score(self.config)

        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)
        self.done = False
        return self._get_observation()

    def step(self, action: int) -> tuple:
        """Take a step in the environment."""
        if action == 1:
            self.player.flap()

        pygame.time.wait(25)
        self.background.tick()
        self.floor.tick()
        self.pipes.tick()
        self.score.tick()
        self.player.tick()

        obs = self._get_observation()
        reward = self._calculate_reward()
        self.done = self.player.collided(self.pipes, self.floor)
        if self.done:
            self.game_over()

        for _i, pipe in enumerate(self.pipes.upper):
            if self.player.crossed(pipe):
                self.score.add()

        return obs, reward, self.done, {}

    def render(self, mode: str = "human") -> bool:
        """Render the environment.

        Args:
            mode: The mode to render the environment in.

        Returns:
            bool: True if the environment is still running, False if it is closed.
        """
        self.config.screen.blit(self.config.images.background, (0, 0))

        self.floor.render()
        self.pipes.render()
        self.player.render()
        self.score.render()
        pygame.display.update()

        # Event handling for human play
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.close()
                return False
            if self._is_tap_event(event):
                self.step(1)

        self.step(0)
        return True

    def close(self) -> None:
        """Close the environment."""
        pygame.quit()

    def _get_observation(self) -> np.ndarray:
        """Capture the game screen as the observation."""
        return pygame.surfarray.array3d(pygame.display.get_surface()).transpose(1, 0, 2)

    def _calculate_reward(self) -> int:
        """Calculate the reward for the current step."""
        reward = 1
        if self.player.collided(self.pipes, self.floor):
            reward = -100
        return reward

    def _is_tap_event(self, event: pygame.event.Event) -> bool:
        """Check if the event is a tap event."""
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    def game_over(self) -> None:
        """Crashes the player down and shows gameover image."""
        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self._is_tap_event(event):
                    self.splash()
                    return

            self.pipes.tick()
            self.player.tick()

            self.background.render()
            self.floor.render()
            self.pipes.render()
            self.score.render()
            self.player.render()
            self.game_over_message.render()

            self.config.tick()
            pygame.display.update()

    def splash(self) -> None:
        """Shows welcome splash screen animation of flappy bird."""
        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self._is_tap_event(event):
                    self.reset()
                    return

            self.background.render()
            self.floor.render()
            self.player.render()
            self.welcome_message.render()

            pygame.display.update()
            self.config.tick()

    def check_quit_event(self, event: pygame.event.Event) -> None:
        """Check if the quit event is triggered."""
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


# Game loop for human play
if __name__ == "__main__":
    env = FlappyBirdEnv()
    env.reset()
    env.splash()

    running = True
    while running:
        running = env.render()

    env.close()
