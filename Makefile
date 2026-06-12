MAIN := pac-man.py
CONFIG := config.json
CONFIG_EVAL := config_eval.json

# stamp files to track when last synced, check if uv is installed
SYNC := .synced
INSTALL := .uv_installed

# default rule, run main entry
run: $(INSTALL) $(SYNC)
	uv run python $(MAIN) $(CONFIG)

# for evaluations
eval: $(INSTALL) $(SYNC)
	uv run python $(MAIN) $(CONFIG_EVAL)

# Makes sure that uv is installed
$(INSTALL):
	pipx install uv || pip install uv
	touch $(INSTALL)
	
# Syncs the environment with pyproject.toml
$(SYNC): $(INSTALL) pyproject.toml
	uv sync
	touch $(SYNC)

# thoroughly cleans the environment
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .ruff_cache .pytest_cache
	rm -rf $(INSTALL) .venv
	rm -rf uv.lock

# basic linting
lint: $(SYNC)
	uv run ruff check
	uv run flake8
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

# strict linting
lint-strict: $(SYNC)
	uvx ruff check
	uvx flake8
	uv run mypy . --strict

# runs the test suite in ./tests
test: $(SYNC)
	uv run pytest

# format every source file
format:
	uvx ruff format

# spawns pdb for debugging
debug: $(SYNC)
	uv run python -m pdb main.py

# cleans the env and runs the default entry
re: clean run

# not files; don't check timestamp;
.PHONY: run eval clean format lint lint-strict debug re test 
