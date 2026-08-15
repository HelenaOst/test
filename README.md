# AutoRia Clone — Car Marketplace API

Навчальний REST API для платформи продажу автомобілів, побудований на **Django REST Framework**.

Проєкт демонструє роботу з:

- Django REST Framework
- JWT-аутентифікацією
- ролями та permissions
- Docker / Docker Compose
- MySQL
- Redis
- Celery та Celery Beat
- фільтрацією та пошуком
- асинхронними задачами
- email-сповіщеннями
- OpenAPI-документацією через DRF-Spectacular
- інтеграцією з PrivatBank API
- хмарною базою даних Railway

> **Проєкт створений у навчальних цілях.**
>
> Поточна версія використовує вже налаштовану хмарну базу даних Railway з тестовими даними.

---

# Зміст

- [Стек технологій](#стек-технологій)
- [Архітектура](#архітектура)
- [Запуск проекту](#запуск-проекту)
- [База даних](#база-даних)
- [Ролі та доступи](#ролі-та-доступи)
- [Преміум акаунт](#преміум-акаунт)
- [Основні API endpoints](#основні-api-endpoints)
- [Celery Tasks](#celery-tasks)
- [Фільтрація та пошук](#фільтрація-та-пошук)
- [Email сповіщення](#email-сповіщення)
- [Документація API](#документація-api)
- [Тестування через Postman](#тестування-через-postman)
- [Додавання нових ролей і permissions](#додавання-нових-ролей-і-permissions)
- [Docker](#docker)
- [Ліцензія](#ліцензія)

---

# Стек технологій

## Backend

- **Python 3.12**
- **Django 6**
- **Django REST Framework**
- **MySQL 8** — основна база даних
- **Redis** — брокер повідомлень для Celery
- **Celery + Celery Beat** — асинхронні та періодичні задачі
- **Docker / Docker Compose** — контейнеризація

## Автентифікація

- **JWT**
- **djangorestframework-simplejwt**

## Документація API

- **DRF-Spectacular** — генерація OpenAPI-схеми
- **Swagger UI** — інтерактивна документація
- **ReDoc** — альтернативне представлення документації

## Інтеграції

- **Mailtrap** — тестування email
- **PrivatBank API** — отримання курсів валют

## Інші бібліотеки

- **django-filter** — фільтрація оголошень
- **Pillow** — робота із зображеннями

---

# Архітектура

Проєкт розділений на Django apps відповідно до окремих доменів:

| App | Призначення |
|-----|-------------|
| `users` | користувачі, ролі, permissions, профілі |
| `auth` | реєстрація, логін, JWT |
| `listing` | оголошення та робота з ними |
| `moderation` | модерація оголошень |
| `cars` | бренди та моделі автомобілів |
| `listing_stats` | статистика оголошень |
| `payment` | курси валют та перерахунок цін |
| `core` | спільні permissions, сервіси та інша інфраструктура |

Для фонових задач використовується **Celery**, а для їхнього періодичного запуску — **Celery Beat**.

---

# Запуск проекту

## 1. Клонування репозиторію

```bash
git clone <url>
cd python_test
```

---

## 2. Створення `.env`

Скопіюйте приклад конфігурації:

```bash
cp .env_example .env
```

Заповніть `.env` необхідними параметрами.

### Поточна конфігурація

Проєкт використовує хмарну базу даних Railway:

```env
MYSQL_HOST=acela.proxy.rlwy.net
MYSQL_PORT=43944
MYSQL_DATABASE=railway
MYSQL_USER=root
MYSQL_PASSWORD=lIIpVlQvnPRZQDOyqwaVObrGlHvZmowU
MYSQL_ROOT_PASSWORD=lIIpVlQvnPRZQDOyqwaVObrGlHvZmowU
```

Для тестування email через Mailtrap:

```env
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=abf3ef193a3d41
EMAIL_HOST_PASSWORD=2d85d3045723bc
EMAIL_PORT=2525
```

Email, на який система надсилає службові повідомлення:

```env
MANAGERS_EMAIL=moderation@automarket.com
```

> **Примітка:** у навчальній версії проєкту тестові credentials вказані безпосередньо в README для спрощення перевірки проєкту.

---

## 3. Запуск Docker

Запустіть усі необхідні сервіси:

```bash
docker compose up -d --build
```

Docker Compose запускає:

- Django application
- MySQL / підключення до БД
- Redis
- Celery worker
- Celery Beat

---

## 4. Перевірка контейнерів

```bash
docker compose ps
```

Усі необхідні сервіси повинні мати статус `Up`.

Для перегляду логів:

```bash
docker compose logs -f app
```

Для Celery:

```bash
docker compose logs -f celery
```

---

## 5. Міграції

Міграції застосовуються автоматично під час запуску контейнера.

За необхідності їх можна виконати вручну:

```bash
docker compose exec app python manage.py migrate
```

> **Важливо:** у поточній Railway БД міграції вже застосовані. При звичайному запуску проєкту повторно виконувати їх не потрібно.

---

# База даних

Проєкт використовує **хмарну MySQL базу даних Railway**.

Локальна MySQL база даних для поточної конфігурації не використовується.

## Параметри бази даних

| Параметр | Значення |
|----------|----------|
| Host | `acela.proxy.rlwy.net` |
| Port | `43944` |
| User | `root` |
| Database | `railway |

> Railway може відповідати повільніше за локальну базу даних. Це особливо помітно під час першого запиту або при виконанні кількох послідовних операцій.

---

# Важливо про fixtures

У поточній версії проєкту **фікстури вже завантажені в Railway БД**.

Також у БД вже існують тестові користувачі.

Тому при звичайному запуску проєкту:

**НЕ потрібно виконувати:**

```bash
docker compose exec app python manage.py loaddata regions.json
docker compose exec app python manage.py loaddata brands.json
docker compose exec app python manage.py loaddata car_models.json
docker compose exec app python manage.py loaddata listings.json
```

Ці команди потрібні тільки у випадку, якщо проєкт запускається з **іншою або чистою базою даних**.

---

## Розгортання на іншій / чистій БД

Якщо потрібно запустити проєкт із новою базою даних:

### 1. Налаштувати `.env`

Вкажіть credentials нової БД:

```env
MYSQL_HOST=...
MYSQL_PORT=...
MYSQL_DATABASE=...
MYSQL_USER=...
MYSQL_PASSWORD=...
```

### 2. Запустити Docker

```bash
docker compose up -d --build
```

### 3. Застосувати міграції

```bash
docker compose exec app python manage.py migrate
```

### 4. Завантажити базові fixtures

```bash
docker compose exec app python manage.py loaddata regions.json
docker compose exec app python manage.py loaddata brands.json
docker compose exec app python manage.py loaddata car_models.json
```

### 5. Створити адміністратора

```bash
docker compose exec app python manage.py createsuperuser
```

### 6. За необхідності завантажити тестові оголошення

Файл `listings.json` містить посилання на конкретних користувачів.

Тому перед його завантаженням необхідно створити користувачів, на яких посилаються fixtures.

```bash
docker compose exec app python manage.py loaddata listings.json
```

> **Примітка:** `listings.json` залежить від наявності відповідних користувачів у базі даних.

---

# Тестові користувачі

У поточній Railway БД вже існують користувачі для тестування:

| Роль | Email / username | Пароль |
|------|------------------|--------|
| **Admin** | `admin` | `admin` |
| **Seller 1** | `seller1@mail.com` | `seller1111` |
| **Seller 2** | `seller2@mail.com` | `seller1111` |

> Ці облікові дані призначені виключно для тестової/навчальної версії проєкту.

---

# Ролі та доступи

| Роль | Можливості |
|------|------------|
| **Buyer** | перегляд оголошень, скарги, створення першого оголошення |
| **Seller** | усе, що Buyer + створення та редагування власних оголошень, робота з фото |
| **Manager** | модерація оголошень, управління користувачами, статистика |
| **Admin (superuser)** | повний доступ до системи |

### Додаткові правила

- Покупець автоматично стає продавцем після створення першого оголошення.
- Базовий акаунт може мати одне активне оголошення.
- Premium-акаунт може мати необмежену кількість активних оголошень.
- Статистика доступна Premium Seller, Manager та Admin.
- Manager може створювати бренди та моделі, але не може їх видаляти.
- Видалення і редагування ключових сутностей `Brand` та `CarModel` доступне тільки Admin.

---

# Преміум акаунт

Оплата реалізована як **mock-функціонал** без реальної платіжної системи.

Ендпоінт:

```http
POST /api/users/me/premium/mock/
```

активує Premium-акаунт без фактичної оплати на 30 днів.

У реальному комерційному проєкті цей механізм має бути замінений інтеграцією з платіжною системою.

---

# Основні API endpoints

## Auth

| Метод | URL | Опис |
|------|-----|------|
| POST | `/api/auth/register/` | Реєстрація |
| POST | `/api/auth/login/` | Логін |
| POST | `/api/auth/refresh/` | Оновлення JWT |
| POST | `/api/auth/logout/` | Вихід |

---

## Users

| Метод | URL | Опис | Доступ |
|------|-----|------|--------|
| GET | `/api/users/` | Список користувачів | Admin / Manager |
| GET | `/api/users/me/` | Поточний користувач | Всі |
| GET | `/api/users/<pk>/` | Перегляд користувача | Всі |
| PATCH | `/api/users/me/update/` | Оновити власний акаунт | Всі |
| DELETE | `/api/users/me/delete/` | Видалити власний акаунт | Всі |
| DELETE | `/api/users/<pk>/delete/` | Видалити користувача | Admin / Manager |
| POST | `/api/users/me/premium/mock/` | Активувати Premium | Buyer / Seller |
| PATCH | `/api/users/<pk>/block/` | Заблокувати користувача | Admin / Manager |
| PATCH | `/api/users/<pk>/unblock/` | Розблокувати користувача | Admin / Manager |
| PATCH | `/api/users/<pk>/manager/` | Призначити Manager | Admin |

---

## Listings

| Метод | URL | Опис | Доступ |
|------|-----|------|--------|
| GET | `/api/listings/` | Список активних оголошень | Публічно |
| GET | `/api/listings/<pk>/` | Перегляд оголошення | Публічно |
| GET | `/api/listings/regions/` | Список регіонів | Публічно |
| GET | `/api/listings/my/` | Власні оголошення | Seller |
| POST | `/api/listings/create/` | Створити оголошення | Buyer / Seller |
| PATCH | `/api/listings/update/<pk>/` | Редагувати оголошення | Seller — власник |
| DELETE | `/api/listings/delete/<pk>/` | Зняти оголошення з продажу | Seller — власник |
| POST | `/api/listings/<pk>/photos/` | Завантажити фото | Seller — власник |
| DELETE | `/api/listings/photos/<pk>/` | Видалити фото | Seller — власник |
| POST | `/api/listings/report-problem/<pk>/` | Поскаржитися на оголошення | Авторизований користувач |
| GET | `/api/listings/edit/` | Pending-оголошення | Admin / Manager |
| PATCH | `/api/listings/moderation/<pk>/` | Модерація оголошення | Admin / Manager |
| GET | `/api/listings/statistics/<pk>/` | Статистика оголошення | Premium Seller / Manager / Admin |

---

## Cars

| Метод | URL | Опис | Доступ |
|------|-----|------|--------|
| GET | `/api/cars/brands/` | Список брендів | Публічно |
| GET | `/api/cars/brands/<pk>/` | Перегляд бренду | Публічно |
| GET | `/api/cars/models/` | Список моделей | Публічно |
| GET | `/api/cars/models/<pk>/` | Перегляд моделі | Публічно |
| GET | `/api/cars/brands/<pk>/models/` | Моделі конкретного бренду | Публічно |
| POST | `/api/cars/request-brand/` | Запит на нову марку | Авторизований користувач |
| POST | `/api/cars/brands/` | Створення бренду | Admin / Manager |
| PATCH / DELETE | `/api/cars/brands/<pk>/` | Редагування / видалення бренду | Admin |
| POST | `/api/cars/models/` | Створення моделі | Admin / Manager |
| PATCH / DELETE | `/api/cars/models/<pk>/` | Редагування / видалення моделі | Admin |

---

## Payment

| Метод | URL | Опис | Доступ |
|------|-----|------|--------|
| GET | `/api/payment/rate/` | Поточний курс валют | Публічно |

---

# Celery Tasks

Проєкт використовує Celery для виконання фонових задач.

| Task | Запуск | Опис |
|------|--------|------|
| `fetch_currency_rates_task` | щодня о 09:00 | Отримання курсів валют з PrivatBank API |
| `update_listings_prices_task` | після оновлення курсів | Перерахунок цін оголошень |
| `moderation_listings_task` | при створенні / редагуванні | Перевірка оголошень на нецензурну лексику |

## Примусовий запуск оновлення курсів

Для тестування задачу можна запустити вручну:

```bash
docker compose exec celery celery -A config call apps.payment.tasks.fetch_currency_rates_task
```

Після виконання:

- у таблиці `currency_rate` з'явиться актуальний курс;
- ціни активних оголошень будуть перераховані відповідно до нового курсу.

---

# Фільтрація та пошук

Ендпоінт:

```text
/api/listings/
```

підтримує фільтрацію, пошук та сортування.

### Приклади

```text
?body_type=suv
```

```text
?fuel_type=electric
```

```text
?region=1
```

```text
?condition_type=new
```

```text
?price_usd_min=10000&price_usd_max=30000
```

```text
?mileage_max=50000
```

```text
?year_min=2019
```

```text
?search=BMW
```

```text
?ordering=price_usd
```

```text
?ordering=-created_at
```

Параметри можна комбінувати:

```text
/api/listings/?fuel_type=electric&year_min=2020&price_usd_max=30000
```

---

# Email сповіщення

Для тестування email використовується **Mailtrap**.

Листи не надсилаються на реальні поштові скриньки, а перехоплюються Mailtrap та доступні у його веб-інтерфейсі.

Система надсилає службові повідомлення:

- менеджеру після блокування оголошення після 3 невдалих спроб модерації;
- менеджеру при скарзі на оголошення;
- менеджеру при запиті на додавання нової марки автомобіля.

## Налаштування Mailtrap

1. Зареєструйтеся на Mailtrap.
2. Відкрийте `Email Testing`.
3. Перейдіть до `Sandboxes`.
4. Відкрийте потрібний Sandbox.
5. Перейдіть на вкладку `SMTP`.
6. Скопіюйте SMTP credentials у `.env`.

Приклад:

```env
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=your_mailtrap_user
EMAIL_HOST_PASSWORD=your_mailtrap_password
EMAIL_PORT=2525
```

---

# Документація API

Для автоматичної генерації документації використовується **DRF-Spectacular**.

Після запуску проєкту доступні:

| Інтерфейс | URL |
|-----------|-----|
| Swagger UI | `http://localhost:8000/api/docs/` |
| ReDoc | `http://localhost:8000/api/redoc/` |
| OpenAPI schema | `http://localhost:8000/api/schema/` |

## Swagger UI

Swagger UI дозволяє:

1. переглядати всі API endpoints;
2. бачити HTTP-методи та параметри;
3. переглядати схеми запитів та відповідей;
4. авторизуватися через JWT;
5. безпосередньо виконувати API-запити.

Відкрийте:

```text
http://localhost:8000/api/docs/
```

та використовуйте кнопку **Authorize** для авторизації.

---

# Тестування через Postman

Postman-колекція знаходиться у:

```text
postman/AutoRia Clone API.postman_collection.json
```

## Імпорт

1. Відкрийте Postman.
2. Натисніть **Import**.
3. Виберіть файл:

```text
postman/AutoRia Clone API.postman_collection.json
```

4. Створіть Environment.

### Environment variables

| Variable | Значення |
|----------|----------|
| `host` | `http://localhost:8000` |
| `access` | заповнюється автоматично |
| `refresh` | заповнюється автоматично |

Після виконання `login` access та refresh tokens автоматично зберігаються в Environment.

---

# Додавання нових ролей і permissions

Ролі та permissions є частиною архітектури системи та змінюються через **Django migrations**, а не через UI.

Це дозволяє зберігати зміни в системі permissions у коді та відтворювати їх на інших середовищах.

## Додавання нового permission

Створіть порожню міграцію:

```bash
docker compose exec app python manage.py makemigrations users --empty --name add_new_permission
```

У створеній міграції можна використати наступну структуру:

```python
def add_permission(apps, schema_editor):
    CustomPermission = apps.get_model('users', 'CustomPermission')
    RolePermissions = apps.get_model('users', 'RolePermissions')
    Role = apps.get_model('users', 'Role')

    perm = CustomPermission.objects.create(
        name='Назва permission',
        codename='codename_permission'
    )

    role = Role.objects.get(name='seller')

    RolePermissions.objects.create(
        role=role,
        permission=perm
    )
```

Після цього застосуйте міграцію:

```bash
docker compose exec app python manage.py migrate
```

Нові ролі додаються аналогічним способом через міграції.

---

# Docker

## Запуск

```bash
docker compose up -d --build
```

## Перевірка статусу

```bash
docker compose ps
```

## Логи Django

```bash
docker compose logs -f app
```

## Логи Celery

```bash
docker compose logs -f celery
```

## Логи всіх сервісів

```bash
docker compose logs -f
```

## Перезапуск Django

```bash
docker compose restart app
```

## Зупинка проекту

```bash
docker compose down
```

---

# Перевірка роботи

Після запуску можна перевірити API:

```bash
curl http://localhost:8000/api/listings/
```

Також перевірте статус контейнерів:

```bash
docker compose ps
```

Очікується, що основні сервіси знаходяться у статусі:

```text
Up
```

Після цього можна відкрити:

### API

```text
http://localhost:8000/api/listings/
```

### Swagger UI

```text
http://localhost:8000/api/docs/
```

### ReDoc

```text
http://localhost:8000/api/redoc/
```

---

# Ліцензія

Цей проєкт створений у навчальних цілях.