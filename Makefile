# Project Chimera - Standardised commands
# Task 3.2: Containerization & Automation

IMAGE_NAME := chimera-tenx
PYTHON_MIN := 3.13

.PHONY: setup test spec-check clean help

help:
	@echo "Targets:"
	@echo "  make setup      - Install dependencies (uv sync)"
	@echo "  make test      - Run tests in Docker"
	@echo "  make spec-check - Verify spec alignment (files + contract tests)"
	@echo "  make clean     - Remove Docker image and cache"

setup:
	uv sync --all-groups

test:
	docker build -t $(IMAGE_NAME) .
	docker run --rm $(IMAGE_NAME)

spec-check:
	@echo "=== Spec alignment check (Option A) ==="
	@echo "Checking required spec files..."
	@test -f specs/technical.md || (echo "ERROR: specs/technical.md missing" && exit 1)
	@test -f specs/functional.md || (echo "ERROR: specs/functional.md missing" && exit 1)
	@test -f specs/_meta.md || (echo "ERROR: specs/_meta.md missing" && exit 1)
	@test -f skills/README.md || (echo "ERROR: skills/README.md missing" && exit 1)
	@echo "Checking Python version (>= $(PYTHON_MIN))..."
	@python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 13) else 1)" || echo "WARNING: Python 3.13+ recommended (see specs)"
	@echo "Running contract validation tests in Docker..."
	@docker build -t $(IMAGE_NAME) -q . && docker run --rm $(IMAGE_NAME) uv run pytest tests/test_trend_fetcher.py tests/test_skills_interface.py -v
	@echo "Spec check complete."

clean:
	docker rmi $(IMAGE_NAME) 2>/dev/null || true
