# AutoRia Clone — Car Marketplace API

REST API платформи для продажу автомобілів, побудований на Django REST Framework.

---

## Стек технологій

### Backend
- **Python 3.12** / **Django 5** / **Django REST Framework**
- **MySQL 8** — основна база даних
- **Redis** — брокер повідомлень для Celery
- **Celery + Celery Beat** — асинхронні задачі та планувальник

### Документація API
- **DRF-Spectacular** — генерація OpenAPI схеми
- **Swagger UI** — інтерактивна документація API
- **ReDoc** — альтернативний перегляд документації

### Автентифікація та безпека
- **JWT** (SimpleJWT) — токен-автентифікація

### Інтеграції
- **Mailtrap** — тестова відправка email
- **PrivatBank API** — курси валют

### Інфраструктура
- **Docker / Docker Compose** — контейнеризація

---

## Запуск проекту

### 1. Клонувати репозиторій

```bash
git clone <url>
cd python_test
```

### 2. Створити `.env` файл

Скопіюйте `.env_example` та заповніть своїми даними:

```bash
cp .env_example .env
```

Обов'язкові змінні:

```env
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

### 4. Застосувати міграції

```bash
docker compose exec app python manage.py migrate
```

### 5. Завантажити фікстури

```bash
docker compose exec app python manage.py loaddata regions.json
docker compose exec app python manage.py loaddata brands.json
docker compose exec app python manage.py loaddata car_models.json
```

### Опціонально: фікстури з оголошеннями

Для швидкого тестування можна завантажити `listings.json`.

Перед завантаженням необхідно:
1. Створити суперкористувача:
   ```bash
   docker compose exec app python manage.py createsuperuser
   ```
2. Зареєструвати через API двох продавців (вони повинні мати ID `2` і `3`)
3. Користувачу з ID `2` надати преміум-акаунт через ендпоінт `/api/users/me/premium/mock/` або через БД в таблиці profile,  в полі account_type вказати premium замість basic
4. Завантажити фікстуру:
   ```bash
   docker compose exec app python manage.py loaddata listings.json
   ```

---

## База даних

У проекті використовується **локальний volume** `./mysql:/var/lib/mysql` — всі дані зберігаються у папці `mysql` в корені проекту.

> **Важливо:** Папка `mysql/` додана в `.gitignore` і не повинна потрапляти в репозиторій.

### Підключення до БД ззовні (DataGrip, DBeaver, MySQL Workbench)

| Параметр | Значення | Примітка |
|----------|----------|----------|
| **Host** | `localhost` | або `127.0.0.1` |
| **Port** | `3307` | ⚠️ зовнішній порт, не 3306! |
| **User** | `user` | з `.env` (`MYSQL_USER`) |
| **Password** | `user` | з `.env` (`MYSQL_PASSWORD`) |
| **Database** | `car_shop_db` | з `.env` (`MYSQL_DATABASE`) |

> **Важливо:** Всередині Docker-мережі БД доступна за адресою `db:3306`. Ззовні (з вашого комп'ютера) — `localhost:3307`.

### Підключення як root

| Параметр | Значення |
|----------|----------|
| **User** | `root` |
| **Password** | `superuser` (з `.env`) |

### Перевірка підключення

```bash
# Через Docker
docker compose exec db mysql -u user -puser car_shop_db

# Через клієнт на хості (якщо встановлений MySQL)
mysql -h localhost -P 3307 -u user -puser car_shop_db
```

### Очищення даних БД

```bash
# Зупинити контейнери
docker compose down

# Видалити папку з даними
rm -rf ./mysql

# Запустити заново
docker compose up -d --build
```

---

## Порти

| Сервіс | Внутрішній порт | Зовнішній порт | Опис |
|--------|-----------------|----------------|------|
| app    | 8000            | 8000           | Django сервер |
| db     | 3306            | 3307           | MySQL |
| web    | 80              | 80             | Nginx для статики |
| redis  | 6379            | -              | Redis (не доступний ззовні) |

---

## Перевірка роботи

Після запуску переконайтеся, що всі сервіси працюють коректно:

```bash
# Перевірити статус контейнерів
docker compose ps
# Всі сервіси мають бути в статусі `Up`

# Перевірити логи
docker compose logs --tail=50

