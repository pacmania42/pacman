MAIN := pac-man.py
CONFIG := config.json
CONFIG_EVAL := config_eval.json

MYPY_OPTIONS := --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

SRC := pac-man.py \
	src/main.py \
	src/config.py \
	src/entity_data.py \
	tests/test_config.py

# stamp files to track when last synced, check if uv is installed
SYNC := .synced


# default rule, runs game with the provided config
run: install
	uv run python $(MAIN) $(CONFIG)


# for evaluations
eval: $(SYNC)
	uv run python $(MAIN) $(CONFIG_EVAL)


# calls sync for syncing
install: $(SYNC)


# Makes sure that uv is installed and syncs the env
$(SYNC): pyproject.toml
	git config core.hooksPath .githooks
	uv sync || pip install uv && uv sync
	@touch $(SYNC)
	

# thoroughly cleans the environment
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .ruff_cache .pytest_cache
	rm -rf $(SYNC) .venv


# basic linting
lint: $(SYNC)
	ruff check $(SRC)
	uv run flake8 $(SRC)
	uv run mypy $(SRC) $(MYPY_OPTIONS)


# strict linting
lint-strict: $(SYNC)
	ruff check $(SRC)
	uv run flake8 $(SRC)
	uv run mypy --strict $(SRC)


# runs the test suite in ./tests
test: $(SYNC)
	uv run pytest


# format every source file
format:
	ruff check --fix $(SRC)


# spawns pdb for debugging
debug: $(SYNC)
	uv run python -m pdb $(MAIN) $(CONFIG)


# runs the game after thoroughly cleaning
re: clean run


# not files; don't check timestamp;
.PHONY: run eval clean format lint lint-strict debug re test 
