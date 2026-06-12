MAIN := pac-man.py
CONFIG := config.json
CONFIG_EVAL := config_eval.json

VENV := .synced
UV_STAMP := .uv_installed

run: $(UV_STAMP) $(VENV)
	uv run python $(MAIN) $(CONFIG)

eval: $(UV_STAMP) $(VENV)
	uv run python $(MAIN) $(CONFIG_EVAL)

$(UV_STAMP):
	pipx install uv || pip install uv
	touch $(UV_STAMP)
	
$(VENV): $(UV_STAMP) pyproject.toml
	uv sync
	touch $(VENV)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .ruff_cache .pytest_cache
	rm -rf $(UV_STAMP) .venv
	rm -rf uv.lock

lint: $(VENV)
	uv run ruff check
	uv run flake8
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: $(VENV)
	uvx ruff check
	uvx flake8
	uv run mypy .

test: $(VENV)
	uv run pytest

format:
	uvx ruff format

debug: $(VENV)
	uv run python -m pdb main.py

re: clean run

.PHONY: run eval clean format lint lint-strict debug re test 
