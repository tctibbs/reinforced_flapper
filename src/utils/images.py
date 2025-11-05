"""Module for managing game images."""

import random

import pygame

from src.utils.constants import BACKGROUNDS, PIPES, PLAYERS


class Images:
    """Game images.

    Attributes:
        numbers: List of number sprites.
        game_over: Game over sprite.
        welcome_message: Welcome message sprite.
        base: Base sprite.
        background: Background sprite.
        player: Tuple of player sprites.
        pipe: Tuple of pipe sprites.
    """

    numbers: list[pygame.Surface]
    game_over: pygame.Surface
    welcome_message: pygame.Surface
    base: pygame.Surface
    background: pygame.Surface
    player: tuple[pygame.Surface]
    pipe: tuple[pygame.Surface]

    def __init__(self) -> None:
        """Initialize game images and load sprites."""
        self.numbers = [
            pygame.image.load(f"assets/sprites/{num}.png").convert_alpha()
            for num in range(10)
        ]

        # game over sprite
        self.game_over = pygame.image.load(
            "assets/sprites/gameover.png"
        ).convert_alpha()
        # welcome_message sprite for welcome screen
        self.welcome_message = pygame.image.load(
            "assets/sprites/message.png"
        ).convert_alpha()
        # base (ground) sprite
        self.base = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.randomize()

    def randomize(self) -> None:
        """Randomize the game sprites."""
        # select random background sprites
        rand_bg = random.randint(0, len(BACKGROUNDS) - 1)
        # select random player sprites
        rand_player = random.randint(0, len(PLAYERS) - 1)
        # select random pipe sprites
        rand_pipe = random.randint(0, len(PIPES) - 1)

        self.background = pygame.image.load(BACKGROUNDS[rand_bg]).convert()
        self.player = (
            pygame.image.load(PLAYERS[rand_player][0]).convert_alpha(),
            pygame.image.load(PLAYERS[rand_player][1]).convert_alpha(),
            pygame.image.load(PLAYERS[rand_player][2]).convert_alpha(),
        )
        self.pipe = (
            pygame.transform.flip(
                pygame.image.load(PIPES[rand_pipe]).convert_alpha(),
                False,
                True,
            ),
            pygame.image.load(PIPES[rand_pipe]).convert_alpha(),
        )
