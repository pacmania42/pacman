SRC = ./pac-man.py
SYNC := .synced

run: install
	uv run python3 pac-man.py config.json

cheat: install
	uv run python3 pac-man.py config-cheat.json

install: $(SYNC)

$(SYNC): pyproject.toml
	uv sync || pip install uv && uv sync
	@touch $(SYNC)
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf dist/
	rm -rf $(SYNC)

lint: $(SYNC)
	uv run ruff check $(SRC) 2>/dev/null || ruff check $(SRC)
	uv run flake8 $(SRC)
	uv run mypy $(SRC) --strict

debug: install
	uv run python3 -m pdb pac-man.py config.json

test: $(SYNC)
	uv run pytest

format:
	uv run ruff check --fix $(SRC) 2>/dev/null || ruff check --fix $(SRC)

build:
	uv build

re: clean run

	
.PHONY: run install clean lint debug test format build re
