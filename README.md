# AutoRia Clone — Car Marketplace API
Навчальний/тестовий REST API для платформи продажу автомобілів.

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
docker-compose up -d --build
```

### 4. Застосувати міграції

```bash
docker exec -it python_test-app-1 python manage.py migrate
```

### 5. Завантажити фікстури

```bash
docker exec -it python_test-app-1 python manage.py loaddata regions.json
docker exec -it python_test-app-1 python manage.py loaddata brands.json
docker exec -it python_test-app-1 python manage.py loaddata car_models.json
```

### Опціонально: fixtures з оголошеннями

Для швидкого тестування можна завантажити `listings.json`.

Перед завантаженням необхідно:
1. Створити суперюзера через `createsuperuser`.
2. Зареєструвати через API двох продавців.
3. Вони повинні мати ID `2` і `3`, оскільки `listings.json` містить посилання на цих користувачів.

```bash
docker exec -it python_test-app-1 python manage.py createsuperuser
docker exec -it python_test-app-1 python manage.py loaddata listings.json
```
### Тепер можна реєструвати інших юзерів на тести через API

## Архітектура

Проєкт розділений на Django apps відповідно до доменів:

- `users` — користувачі, ролі, permissions, профілі
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

## Основні ендпоінти

### Auth
| Метод | URL | Опис             |
|-------|-----|------------------|
| POST | `/api/auth/register/` | Реєстрація       |
| POST | `/api/auth/login/` | Логін            |
| POST | `/api/auth/refresh/` | Оновлення токену |
| POST | `/api/auth/logout/` | Вихід з аккаунта |

### Users
| Метод | URL | Опис | Доступ          |
|-------|-----|------|-----------------|
| GET | `/api/users/` | Список юзерів | Admin / Manager |
| GET | `/api/users/me/` | Свій акаунт | Всі             |
| PATCH | `/api/users/me/update/` | Оновити акаунт | Всі             |
| DELETE | `/api/users/me/delete/` | Видалити акаунт | Всі             |
| POST | `/api/users/profile/upgrade/` | Преміум акаунт | Buyer/Seller    |
| PATCH | `/api/users/<pk>/block/` | Заблокувати юзера | Admin / Manager       |
| PATCH | `/api/users/<pk>/unblock/` | Розблокувати юзера | Admin / Manager        |
| PATCH | `/api/users/<pk>/manager/` | Призначити менеджера | Admin       |

### Listings
| Метод | URL | Опис                         | Доступ |
|-------|-----|------------------------------|--------|
| GET | `/api/listings/` | Всі активні оголошення       | Публічно |
| GET | `/api/listings/<pk>/` | Одне оголошення              | Публічно |
| GET | `/api/listings/regions/` | Список регіонів              | Публічно |
| GET | `/api/listings/my/` | Мої оголошення               | Seller |
| POST | `/api/listings/create/` | Створити оголошення          | Buyer/Seller |
| PATCH | `/api/listings/update/<pk>/` | Редагувати оголошення        | Seller (власник) |
| DELETE | `/api/listings/delete/<pk>/` | Зняти з продажу              | Seller (власник) |
| POST | `/api/listings/<pk>/photos/` | Завантажити фото             | Seller (власник) |
| DELETE | `/api/listings/photos/<pk>/` | Видалити фото                | Seller (власник) |
| POST | `/api/listings/report-problem/<pk>/` | Скарга на оголошення         | Залогінений |
| GET | `/api/listings/edit/` | Оголошення в статусі Pending | Admin / Manager |
| PATCH | `/api/listings/moderation/<pk>/` | Модерувати оголошення        | Admin / Manager |

### Statistics (Premium Seller / Manager / Admin)
| Метод | URL | Опис |
|-------|-----|------|
| GET | `/api/listings/statistics/<pk>/` | Статистика оголошення |

### Cars
| Метод             | URL | Опис                           | Доступ          |
|-------------------|-----|--------------------------------|-----------------|
| GET               | `/api/cars/brands/` | Список брендів                 | Публічно        |
| GET               | `/api/cars/models/` | Список моделей                 | Публічно        |
| GET               | `/api/cars/brands/<pk>/models/` | Моделі бренду                  | Публічно        |
| POST              | `/api/cars/request-brand/` | Запит на нову марку            | Залогінений     |
| POST              | `/api/cars/brands/<pk>/` | Створення бренду               | Admin / Manager |
| PATCH/DELETE | `/api/cars/brands/<pk>/` | Редагування / видалення бренду | Admin           |
| POST              | `/api/cars/models/` | Створення моделі               | Admin / Manager |
| PATCH/DELETE | `/api/cars/models/<pk>/` | Редагування / видалення моделі | Admin           |

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

Проект використовує **Mailtrap** для тестування email.

Для перегляду тестових листів необхідно створити безкоштовний акаунт у Mailtrap та взяти SMTP credentials із відповідного Email Sandbox.

Листи відправляються:
- Менеджеру при блокуванні оголошення після 3 невдалих спроб модерації
- Менеджеру при скарзі на оголошення
- Менеджеру при запиті на нову марку авто
```
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=your_mailtrap_user
EMAIL_HOST_PASSWORD=your_mailtrap_password
EMAIL_PORT=2525
```

---

## Тестування

Postman колекція з усіма замоканими запитами знаходиться у файлі `car_shop.postman_collection.json`.

Імпортуй в Postman і встанови змінну `host = http://localhost:8888`.


### Перегляд логів

```bash
docker-compose logs -f app
```

### Зупинка проекту

```bash
docker-compose down
```