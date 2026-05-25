Система технічної підтримки (Тікетинг)# Система технічної підтримки (Тікетинг)

![CI Pipeline](https://github.com/Nazar89/support-system/actions/workflows/ci-pipeline.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Nazar89_support-system&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Nazar89_support-system)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Nazar89_support-system&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Nazar89_support-system)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Nazar89_support-system&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Nazar89_support-system)

REST API система технічної підтримки з веб-інтерфейсом. Реалізована як **модульний моноліт** на Python (FastAPI + SQLite).

---

## Зміст

- [Опис проєкту](#опис-проєкту)
- [Архітектура](#архітектура)
- [Модулі](#модулі)
- [Ролі та права доступу](#ролі-та-права-доступу)
- [Запуск](#запуск)
- [Тестування](#тестування)
- [CI/CD](#cicd)
- [Структура репозиторію](#структура-репозиторію)

---

## Опис проєкту

Система дозволяє користувачам подавати звернення (тікети) до служби підтримки, вести переписку з операторами, переглядати FAQ. Адміністратори мають доступ до статистики і управління користувачами.

Ключовий функціонал:
- Реєстрація та авторизація (токен-базована)
- Створення тікетів і зміна їх статусів
- Переписка всередині тікета
- База FAQ (питання-відповідь)
- Адмін-панель зі статистикою
- Веб-інтерфейс (single-page, HTML/CSS/JS)

---

## Архітектура

**Модульний моноліт** — весь застосунок запускається як єдиний процес, але логічно розділений на незалежні модулі. Кожен модуль містить власні: `models.py`, `routes.py`, `schemas.py`, `service.py`.

Патерни та принципи:
- **Repository pattern** — сервіси ізолюють логіку від роутерів
- **Dependency Injection** — FastAPI Depends для бази і автентифікації
- **SOLID** — кожен модуль має єдину відповідальність

---

## Модулі

| Модуль | Опис |
|--------|------|
| `auth` | Вхід користувача, видача Bearer-токена |
| `users` | Реєстрація, перегляд профілю, зміна ролей |
| `tickets` | Створення тікетів, перегляд, зміна статусів |
| `messages` | Повідомлення всередині тікета |
| `faq` | Часті питання: читання, додавання, видалення |
| `admin` | Статистика системи (лише для адміна) |

---

## Ролі та права доступу

| Дія | user | operator | admin |
|-----|:----:|:--------:|:-----:|
| Реєстрація / вхід | ✅ | ✅ | ✅ |
| Створення тікета | ✅ | ✅ | ✅ |
| Перегляд своїх тікетів | ✅ | ✅ | ✅ |
| Перегляд всіх тікетів | ❌ | ✅ | ✅ |
| Зміна статусу тікета | ❌ | ✅ | ✅ |
| Надсилання повідомлень | ✅ | ✅ | ✅ |
| Перегляд FAQ | ✅ | ✅ | ✅ |
| Управління FAQ | ❌ | ❌ | ✅ |
| Управління користувачами | ❌ | ❌ | ✅ |
| Перегляд статистики | ❌ | ❌ | ✅ |

Статуси тікета: `open` → `in_progress` → `closed`

---

## Запуск

### Вимоги

- Python 3.13+
- pip

### Встановлення

```bash
git clone https://github.com/Nazar89/support-system.git
cd support-system
pip install -r requirements-dev.txt
```

### Запуск застосунку

```bash
uvicorn app.main:app --reload
```

- **Веб-інтерфейс:** http://127.0.0.1:8000
- **API документація:** http://127.0.0.1:8000/docs

### Початковий адміністратор
Show Image
Show Image
Show Image
Show Image
REST API система технічної підтримки з веб-інтерфейсом. Реалізована як модульний моноліт на Python (FastAPI + SQLite).
Зміст

Опис проєкту
Архітектура
Модулі
Ролі та права доступу
Запуск
Тестування
CI/CD
Структура репозиторію

Опис проєкту
Система дозволяє користувачам подавати звернення (тікети) до служби підтримки, вести переписку з операторами, переглядати FAQ. Адміністратори мають доступ до статистики і управління користувачами.
Ключовий функціонал: реєстрація та авторизація (токен-базована), створення тікетів і зміна їх статусів, переписка всередині тікета, база FAQ, адмін-панель зі статистикою, веб-інтерфейс (single-page, HTML/CSS/JS).
Архітектура
Модульний моноліт — весь застосунок запускається як єдиний процес, але логічно розділений на незалежні модулі. Кожен модуль містить власні models.py, routes.py, schemas.py, service.py.
Патерни та принципи: Repository pattern — сервіси ізолюють логіку від роутерів. Dependency Injection — FastAPI Depends для бази і автентифікації. SOLID — кожен модуль має єдину відповідальність.
Модулі
auth — вхід користувача, видача Bearer-токена. users — реєстрація, перегляд профілю, зміна ролей. tickets — створення тікетів, перегляд, зміна статусів. messages — повідомлення всередині тікета. faq — часті питання: читання, додавання, видалення. admin — статистика системи (лише для адміна).
Ролі та права доступу
user може: реєстрація/вхід, створення тікета, перегляд своїх тікетів, надсилання повідомлень, перегляд FAQ. operator додатково може: перегляд всіх тікетів, зміна статусу тікета. admin може все вище плюс: управління FAQ, управління користувачами, перегляд статистики.
Статуси тікета: open → in_progress → closed
Запуск
Вимоги: Python 3.13+, pip.
Встановлення: git clone https://github.com/Nazar89/support-system.git потім cd support-system потім pip install -r requirements-dev.txt
Запуск: uvicorn app.main:app --reload
Веб-інтерфейс: http://127.0.0.1:8000 API документація: http://127.0.0.1:8000/docs
Початковий адміністратор: username: admin, password: admin123
Тестування
Запуск тестів: pytest tests/ -v
Запуск з покриттям: pytest tests/ --cov=app --cov-report=html --cov-report=xml -v
Статистика: 132 тести, покриття 98.4%, Bugs 0, Maintainability A.
Структура: conftest.py — фікстури, test_auth.py — 15 тестів, test_users.py — 19 тестів, test_tickets.py — 26 тестів, test_messages.py — 18 тестів, test_faq.py — 21 тест, test_admin.py — 13 тестів, test_security.py — 20 тестів.
CI/CD
Пайплайн запускається автоматично при кожному коміті до main. Кроки: Checkout, Setup Python 3.13, Install dependencies, Run tests, Upload artifacts, SonarCloud scan.
Артефакти після кожного запуску: coverage-html-report, coverage-xml-report, junit-test-report.
Структура репозиторію
app/core/security.py — автентифікація, токени, хешування. app/modules/ — admin, auth, faq, messages, tickets, users. app/database.py — підключення SQLite. app/main.py — точка входу FastAPI. static/index.html — веб-інтерфейс. tests/ — 132 тести. .github/workflows/ci-pipeline.yml — GitHub Actions. sonar-project.properties — конфігурація SonarCloud. pytest.ini — конфігурація pytest. setup.cfg — конфігурація coverage. requirements.txt і requirements-dev.txt — залежності.

---

## Тестування

```bash
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html --cov-report=xml -v
```

| Показник | Значення |
|----------|----------|
| Кількість тестів | 132 |
| Покриття коду | 98.4% |
| Bugs | 0 |
| Maintainability | A |

---

## CI/CD

Пайплайн запускається автоматично при кожному коміті до `main`.

Кроки: Checkout → Setup Python 3.13 → Install dependencies → Run tests → Upload artifacts → SonarCloud scan

Артефакти після кожного запуску:
- `coverage-html-report` — HTML звіт покриття
- `coverage-xml-report` — XML звіт для SonarCloud
- `junit-test-report` — JUnit XML звіт тестів

---

## Структура репозиторію

**app/** — основний код застосунку
- `app/core/security.py` — автентифікація, токени, хешування
- `app/modules/admin/` — статистика системи
- `app/modules/auth/` — авторизація
- `app/modules/faq/` — FAQ
- `app/modules/messages/` — повідомлення
- `app/modules/tickets/` — тікети
- `app/modules/users/` — користувачі
- `app/database.py` — підключення SQLite
- `app/main.py` — точка входу FastAPI

**static/** — фронтенд
- `static/index.html` — веб-інтерфейс

**tests/** — 132 тести (pytest)

**.github/workflows/ci-pipeline.yml** — GitHub Actions пайплайн

**sonar-project.properties** — конфігурація SonarCloud

**pytest.ini** — конфігурація pytest

**setup.cfg** — конфігурація coverage

**requirements.txt** — залежності

**requirements-dev.txt** — залежності для розробки

## Додаток
логін і пароль для адмін аккаунту

логін: admin

пароль: admin123