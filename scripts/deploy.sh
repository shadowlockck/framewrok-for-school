#!/usr/bin/env bash
set -e

echo "=== Початок процедури оновлення School Website Framework ==="

echo "[1/4] Отримання останніх змін із репозиторію..."
git pull origin main

echo "[2/4] Перезбірка Docker-контейнерів..."
docker compose build

echo "[3/4] Запуск оновлених контейнерів..."
docker compose up -d

echo "[4/4] Застосування нових міграцій бази даних..."
docker compose exec -T backend python manage.py migrate
docker compose exec -T backend python manage.py setup_school_roles

echo "=== Оновлення успішно завершено! Сайт доступний та функціонує. ==="
