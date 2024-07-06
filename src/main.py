"""This is the main module of the reinforced_flapper program.

It contains the entry point of the program, which initializes and starts the Flappy game.
"""

import argparse
from .flappy_env import FlappyBirdEnv  # Assuming you have this Gym environment defined


def main(mode: str) -> None:
    """Entry point of the program."""
    if mode == "human":
        human_mode()

    elif mode == "agent":
        pass

    elif mode == "agent_training":
        pass

def human_mode() -> None: 
    """Runs the Flappy Bird game in human mode."""
    FlappyBirdEnv()
    env = FlappyBirdEnv()
    env.reset()
    env.splash()

    running = True
    while running:
        running = env.render()

    env.close()

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Flappy Bird Reinforcement Learning")
    parser.add_argument(
        "mode",
        choices=["human", "agent", "agent_training"],
        help="Mode to run the program in.\n"
            "\t'human' for human play,\n"
            "\t'agent' for agent play,\n"
            "\t'agent_training' for training the agent.",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.mode == "human":
        main(args.mode)
    else:
        main(args.mode)
