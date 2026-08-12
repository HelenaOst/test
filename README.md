# AutoRia Clone — Car Marketplace API
REST API платформи для продажу автомобілів, побудований на Django REST Framework.

---

## Стек технологій

- **Python 3.12** / **Django 6** / **Django REST Framework**
- **MySQL 8** — основна база даних
- **Redis** — брокер повідомлень для Celery
- **Celery + Celery Beat** — асинхронні задачі та планувальник
- **Docker / Docker Compose** — контейнеризація
- **JWT** (SimpleJWT) — автентифікація
- **Mailtrap** — тестова відправка email
- **PrivatBank API** — курси валют

---

## Запуск проекту

### 1. Клонувати репозиторій

```bash
git clone <url>
cd python_test
```

### 2. Створити `.env` файл

Скопіюй `.env_example` і заповни своїми даними:

```bash
cp .env_example .env
```

Обов'язкові змінні:

```
MYSQL_USER=user
MYSQL_PASSWORD=user
MYSQL_ROOT_PASSWORD=superuser
MYSQL_DATABASE=car_shop_db
MYSQL_HOST=db
MYSQL_PORT=3306

EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=your_mailtrap_user
EMAIL_HOST_PASSWORD=your_mailtrap_password
EMAIL_PORT=2525

MANAGERS_EMAIL=moderation@automarket.com
```



### 3. Запустити Docker

```bash
docker compose up -d --build
```

Після запуску переконайтеся, що всі контейнери працюють:

```bash
docker compose ps
```
### База даних

У проекті використовується **локальний volume** `./mysql:/var/lib/mysql`, тому всі дані зберігаються у папці `mysql` в корені проекту.
**Важливо:** Папка `mysql/` додана в `.gitignore` і не повинна потрапляти в репозиторій.

### Якщо потрібно очистити дані БД

```bash
# Зупинити контейнери
docker compose down

# Видалити папку з даними
rm -rf ./mysql

# Запустити заново
docker compose up -d --build
```

## Порти

| Сервіс | Внутрішній порт | Зовнішній порт | Опис |
|--------|-----------------|----------------|------|
| app    | 8000            | 8000           | Django сервер |
| db     | 3306            | 3307           | MySQL |
| web    | 80              | 80             | Nginx для статики |
| redis  | 6379            | -              | Redis (не доступний ззовні) |

Після запуску переконайтеся, що всі контейнери працюють:

```bash
docker compose ps
```
Якщо порти зайняті, зупиніть інші Docker проекти або змініть порти у `.env` та `docker-compose.yml`.

### 4. Застосувати міграції

 В проекті використовується локальний volume ./mysql:/var/lib/mysql, а не Docker volume. 
 Це означає, що дані зберігаються прямо у файловій системі в папці mysql всередині проекту.

```bash
docker exec -it python_test-app-1 python manage.py migrate
```

### 5. Завантажити фікстури (fixtures)

```bash
docker compose exec app python manage.py loaddata regions.json
docker compose exec app python manage.py loaddata brands.json
docker compose exec app python manage.py loaddata car_models.json
```

### Опціонально: фікстури з оголошеннями

Для швидкого тестування можна завантажити `listings.json`.

Перед завантаженням необхідно:
1. Створити суперюзера через `createsuperuser`.
2. Зареєструвати через API двох продавців. Вони повинні мати ID `2` і `3`, оскільки `listings.json` містить посилання на цих користувачів.

```bash
docker compose exec app python manage.py createsuperuser
docker compose exec app python manage.py loaddata listings.json
```
### Тепер можна реєструвати інших юзерів на тести через API

## API Документація

Після запуску проекту документація доступна за адресами:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Архітектура

Проєкт розділений на Django apps відповідно до доменів:

- `users` — користувачі, ролі, дозволи (permissions), профілі
- `listing` — оголошення та їхня модерація
- `cars` — бренди та моделі автомобілів
- `listing_stats` — статистика оголошень
- `payment` — курси валют та перерахунок цін
- `core` — спільні моделі, permissions та сервіси

Celery використовується для фонових задач та періодичного оновлення даних.

## Ролі і доступи

