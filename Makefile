# Define variables
APP_CONTAINER=app

.PHONY: up down test lint createsuperuser startapp

# Bring the Docker Compose services up
up:
	docker compose up

# Bring the Docker Compose services down
down:
	docker compose down

# Run Django tests
test:
	docker compose run --rm $(APP_CONTAINER) sh -c "python manage.py test"

# Run flake8 for linting
lint:
	docker compose run --rm $(APP_CONTAINER) sh -c "flake8"

# Create a Django superuser
createsuperuser:
	docker compose run --rm $(APP_CONTAINER) sh -c "python manage.py createsuperuser"

# Make migrations
makemigrations:
	docker compose run --rm $(APP_CONTAINER) sh -c "python manage.py makemigrations"

# Create a new Django app with the given name
# Usage: make startapp name=<app_name>
startapp:
	@if [ -z "$(name)" ]; then \
		echo "Error: Please provide a name for the app. Usage: make startapp name=<app_name>"; \
		exit 1; \
	fi
	docker compose run --rm $(APP_CONTAINER) sh -c "python manage.py startapp $(name)"
