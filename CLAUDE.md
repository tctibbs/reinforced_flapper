# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**reinforced_flapper** - Flappy Bird implementation with reinforcement learning capabilities

- Stack: Python 3.12+, Pygame (game engine), Gymnasium (RL environment), Stable-Baselines3 (DQN agent)
- Package Manager: Poetry
- Purpose: Training RL agents to play Flappy Bird using Deep Q-Learning, with human playable mode for comparison

## Development Commands

### Running the Game

```bash
# Human playable mode (default)
make run
# or
python -m src.main human

# Agent play mode (trained agent plays)
make agent
# or
python -m src.main agent

# Agent training mode
python -m src.main agent_training
```

### Dependency Management

```bash
# Install dependencies with Poetry
poetry install

# Add new dependency
poetry add <package-name>

# Add dev dependency
poetry add --group dev <package-name>
```

### Code Quality

```bash
# Format code with Ruff
make format
# or directly:
uv run --with ruff ruff format .

# Lint code with Ruff
make lint
# or directly:
uv run --with ruff ruff check .

# Fix linting issues automatically
uv run --with ruff ruff check --fix .

# Run all quality checks
make check

# Clean build artifacts
make clean
```

**Pre-commit hooks:**
```bash
# Install pre-commit hooks (first time setup)
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

The pre-commit configuration includes:
- Ruff linting and formatting
- Trailing whitespace removal
- End-of-file fixing
- YAML validation
- Large file checks
- Merge conflict detection
- Debug statement detection

## Architecture

### Dual Game Implementations

The codebase contains **two parallel implementations** of Flappy Bird:

1. **Flappy** (`src/flappy.py`) - Original async-based game implementation
   - Uses Python asyncio for game loop
   - Standalone game without RL integration
   - Currently not actively used in main entry point

2. **FlappyBirdEnv** (`src/flappy_env.py`) - Gymnasium environment wrapper
   - Implements `gym.Env` interface for RL training
   - Same game logic as Flappy, but structured for agent interaction
   - **This is the active implementation** used in `src/main.py`

Both share the same entity system and game mechanics but differ in control flow structure.

### Core Architecture Patterns

**Entity-Component Pattern**:
- Base `Entity` class in `src/entities/entity.py` defines common behavior (tick, render, check_crash)
- Game objects extend Entity: `Player`, `Pipes`, `Floor`, `Background`, `Score`, `WelcomeMessage`, `GameOver`
- Each entity encapsulates its own update logic and rendering

**Gymnasium Environment Interface** (`FlappyBirdEnv`):
- `action_space`: Discrete(2) - 0 = no flap, 1 = flap
- `observation_space`: Box(low=0, high=255, shape=(288, 512, 3)) - RGB screen pixels
- `reset()`: Initialize new game state, returns initial observation
- `step(action)`: Execute action, update state, return (obs, reward, done, info)
- `render()`: Display game state, handle human input events in human mode

**Reward Structure**:
- +1 per frame survived
- -100 for collision (death)
- Score increases handled separately by Score entity

### Project Structure

```
src/
├── main.py              # Entry point, mode selection (human/agent/agent_training)
├── flappy_env.py        # Gymnasium environment (ACTIVE)
├── flappy.py            # Async game implementation (legacy/reference)
├── agent.py             # DQN training script with Stable-Baselines3
├── entities/            # Game objects
│   ├── entity.py        # Base Entity class
│   ├── player.py        # Bird with PlayerMode (SHM/NORMAL/CRASH)
│   ├── pipe.py          # Pipe, Pipes classes
│   ├── floor.py         # Scrolling floor
│   ├── background.py    # Static background
│   ├── score.py         # Score display and tracking
│   ├── game_over.py     # Game over message
│   └── welcome_message.py # Splash screen message
└── utils/               # Shared utilities
    ├── game_config.py   # GameConfig dataclass (screen, clock, fps, window, images, sounds)
    ├── images.py        # Image asset loader
    ├── sounds.py        # Sound asset loader
    ├── window.py        # Window configuration
    ├── constants.py     # Game constants
    └── utils.py         # Helper functions (clamp, pixel_collision, get_hit_mask)
```

### Key Concepts

**PlayerMode** (enum in `src/entities/player.py`):
- `SHM`: Simple Harmonic Motion - bird bobs up/down on splash screen
- `NORMAL`: Active gameplay with gravity and flapping
- `CRASH`: Death animation, falling to ground

**Game Loop Flow**:
1. Splash screen (PlayerMode.SHM) - wait for user input
2. Play (PlayerMode.NORMAL) - game runs until collision
3. Game over (PlayerMode.CRASH) - show death animation and score
4. Loop back to splash

**Collision Detection**:
- Pixel-perfect collision using `pixel_collision()` utility
- Player checks collision against pipes and floor each frame
- Implemented in `Player.collided()` method

## RL Agent Training

The DQN agent (`src/agent.py`) uses:
- CNN Policy (processes raw screen pixels)
- Experience replay buffer (10,000 transitions)
- Target network updates every 500 steps
- Batch size of 32
- Learning starts after 1,000 steps

Model is saved as `dqn_flappybird` after training.

## Important Notes

- Game runs at 30 FPS (configured in `GameConfig`)
- Screen resolution: 288x512 pixels (portrait orientation)
- Assets loaded from `assets/` directory (sprites, audio)
- Ruff is configured to ignore F401 (unused imports) in `__init__.py` files
- The `step()` method in `FlappyBirdEnv` includes a hardcoded 25ms delay via `pygame.time.wait(25)` - this may affect RL training speed

## Current State

Based on git history:
- Initial fork of FlapPyBird completed
- Reworked into Gymnasium environment
- Main entry point supports human/agent/agent_training modes
- Agent training mode placeholder exists but implementation may be incomplete (check `src/agent.py` vs `src/main.py` integration)