| Роль                  | Можливості |
|-----------------------|-----------|
| **Buyer**             | перегляд оголошень, скарги, створення першого оголошення |
| **Seller**            | Все що Buyer + створення/редагування оголошень, фото |
| **Manager**           | Модерація оголошень, управління юзерами |
| **Admin (superuser)** | Повний доступ до всього |

> Покупець автоматично стає продавцем при створенні першого оголошення.
> Базовий акаунт — одне активне оголошення. Преміум — необмежено.

---
## Преміум акаунт

Функціонал оплати реалізований як **заглушка** — без реальної платіжної системи.
При натисканні на `POST /api/users/profile/upgrade/` преміум активується одразу
без оплати на 30 днів. У реальному проекті цей ендпоінт замінюється на інтеграцію з платіжним сервісом.

## Основні ендпоінти

### Auth
| Метод | URL                     | Опис              |
|-------|-------------------------|-------------------|
| POST | `/api/auth/register/`   | Реєстрація        |
| POST | `/api/auth/login/`      | Логін             |
| POST | `/api/auth/refresh/`    | Оновлення токену  |
| POST | `/api/auth/logout/`     | Вихід з акаунта   |

### Users
| Метод  | URL                        | Опис                     | Доступ            |
|--------|----------------------------|--------------------------|-------------------|
| GET    | `/api/users/`              | Список юзерів            | Admin / Manager   |
| GET    | `/api/users/me/`           | Свій акаунт              | Всі               |
| GET    | `/api/users/<pk>/`         | Переглянути акаунт по ID | Всі               |
| PATCH  | `/api/users/me/update/`    | Оновити власний акаунт   | Всі               |
| DELETE | `/api/users/me/delete/`    | Видалити власний акаунт  | Всі               |
| DELETE | `/api/users/<pk>/delete/`  | Видалити акаунт по ID    | Admin / Manager   |
| POST   | `/api/users/premium/mock/` | Отримати преміум акаунт  | Buyer/Seller      |
| PATCH  | `/api/users/<pk>/block/`   | Заблокувати юзера        | Admin / Manager   |
| PATCH  | `/api/users/<pk>/unblock/` | Розблокувати юзера       | Admin / Manager   |
| PATCH  | `/api/users/<pk>/manager/` | Призначити менеджера     | Admin             |

### Listings
| Метод | URL | Опис                               | Доступ |
|-------|-----|------------------------------------|--------|
| GET | `/api/listings/` | Всі активні оголошення             | Публічно |
| GET | `/api/listings/<pk>/` | Одне оголошення                    | Публічно |
| GET | `/api/listings/regions/` | Список регіонів                    | Публічно |
| GET | `/api/listings/my/` | Мої оголошення                     | Seller |
| POST | `/api/listings/create/` | Створити оголошення                | Buyer/Seller |
| PATCH | `/api/listings/update/<pk>/` | Редагувати оголошення              | Seller (власник) |
| DELETE | `/api/listings/delete/<pk>/` | Зняти з продажу                    | Seller (власник) |
| POST | `/api/listings/<pk>/photos/` | Завантажити фото                   | Seller (власник) |
| DELETE | `/api/listings/photos/<pk>/` | Видалити фото                      | Seller (власник) |
| POST | `/api/listings/report-problem/<pk>/` | Скарга на оголошення               | Залогінений |
| GET | `/api/listings/edit/` | Список оголошень в статусі Pending | Admin / Manager |
| PATCH | `/api/listings/moderation/<pk>/` | Модерувати оголошення              | Admin / Manager |
| GET | `/api/listings/statistics/<pk>/` | Статистика оголошення | Premium Seller / Manager / Admin  |



