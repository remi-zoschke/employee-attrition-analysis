.PHONY: setup render-html preview lint lint-fix test clean help

help:
	@echo "Employee Attrition Analysis - Available commands:"
	@echo "  make setup       - Install dependencies"
	@echo "  make render-html - Generate HTML report"
	@echo "  make preview     - Live preview"
	@echo "  make lint        - Check Python code"
	@echo "  make lint-fix    - Auto-fix Python code"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean generated files"

setup:
	uv sync
	uv run python -m ipykernel install --user --name=employee-attrition-analysis --display-name "Python (employee-attrition-analysis)"
	@echo "Dependencies installed"
	@echo "Make sure Quarto is installed: https://quarto.org/docs/get-started/"

prepare-data:
	uv run python -m scripts.prepare_data
	
render-html:
	quarto render report.qmd --to html

preview:
	quarto preview report.qmd

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

lint-fix:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

test:
	uv run pytest tests/ -v

clean:
	rm -rf output/*
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true	