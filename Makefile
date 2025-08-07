.PHONY: help install lint format clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  lint         - Check code quality (autoflake + isort + black)"
	@echo "  format       - Format code (autoflake + isort + black)"
	@echo "  clean        - Clean up cache and temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"

install:
	poetry lock && poetry install --only main

lint:
	poetry run autoflake --check --remove-all-unused-imports --recursive app/
	poetry run isort --check-only app/
	poetry run black --check app/

format:
	poetry run autoflake --remove-all-unused-imports --in-place --recursive app/
	poetry run isort app/
	poetry run black app/

format-check: lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ .coverage htmlcov/ logs/ 2>/dev/null || true

docker-build:
	docker build -t app .

docker-run:
	docker run -p 8000:8000 app

docker-build-run:
	docker build -t app . && run -p 8000:8000 app