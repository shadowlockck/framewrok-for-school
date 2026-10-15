# Керівництво з розгортання та адміністрування (Deployment Guide)

> **School Website Framework — Single-tenant Production Deployment**

---

## 1. Системні вимоги

- **ОС:** Linux (Ubuntu 22.04 / 24.04 LTS або Debian 12 recommended);
- **Процесор:** від 2 vCPU;
- **Оперативна пам'ять:** від 2 ГБ RAM (рекомендовано 4 ГБ);
- **Дисковий простір:** від 20 ГБ SSD;
- **Встановлене ПЗ:** Docker Engine 24+ та Docker Compose v2+.

---

## 2. Швидке встановлення на сервері

### Крок 1: Клонування репозиторію

```bash
cd /opt
sudo git clone https://github.com/your-org/framework-for-school.git school-site
cd school-site
```

### Крок 2: Налаштування файлу середовища (`.env`)

Скопіюйте приклад та обов'язково змініть секретні ключі:

```bash
cp .env.example .env
nano .env
```

Обов'язкові змінні для продакшену:
```ini
SECRET_KEY=your-ultra-secure-django-secret-key-at-least-50-chars
DEBUG=False
ALLOWED_HOSTS=school.edu.ua,www.school.edu.ua,backend

DB_NAME=school_production_db
DB_USER=school_prod_user
DB_PASSWORD=generated-strong-db-password-2026
DB_ROOT_PASSWORD=generated-strong-root-password-2026

VITE_API_URL=https://school.edu.ua/api/v1
```

### Крок 3: Запуск сервісів

```bash
make up
```
або
```bash
docker compose up -d --build
```

### Крок 4: Застосування міграцій та наповнення початковими даними

```bash
make migrate
make seed
make superuser
```

---

## 3. Налаштування зворотного проксі (Nginx + HTTPS / Let's Encrypt)

Рекомендована конфігурація `/etc/nginx/sites-available/school.edu.ua`:

```nginx
server {
    listen 80;
    server_name school.edu.ua www.school.edu.ua;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name school.edu.ua www.school.edu.ua;

    ssl_certificate /etc/letsencrypt/live/school.edu.ua/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/school.edu.ua/privkey.pem;

    # Максимальний розмір завантаження PDF-документів та звітів
    client_max_body_size 50M;

    # Frontend (React SPA)
    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API & Admin
    location ~ ^/(api|admin|static|media)/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Отримання безкоштовного SSL-сертифіката:
```bash
sudo certbot --nginx -d school.edu.ua -d www.school.edu.ua
```

---

## 4. Резервне копіювання (Backup)

Використовуйте автоматичний скрипт `scripts/backup.sh`:

```bash
./scripts/backup.sh
```

Він створює архів із дампом бази даних MySQL та всіма завантаженими документами/медіафайлами в папку `./backups/`.
Рекомендовано додати до `crontab` щоденне виконання о 02:00:
```cron
0 2 * * * /opt/school-site/scripts/backup.sh >> /var/log/school_backup.log 2>&1
```

---

## 5. Оновлення фреймворку (Deploy & Update)

Для оновлення до нової версії без простою:

```bash
./scripts/deploy.sh
```
Скрипт автоматично:
1. Отримує нові зміни через `git pull`;
2. Перезбирає образи контейнерів;
3. Виконує нові міграції бази даних;
4. Перезапускає контейнери з нульовим часом простою.
