default:
	@make run

run:
	python main.py

agent:
	python -m src.flappy_env

# init:
# 	@pip install -U pip; \
# 	pip install -e ".[dev]"; \s
# 	pre-commit install; \

# pre-commit:
# 	pre-commit install

# pre-commit-all:
# 	pre-commit run --all-files

# format:
# 	black .

# lint:
# 	ruff format
# 	ruff check --fix
