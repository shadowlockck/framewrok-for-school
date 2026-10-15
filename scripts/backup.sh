#!/usr/bin/env bash
set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_BACKUP_FILE="${BACKUP_DIR}/school_db_${TIMESTAMP}.sql.gz"
MEDIA_BACKUP_FILE="${BACKUP_DIR}/school_media_${TIMESTAMP}.tar.gz"

# Завантаження змінних оточення з .env за наявності
if [ -f .env ]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

DB_USER_NAME="${DB_USER:-school_user}"
DB_PASS_VAL="${DB_PASSWORD:-school_secure_pass_2026}"
DB_DATABASE="${DB_NAME:-school_db}"

mkdir -p "${BACKUP_DIR}"

echo "[1/3] Створення дампу бази даних MySQL..."
docker compose exec -T db mysqldump -u "${DB_USER_NAME}" -p"${DB_PASS_VAL}" "${DB_DATABASE}" | gzip > "${DB_BACKUP_FILE}"

echo "[2/3] Резервне копіювання завантажених документів та медіафайлів..."
if [ -d "backend/media" ]; then
    tar -czf "${MEDIA_BACKUP_FILE}" -C backend media
elif docker compose ps backend --status running -q 2>/dev/null | grep -q .; then
    docker compose cp backend:/app/media "${BACKUP_DIR}/media_temp" 2>/dev/null || true
    if [ -d "${BACKUP_DIR}/media_temp" ]; then
        tar -czf "${MEDIA_BACKUP_FILE}" -C "${BACKUP_DIR}" media_temp
        rm -rf "${BACKUP_DIR}/media_temp"
    fi
fi

echo "[3/3] Очищення старих бекапів (старше 30 днів)..."
find "${BACKUP_DIR}" -type f -name "*.gz" -mtime +30 -delete

echo "Резервне копіювання успішно завершено: ${BACKUP_DIR}"
