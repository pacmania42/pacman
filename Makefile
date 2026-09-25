SYNC := .synced
RUFF_PREFIX := $(shell [ -e /etc/NIXOS ] && echo "" || echo "uv run ")
MYPY_FLAGS := --warn-return-any --warn-unused-ignores \
              --ignore-missing-imports --disallow-untyped-defs \
              --check-untyped-defs

run: install
	uv run python3 pac-man.py config.json

install: $(SYNC)

$(SYNC): pyproject.toml
	uv sync || (pip install uv && uv sync)
	@touch $(SYNC)
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf dist/ build
	rm -rf $(SYNC)

clean-all: clean
	rm -rf .venv

lint: $(SYNC)
	uv run flake8 .
	uv run mypy . $(MYPY_FLAGS)

lint-strict: $(SYNC)
	$(RUFF_PREFIX) ruff check .
	uv run flake8 .
	uv run mypy --strict .

debug: install
	uv run python3 -m pdb pac-man.py config.json

test: $(SYNC)
	uv run pytest -q

format:
	$(RUFF_PREFIX) ruff format .
	$(RUFF_PREFIX) ruff check --fix .

build: install
	uv run pyinstaller pacman.spec
	# uv run pyinstaller --name pacman --windowed --noconfirm --add-data src/assets:src/assets pac-man.py --icon pacman-icon.ico --onefile --collect-all mlx

re: clean-all run

	
.PHONY: run install clean clean-all lint lint-strict debug test \
        format build re