# Перевірити підключення до БД
docker compose exec app python manage.py dbshell
# Якщо підключилося — введіть \q для виходу

# Перевірити API
curl http://localhost:8000/api/listings/
```

---

## API Документація

Після запуску проекту документація доступна за адресами:

| Інтерфейс | URL |
|-----------|-----|
| Swagger UI | `http://localhost:8000/api/docs/` |
| ReDoc | `http://localhost:8000/api/redoc/` |

---

## Архітектура

Проєкт розділений на Django apps відповідно до доменів:

- `users` — користувачі, ролі, дозволи (permissions), профілі
- `listing` — оголошення та їхня модерація
- `cars` — бренди та моделі автомобілів
- `listing_stats` — статистика оголошень
- `payment` — курси валют та перерахунок цін
- `core` — спільні моделі, permissions та сервіси

Celery використовується для фонових задач та періодичного оновлення даних.

---

## Ролі і доступи

| Роль | Можливості |
|------|------------|
| **Buyer** | перегляд оголошень, скарги, створення першого оголошення |
| **Seller** | Все, що Buyer + створення/редагування оголошень, фото |
| **Manager** | Модерація оголошень, управління юзерами |
| **Admin (superuser)** | Повний доступ до всього |

> Покупець автоматично стає продавцем при створенні першого оголошення.  
> Базовий акаунт — одне активне оголошення. Преміум — необмежено.

---

## Преміум акаунт

Функціонал оплати реалізований як **заглушка** — без реальної платіжної системи.  
При натисканні на `POST /api/users/me/premium/mock/` преміум активується одразу без оплати на 30 днів. У реальному проекті цей ендпоінт замінюється на інтеграцію з платіжним сервісом.

---

## Основні ендпоінти

### Auth

| Метод | URL | Опис |
|-------|-----|------|
| POST | `/api/auth/register/` | Реєстрація |
| POST | `/api/auth/login/` | Логін |
| POST | `/api/auth/refresh/` | Оновлення токену |
| POST | `/api/auth/logout/` | Вихід з акаунта |

### Users

| Метод | URL                           | Опис | Доступ |
|-------|-------------------------------|------|--------|
| GET | `/api/users/`                 | Список юзерів | Admin / Manager |
| GET | `/api/users/me/`              | Свій акаунт | Всі |
| GET | `/api/users/<pk>/`            | Переглянути акаунт по ID | Всі |
| PATCH | `/api/users/me/update/`       | Оновити власний акаунт | Всі |
| DELETE | `/api/users/me/delete/`       | Видалити власний акаунт | Всі |
| DELETE | `/api/users/<pk>/delete/`     | Видалити акаунт по ID | Admin / Manager |
| POST | `/api/users/me/premium/mock/` | Отримати преміум акаунт | Buyer/Seller |
| PATCH | `/api/users/<pk>/block/`      | Заблокувати юзера | Admin / Manager |
| PATCH | `/api/users/<pk>/unblock/`    | Розблокувати юзера | Admin / Manager |
| PATCH | `/api/users/<pk>/manager/`    | Призначити менеджера | Admin |

### Listings

| Метод | URL | Опис | Доступ |
|-------|-----|------|--------|
| GET | `/api/listings/` | Всі активні оголошення | Публічно |
| GET | `/api/listings/<pk>/` | Одне оголошення | Публічно |
| GET | `/api/listings/regions/` | Список регіонів | Публічно |
| GET | `/api/listings/my/` | Мої оголошення | Seller |
| POST | `/api/listings/create/` | Створити оголошення | Buyer/Seller |
| PATCH | `/api/listings/update/<pk>/` | Редагувати оголошення | Seller (власник) |
| DELETE | `/api/listings/delete/<pk>/` | Зняти з продажу | Seller (власник) |
| POST | `/api/listings/<pk>/photos/` | Завантажити фото | Seller (власник) |
| DELETE | `/api/listings/photos/<pk>/` | Видалити фото | Seller (власник) |
| POST | `/api/listings/report-problem/<pk>/` | Скарга на оголошення | Залогінений |
| GET | `/api/listings/edit/` | Список оголошень у статусі Pending | Admin / Manager |
| PATCH | `/api/listings/moderation/<pk>/` | Модерувати оголошення | Admin / Manager |
| GET | `/api/listings/statistics/<pk>/` | Статистика оголошення | Premium Seller / Manager / Admin |

