.PHONY: help install lint format test check clean run agent

# Show available commands
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Install dependencies using uv
install: ## Install project dependencies
	uv sync --all-extras

# Run linting checks
lint: ## Run linting and static analysis
	uv run --with ruff ruff check .

# Format code with ruff
format: ## Format code and fix linting issues
	uv run --with ruff ruff format .
	uv run --with ruff ruff check --fix .

# Run test suite (placeholder for when tests are added)
test: ## Run pytest test suite
	@echo "No tests configured yet"

# Run all quality gates
check: ## Run linting and tests
	$(MAKE) lint
	$(MAKE) test

# Clean build artifacts and cache files
clean: ## Remove build artifacts and cache files
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/

# Default target - show help
default:
	@make help

# Run human playable mode
run: ## Run game in human playable mode
	uv run python src/main.py human

# Run agent mode
agent: ## Run game in agent mode
	uv run python src/main.py agent

# Run agent training mode
train: ## Run game in agent training mode
	uv run python src/main.py agent_training
