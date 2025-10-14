# AI Tutor Backend

Backend система для образовательной платформы с ИИ-тьютором через Telegram бота. Система управляет студентами, материалами курсов и предоставляет API для интеграции с внешними системами.

## 🚀 Возможности

- **FastAPI** с автоматической документацией
- **SQLAlchemy 2.0** с асинхронной поддержкой (без ручного SQL)
- **PostgreSQL** база данных
- **Alembic** для миграций
- **fastapi-admin** админ панель
- **LOCAL/PROD** переключение окружений
- **Telegram бот** интеграция
- **Система курсов** с модулями и уроками
- **3 типа материалов**: лекционные, задания, методические
- **Расписание занятий** с разными типами
- **Система заданий** студентов

## 📁 Структура проекта

```
ai-tutor-platform/
├── app/
│   ├── main.py                 # FastAPI приложение
│   ├── core/
│   │   ├── config.py          # Конфигурация LOCAL/PROD
│   │   └── database.py        # SQLAlchemy async setup
│   ├── models/
│   │   └── education.py       # Все модели как Python классы
│   ├── api/                   # REST API endpoints
│   └── admin/                 # fastapi-admin настройка
├── alembic/                   # Миграции
│   ├── env.py                 # Async Alembic конфигурация
│   ├── script.py.mako         # Шаблон миграций
│   └── versions/              # Папка для версий миграций
├── requirements.txt           # Зависимости
├── env.example               # Пример переменных окружения
└── alembic.ini               # Конфигурация Alembic
```

## 🛠 Установка и запуск

### Требования

- **Python 3.11+**
- **PostgreSQL** (локально или удаленно)
- **Git** (локальный репозиторий)

### Быстрый старт

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Создайте .env файл:**
   ```bash
   copy env.example .env
   ```
   
   Отредактируйте `.env` файл:
   ```env
   ENVIRONMENT=LOCAL
   DATABASE_URL_LOCAL=postgresql+asyncpg://user:pass@localhost:5432/ai_tutor_local
   DATABASE_URL_PROD=postgresql+asyncpg://user:pass@host:5432/ai_tutor_prod
   ```

3. **Создайте первую миграцию:**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

4. **Примените миграции:**
   ```bash
   alembic upgrade head
   ```

5. **Запустите приложение:**
   ```bash
   python -m app.main
   # или
   uvicorn app.main:app --reload
   ```

6. **Откройте приложение:**
   - API: http://localhost:8000
   - Документация: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## 🔧 Конфигурация

### Переменные окружения

Основные переменные в `.env`:

```env
# Окружение (LOCAL/PROD)
ENVIRONMENT=LOCAL

# База данных
DATABASE_URL_LOCAL=postgresql+asyncpg://user:pass@localhost:5432/ai_tutor_local
DATABASE_URL_PROD=postgresql+asyncpg://user:pass@host:5432/ai_tutor_prod

# Приложение
APP_NAME=AI Tutor Backend
APP_VERSION=1.0.0
DEBUG=True

# Безопасность
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Логирование
LOG_LEVEL=INFO
```

### Окружения

- **LOCAL**: Локальная разработка с отладочной информацией
- **PROD**: Продакшн с отключенной документацией и дополнительной безопасностью

### Переключение между базами данных

Система автоматически переключается между локальной и продакшн базой данных в зависимости от переменной `ENVIRONMENT`:

- `ENVIRONMENT=LOCAL` → использует `DATABASE_URL_LOCAL`
- `ENVIRONMENT=PROD` → использует `DATABASE_URL_PROD`

## 📚 API Документация

После запуска приложения доступна автоматическая документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🗄 База данных

### Основные модели

- **Student**: Студенты платформы
- **CourseProgram**: Образовательные программы
- **Stream**: Потоки обучения
- **Module**: Модули курса (разделы)
- **Lesson**: Темы внутри модулей
- **CourseMaterial**: Материалы для уроков (3 типа: лекционные, задания, методические)
- **Message**: Сообщения от студентов
- **BotResponse**: Ответы бота
- **Assignment**: Задания студентов
- **Schedule**: Расписание занятий с типами
- **Prompt**: Промпты для ИИ

### Типы материалов

1. **Лекционные материалы** (`lecture`) - информация для слушателя
2. **Задания** (`assignment`) - тестирования, практические, самостоятельная работа
3. **Методические материалы** (`methodical`) - критерии проверки и оценки заданий

### Типы занятий

1. **Лекционная работа** (`lecture`) - дата + время начала и окончания
2. **Практическая работа** (`practical`) - дата + время начала и окончания
3. **Самостоятельная работа** (`independent`) - только дата (без времени)

### Миграции

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Description"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

## 🤖 ИИ-тьютор и Telegram бот

### Промпты для ИИ

Система хранит промпты в таблице `prompts` с типами:
- **FAQ** (`faq`) - для ответов на часто задаваемые вопросы
- **MATERIALS** (`materials`) - для работы с материалами курса

### Telegram бот интеграция

- Сообщения студентов сохраняются в таблице `messages`
- Ответы бота сохраняются в таблице `bot_responses`
- Поддержка `telegram_user_id` для связи студентов с Telegram

### API для интеграции

Система предоставляет API endpoints для:
- Управления студентами
- Работы с материалами курсов
- Обработки сообщений и ответов бота
- Управления расписанием
- Работы с заданиями студентов

## 🧪 Тестирование

```bash
# Запуск тестов
pytest

# С покрытием
pytest --cov=app
```

## 📦 Развертывание

### Локальная разработка

1. Установите `ENVIRONMENT=LOCAL` в `.env`
2. Настройте локальную PostgreSQL базу данных
3. Примените миграции: `alembic upgrade head`
4. Запустите: `python -m app.main`

### Продакшн

1. Установите `ENVIRONMENT=PROD` в `.env`
2. Настройте продакшн базу данных в `DATABASE_URL_PROD`
3. Примените миграции: `alembic upgrade head`
4. Используйте reverse proxy (nginx)
5. Настройте SSL сертификаты

## 🤝 Разработка

### Структура кода

- **app/core/**: Основная конфигурация (config.py, database.py)
- **app/models/**: SQLAlchemy модели (education.py)
- **app/api/**: API роутеры (будут добавлены)
- **app/admin/**: fastapi-admin настройка (будет добавлена)

### Ключевые принципы

1. **SQLAlchemy модели** создают структуру БД автоматически (никакого ручного SQL)
2. **Миграции через Alembic** для версионирования схемы
3. **Локальный Git проект** (не GitHub до особых указаний)
4. **Возможность переключения** между локальной и корпоративной БД
5. **API-first подход** для интеграции с другими системами
6. **fastapi-admin** для удобного управления данными

### Стиль кода

```bash
# Форматирование
black app/
isort app/

# Линтинг
flake8 app/
```

## 📝 Лицензия

MIT License

## 🆘 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте документацию API
2. Посмотрите логи приложения
3. Проверьте конфигурацию базы данных
4. Убедитесь, что миграции применены

---

**AI Tutor Backend** - Backend для образовательной платформы с ИИ-тьютором 🎓🤖