### Cars

| Метод | URL | Опис | Доступ |
|-------|-----|------|--------|
| GET | `/api/cars/brands/` | Список брендів | Публічно |
| GET | `/api/cars/brands/<pk>/` | Переглянути бренд | Публічно |
| GET | `/api/cars/models/` | Список моделей | Публічно |
| GET | `/api/cars/models/<pk>/` | Переглянути модель | Публічно |
| GET | `/api/cars/brands/<pk>/models/` | Моделі бренду | Публічно |
| POST | `/api/cars/request-brand/` | Запит на нову марку | Залогінений |
| POST | `/api/cars/brands/` | Створення бренду | Admin / Manager |
| PATCH / DELETE | `/api/cars/brands/<pk>/` | Редагування / видалення бренду | Admin |
| POST | `/api/cars/models/` | Створення моделі | Admin / Manager |
| PATCH / DELETE | `/api/cars/models/<pk>/` | Редагування / видалення моделі | Admin |

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

Ендпоінт `/api/listings/` підтримує наступні параметри:

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

Проект використовує **Mailtrap** для тестування email — всі листи перехоплюються і відображаються у веб-інтерфейсі Mailtrap, не потрапляючи на реальні поштові скриньки.

Листи відправляються:
- Менеджеру при блокуванні оголошення після 3 невдалих спроб модерації
- Менеджеру при скарзі на оголошення
- Менеджеру при запиті на нову марку авто

### Налаштування Mailtrap

1. Зареєструйтеся на [mailtrap.io](https://mailtrap.io)
2. Перейдіть у `Email Testing` → `Sandboxes` → `My Sandbox` → вкладка `SMTP`
3. Вкажіть отримані дані у `.env`:

```env
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_HOST_USER=your_mailtrap_user
EMAIL_HOST_PASSWORD=your_mailtrap_password
EMAIL_PORT=2525
```

---

## Додавання нових ролей і дозволів

Ролі та дозволи змінюються через міграції — це свідоме рішення для безпеки.

### Додати новий пермішин:

1. Створіть порожню міграцію:
   ```bash
   docker compose exec app python manage.py makemigrations users --empty --name add_new_permission
   ```

2. Заповніть її за зразком:
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

3. Застосуйте міграцію:
   ```bash
   docker compose exec app python manage.py migrate
   ```

---

## Тестування

### Postman колекція

Postman колекція знаходиться у файлі `postman/AutoRia Clone API.postman_collection.json`.

1. Імпортуйте колекцію в Postman
2. Створіть Environment зі змінними:

| Variable | Initial value |
|----------|---------------|
| `host` | `http://localhost:8000` |
| `access` | (заповниться автоматично) |
| `refresh` | (заповниться автоматично) |

Після виконання `login` access та refresh tokens автоматично зберігаються в Environment.

### Swagger UI

Найзручніший спосіб тестування — Swagger UI:
1. Відкрийте `http://localhost:8000/api/docs/`
2. Авторизуйтеся через кнопку `Authorize`
3. Тестуйте ендпоїнти прямо в інтерфейсі

---

## Команди для Docker

```bash
# Запустити проект
docker compose up -d --build

# Перевірити статус
docker compose ps

# Переглянути логи
docker compose logs -f app
docker compose logs -f celery

# Перезапустити окремий сервіс
docker compose restart app

# Зупинити проект
docker compose down

# Очистити всі дані (контейнери + volume)
docker compose down -v
rm -rf ./mysql
```

---

## Поширені проблеми та рішення

### Порт 8000 або 3307 вже зайнятий

**Симптом:** `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Рішення:**
```bash
# Знайти контейнер, який займає порт
docker ps --filter "publish=8000"

# Зупинити його
docker stop <container_name>

# Або зупинити всі контейнери
docker stop $(docker ps -q)
```

### MySQL не запускається

**Симптом:** `--initialize specified but the data directory has files in it`

**Рішення:**
```bash
docker compose down
rm -rf ./mysql
docker compose up -d --build
```
---

## Ліцензія

Цей проект створений у навчальних цілях.