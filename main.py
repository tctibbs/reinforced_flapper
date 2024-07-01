"""
This is the main module of the reinforced_flapper program.

It contains the entry point of the program, which initializes and starts the Flappy game.
"""

import asyncio

from src.flappy import Flappy


async def main() -> None:
    """Entry point of the program."""
    await Flappy().start()

if __name__ == "__main__":
    asyncio.run(main())
