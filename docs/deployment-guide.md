# Розгортання сайтів на School Website Framework

Фреймворк не залежить від конкретного хостингу чи зворотного проксі. Нижче описано
загальні вимоги до HTTPS і окремий приклад для Docker Compose та Nginx. Для сайту,
створеного через `school-admin startproject`, використовуйте ті самі принципи.

## 1. Налаштування Django

Використовуйте підтримувану версію Django 5.2 LTS. Перед запуском задайте змінні
середовища для свого проєкту:

| Параметр | Репозиторій | Проєкт `school-admin startproject` |
| --- | --- | --- |
| Режим роботи | `DEBUG=False` | `DEBUG=False` |
| Унікальний випадковий ключ | `SECRET_KEY` | `DJANGO_SECRET_KEY` |
| Дозволені домени | `ALLOWED_HOSTS=school.example` | так само |
| Довірені джерела CSRF | `CSRF_TRUSTED_ORIGINS=https://school.example` за потреби | так само |
| Перенаправлення HTTP | `SECURE_SSL_REDIRECT=True` | так само |
| Довіра до проксі | `TRUST_X_FORWARDED_PROTO=True` лише за умов нижче | так само |
| HSTS | `SECURE_HSTS_SECONDS=0` до перевірки HTTPS | так само |

У продакшені обидва варіанти Django вимагають ключ і `ALLOWED_HOSTS`, а cookies
сесії та CSRF позначаються `Secure`. Локальний режим `DEBUG=True` зберігає HTTP
для розробки. Якщо фронтенд і API доступні з одного домену, залиште
`CORS_ALLOWED_ORIGINS` порожнім і використовуйте `/api/v1` як базовий шлях API.

`SECURE_SSL_REDIRECT` увімкнений за замовчуванням при `DEBUG=False`. Коли TLS
завершується на проксі, налаштуйте визначення початкового протоколу за правилами
нижче, щоб HTTPS-запити не потрапляли у цикл перенаправлень.

## 2. TLS і довірений проксі

TLS можна завершувати на сервері застосунку або на зворотному проксі, балансувальнику
чи платформі хостингу. При прямому HTTPS залиште `TRUST_X_FORWARDED_PROTO=False`.
При завершенні TLS на проксі встановіть `TRUST_X_FORWARDED_PROTO=True` **лише якщо**:

1. Django недоступний напряму з інтернету;
2. проксі відкидає отриманий від клієнта `X-Forwarded-Proto` і сам записує `https`
   тільки для запитів, які прийшли через HTTPS.

Інакше клієнт міг би підробити ознаку захищеного запиту. Цю умову окремо
пояснює [документація Django](https://docs.djangoproject.com/en/5.2/ref/settings/#secure-proxy-ssl-header).

Перевірте перенаправлення з HTTP, чинність сертифіката, запити до API та адмінки,
позначку `Secure` у session/CSRF cookies і відсутність змішаного HTTP-контенту.
Для Django виконайте `python manage.py check --deploy` із **продакшен-змінними**.
У репозиторії `python scripts/check_production_security.py` завершується помилкою
за небезпечних попереджень; рекомендації щодо `includeSubDomains` та `preload`
залишені необов'язковими.

### Поетапне ввімкнення HSTS

Почніть із `SECURE_HSTS_SECONDS=0`. Після перевірки всього сайту через HTTPS
встановіть короткий строк, наприклад `300` секунд, а згодом поступово збільшуйте
його. `SECURE_HSTS_INCLUDE_SUBDOMAINS` і `SECURE_HSTS_PRELOAD` залишайте `False`,
доки всі піддомени не підтримують HTTPS і не ухвалено окреме рішення щодо preload.
Помилковий довгий строк HSTS може надовго заблокувати доступ до сайту в браузерах.

## 3. Необов'язковий приклад Docker Compose

[docker-compose.prod.yml](../docker-compose.prod.yml) запускає MySQL та Gunicorn,
але не вмикає TLS і не нав'язує конкретний проксі. БД не має опублікованого порту,
а Gunicorn доступний лише на `127.0.0.1` хоста. Образ не монтує вихідний код;
статичні й завантажені файли зберігаються в `runtime/`.

Скопіюйте [.env.prod.example](../.env.prod.example) у `.env.prod`, задайте
унікальні секрети, домен і параметри БД. `.env.prod` не відстежується Git.
Для довіреного проксі, який переписує заголовок, задайте
`TRUST_X_FORWARDED_PROTO=True` у `.env.prod`; зразок Nginx нижче потребує саме
такого значення.

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --build
docker compose --env-file .env.prod -f docker-compose.prod.yml exec backend python manage.py check --deploy
```

Для React-сайту зберіть статичні файли окремо: `cd frontend && npm ci &&
npm run build:app`. Збірка використовує відносний `/api/v1`, якщо не задано
`VITE_API_URL`. Сервер має віддавати `frontend/dist`, Django `runtime/static`
після `collectstatic`, а файли `runtime/media` — як завантажений контент.
Резервуйте базу даних та `runtime/media` відповідно до способу розгортання.

### Приклад Nginx на тому самому хості

Це лише один варіант. Замініть домен, шляхи та сертифікат. Спочатку отримайте
сертифікат для домену й налаштуйте його автоматичне поновлення.

```nginx
server {
    listen 80;
    server_name school.example;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name school.example;
    ssl_certificate /etc/letsencrypt/live/school.example/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/school.example/privkey.pem;
    client_max_body_size 50M;

    root /srv/school-site/frontend/dist;
    index index.html;

    location /static/ { alias /srv/school-site/runtime/static/; }
    location /media/ { alias /srv/school-site/runtime/media/; }

    location ~ ^/(api|admin)/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / { try_files $uri $uri/ /index.html; }
}
```

`proxy_set_header X-Forwarded-Proto $scheme` замінює клієнтський заголовок.
Оскільки Gunicorn слухає лише адресу localhost хоста, йому можна довіряти в
цій схемі. Перевірте `nginx -t`, HTTP→HTTPS, `/api/v1/core/manifest/`, `/admin/`
та статичні файли до збільшення строку HSTS.

Для іншого хостингу або проксі використовуйте ті самі правила без Docker і Nginx.
У згенерованому проєкті встановіть відповідний WSGI/ASGI-сервер, виконайте
`migrate`, `setup_school_roles` та `collectstatic` і налаштуйте доступ до медіафайлів окремо.