### Cars
| Метод             | URL                             | Опис                           | Доступ          |
|-------------------|---------------------------------|--------------------------------|-----------------|
| GET               | `/api/cars/brands/`             | Список брендів                 | Публічно        |
| GET               | `/api/cars/brands/<pk>/`        | Переглянути бренд              | Публічно        |
| GET               | `/api/cars/models/`             | Список моделей                 | Публічно        |
| GET               | `/api/cars/models/<pk>/`        | Переглянути модель             | Публічно        |
| GET               | `/api/cars/brands/<pk>/models/` | Моделі бренду                  | Публічно        |
| POST              | `/api/cars/request-brand/`      | Запит на нову марку            | Залогінений     |
| POST              | `/api/cars/brands/<pk>/`        | Створення бренду               | Admin / Manager |
| PATCH/DELETE | `/api/cars/brands/<pk>/`        | Редагування / видалення бренду | Admin           |
| POST              | `/api/cars/models/`             | Створення моделі               | Admin / Manager |
| PATCH/DELETE | `/api/cars/models/<pk>/`        | Редагування / видалення моделі | Admin           |

### Payment
| Метод | URL | Опис | Доступ |
|-------|-----|------|--------|
| GET | `/api/payment/rate/` | Актуальний курс валют | Публічно |

---

## Celery Tasks

| Task | Розклад | Опис |
|------|---------|------|
| `fetch_currency_rates_task` | Щодня о 9:00 | Оновлення курсів з ПриватБанку |
| `update_listings_prices_task` | Після оновлення курсів | Перерахунок цін оголошень |
| `moderation_listings_task` | При створенні/редагуванні | Перевірка на нецензурну лексику |

---

## Фільтрація і пошук

Ендпоінт `/api/listings/` підтримує:

```
?body_type=suv
?fuel_type=electric
?region=1
?condition_type=new
?price_usd_min=10000&price_usd_max=30000
?mileage_max=50000
?year_min=2019
?search=BMW
?ordering=price_usd
?ordering=-created_at
```

---

## Email сповіщення

Проект використовує **Mailtrap** для тестування email — всі листи перехоплюються
і відображаються у веб-інтерфейсі Mailtrap, не потрапляючи на реальні поштові скриньки.

Листи відправляються:
- Менеджеру при блокуванні оголошення після 3 невдалих спроб модерації
- Менеджеру при скарзі на оголошення
- Менеджеру при запиті на нову марку авто

### Налаштування Mailtrap

Для перегляду тестових листів необхідно створити безкоштовний акаунт у Mailtrap та взяти SMTP credentials із відповідного Email Sandbox.

1. Зареєструйся на [mailtrap.io](https://mailtrap.io)
2. Перейди у `Email Testing` → `Sandboxes` → `My Sandbox` → вкладка `SMTP`
3. Перевір, чи описані credentials у `.env`:

```
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=your_mailtrap_user
EMAIL_HOST_PASSWORD=your_mailtrap_password
EMAIL_PORT=2525
```
## Додавання нових ролей (roles) і дозволів (permissions)

Ролі та дозволи є частиною архітектури системи і змінюються через міграції,
а не через UI — це свідоме рішення для безпеки.

### Щоб додати новий пермішин:

1. Створи нову порожню міграцію:
```bash
python manage.py makemigrations users --empty --name add_new_permission
```

2. Заповни її за зразком існуючої `0002_seed_roles_and_permissions.py`:
```python
def add_permission(apps, schema_editor):
    CustomPermission = apps.get_model('users', 'CustomPermission')
    RolePermissions = apps.get_model('users', 'RolePermissions')
    Role = apps.get_model('users', 'Role')

    perm = CustomPermission.objects.create(
        name='Назва пермішину',
        codename='codename_permission'
    )
    role = Role.objects.get(name='seller')
    RolePermissions.objects.create(role=role, permission=perm)
```

3. Застосуй міграцію:
```bash
docker exec -it python_test-app-1 python manage.py migrate
```

### Щоб додати нову роль — той самий підхід через міграцію.

---

## Тестування
Postman колекція з тестовими запитами знаходиться у файлі `postman/AutoRia Clone API.postman_collection.json`.

Імпортуй в Postman і встанови змінну `host = http://localhost:8888`.

Імпортуй `AutoRia Clone API.postman_collection.json` у Postman.

Перед запуском запитів створи Environment з такими змінними:

| Variable | Initial value |
|---|---|
| `host` | `http://localhost:8888` |
| `access` | |
| `refresh` | |

Після виконання `login` access та refresh tokens
автоматично зберігаються в Environment.


### Перегляд логів

```bash
docker compose logs -f app
```

### Зупинка проекту

```bash
docker compose down
```