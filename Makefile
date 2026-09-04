SRC = ./pac-man.py \
	./src/main.py \
	./src/__init__.py

SYNC := .synced
RUFF_PREFIX := $(shell [[ -e /etc/NIXOS ]] && echo "" || echo "uv run ")

run: install
	uv run python3 pac-man.py config.json

cheat: install
	uv run python3 pac-man.py config-cheat.json

install: $(SYNC)

$(SYNC): pyproject.toml
	uv sync || (pip install uv && uv sync)
	@touch $(SYNC)
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf dist/
	rm -rf $(SYNC)

clean-all: clean
	rm -rf .venv

lint: $(SYNC)
	$(RUFF_PREFIX) ruff check $(SRC)
	uv run flake8 $(SRC)
	uv run mypy $(SRC) --strict

debug: install
	uv run python3 -m pdb pac-man.py config.json

test: $(SYNC)
	uv run pytest

format:
	$(RUFF_PREFIX) ruff check --fix $(SRC)

build:
	uv build

re: clean-all run

	
.PHONY: run cheat install clean clean-all lint debug test format build re
