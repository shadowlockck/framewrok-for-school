.PHONY: up down build logs restart migrate seed superuser shell clean help

help:
	@echo "Команди керування School Website Framework:"
	@echo "  make up         - Запустити всі контейнери (db, backend, frontend)"
	@echo "  make down       - Зупинити всі контейнери"
	@echo "  make build      - Перезібрати Docker-образи"
	@echo "  make logs       - Переглядати логи в реальному часі"
	@echo "  make migrate    - Застосувати міграції бази даних"
	@echo "  make seed       - Наповнити базу зразковими даними типової школи"
	@echo "  make superuser  - Створити обліковий запис адміністратора"
	@echo "  make shell      - Запустити Django shell у контейнері"
	@echo "  make clean      - Видалити контейнери та volumes"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

restart:
	docker compose restart

migrate:
	docker compose exec backend python manage.py migrate

seed:
	docker compose exec backend python manage.py seed_school_data

superuser:
	docker compose exec backend python manage.py createsuperuser

shell:
	docker compose exec backend python manage.py shell

clean:
	docker compose down -v
