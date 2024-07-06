default:
	@make run

run:
	python -m src.main human

agent:
	python -m src.main agent

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
