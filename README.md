# 🎓 TutorAI - Образовательная платформа с ИИ-тьютором

Современная backend система для образовательной платформы с ИИ-тьютором через Telegram бота. Управляет студентами, материалами курсов, расписанием и предоставляет REST API для интеграции с внешними системами.

## ✨ Ключевые возможности

- 🤖 **ИИ-тьютор** через Telegram бота
- 📚 **Образовательная система** с программами, потоками, модулями и уроками
- 📝 **3 типа материалов**: лекционные, задания, методические
- 📅 **Расписание занятий** с разными типами (лекции, практика, самостоятельная работа)
- 👥 **Управление студентами** с Telegram интеграцией
- 📊 **Админ панель** для управления всеми данными
- 🔄 **Система заданий** с отслеживанием статусов
- 💬 **История сообщений** и ответов ИИ-тьютора

## 🏗️ Технологический стек

- **FastAPI** - современный веб-фреймворк с автоматической документацией
- **SQLAlchemy 2.0** - ORM с асинхронной поддержкой
- **PostgreSQL** - реляционная база данных
- **Alembic** - система миграций
- **SQLAdmin** - админ панель
- **Docker** - контейнеризация
- **Pydantic** - валидация данных

## 📁 Структура проекта

```
TutorAI/
├── app/                          # Основное приложение
│   ├── main.py                   # Точка входа FastAPI
│   ├── core/                     # Ядро приложения
│   │   ├── config.py            # Конфигурация
│   │   └── database.py          # Настройка БД
│   ├── models/                   # Модели данных
│   │   └── education.py         # SQLAlchemy модели
│   ├── api/                      # API endpoints
│   │   └── v1/                   # Версия API v1
│   │       ├── students.py      # Студенты API
│   │       ├── materials.py     # Материалы API
│   │       └── messages.py      # Сообщения API
│   └── admin/                    # Админ панель
│       └── views.py             # Настройка админки
├── alembic/                     # Миграции БД
│   ├── env.py                   # Конфигурация Alembic
│   ├── script.py.mako           # Шаблон миграций
│   └── versions/                # Файлы миграций
├── db/                          # Схемы БД
│   ├── init.sql                 # Инициализация
│   └── schema.sql               # Полная схема
├── scripts/                     # Утилиты
│   ├── init_db.py              # Инициализация БД
│   ├── seed_data.py            # Тестовые данные
│   └── create_user.py           # Создание пользователей
├── docker-compose.yml           # Docker конфигурация
├── Dockerfile                   # Docker образ
├── requirements.txt             # Зависимости Python
├── alembic.ini                  # Конфигурация Alembic
└── README.md                    # Документация
```

## 🚀 Быстрый старт

### Вариант 1: Docker (Рекомендуется)

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd TutorAI

# Запустите с Docker Compose
docker-compose up -d

# Приложение будет доступно по адресу:
# - API: http://localhost:8000
# - Админ панель: http://localhost:8000/admin
# - Документация: http://localhost:8000/docs
```

### Вариант 2: Локальная установка

#### Требования
- **Python 3.11+**
- **PostgreSQL 15+**
- **Git**

#### Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd TutorAI
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте базу данных:**
   ```bash
   # Создайте базу данных PostgreSQL
   createdb ai_tutor_local
   
   # Или используйте Docker для PostgreSQL
   docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
   ```

5. **Инициализируйте базу данных:**
   ```bash
   python scripts/init_db.py --create --migrate --seed
   ```

6. **Запустите приложение:**
   ```bash
   python -m app.main
   # или
   uvicorn app.main:app --reload
   ```

7. **Откройте приложение:**
   - 🏠 **Главная**: http://localhost:8000 (редирект на админку)
   - 📊 **Админ панель**: http://localhost:8000/admin
   - 📚 **API документация**: http://localhost:8000/docs
   - 🔍 **ReDoc**: http://localhost:8000/redoc
   - ❤️ **Health check**: http://localhost:8000/health

## ⚙️ Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# База данных
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_tutor_local

# Окружение
ENVIRONMENT=LOCAL
DEBUG=True

# Приложение
PROJECT_NAME=AI Tutor
VERSION=1.0.0
```

### Docker конфигурация

Для Docker используйте `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: aitutor
      POSTGRES_PASSWORD: aitutor_dev_pass
      POSTGRES_DB: ai_tutor
    ports:
      - "5432:5432"
  
  app:
    build: .
    environment:
      DATABASE_URL: postgresql+asyncpg://aitutor:aitutor_dev_pass@postgres:5432/ai_tutor
    ports:
      - "8000:8000"
```

## 📚 API и документация

### Автоматическая документация

После запуска приложения доступна:

- 📖 **Swagger UI**: http://localhost:8000/docs
- 📋 **ReDoc**: http://localhost:8000/redoc  
- 🔧 **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints

- **GET** `/` - Главная страница (редирект на админку)
- **GET** `/health` - Проверка состояния
- **GET** `/admin` - Админ панель
- **GET** `/docs` - API документация

## 🗄️ База данных

### Основные сущности

| Модель | Описание |
|--------|----------|
| **Student** | Студенты с Telegram интеграцией |
| **CourseProgram** | Образовательные программы |
| **Stream** | Потоки обучения |
| **Module** | Модули курса (разделы) |
| **Lesson** | Уроки/темы внутри модулей |
| **CourseMaterial** | Материалы курса (3 типа) |
| **Message** | Сообщения студентов |
| **BotResponse** | Ответы ИИ-тьютора |
| **Assignment** | Задания студентов |
| **Schedule** | Расписание занятий |
| **Prompt** | Промпты для ИИ |

### Типы материалов

1. 📖 **Лекционные** (`lecture`) - информация для слушателя
2. 📝 **Задания** (`assignment`) - тестирования и практические работы  
3. 📋 **Методические** (`methodical`) - критерии проверки и оценки

### Типы занятий

1. 🎓 **Лекционная работа** - с датой и временем
2. 💻 **Практическая работа** - с датой и временем
3. 📚 **Самостоятельная работа** - только дата

### Управление миграциями

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1

# Показать историю миграций
alembic history
```

## 🤖 ИИ-тьютор и Telegram бот

### Система промптов

Система хранит промпты в таблице `prompts` с типами:
- 🔍 **question_classifier** - классификация вопросов студентов
- ❓ **faq_response** - ответы на часто задаваемые вопросы
- 📚 **material_response** - работа с материалами курса

### Telegram интеграция

- 💬 Сообщения студентов сохраняются в таблице `messages`
- 🤖 Ответы ИИ-тьютора в таблице `bot_responses`
- 🔗 Связь через `telegram_user_id` и `telegram_username`
- 📱 Поддержка множественных чатов

### API для интеграции

REST API endpoints для:
- 👥 Управления студентами
- 📚 Работы с материалами курсов
- 💬 Обработки сообщений и ответов
- 📅 Управления расписанием
- 📝 Работы с заданиями студентов

## 🧪 Тестирование

```bash
# Запуск тестов
pytest

# С покрытием кода
pytest --cov=app
```

## 🛠️ Утилиты

```bash
# Инициализация БД
python scripts/init_db.py --create --migrate --seed

# Загрузка тестовых данных
python scripts/seed_data.py

# Проверка состояния
curl http://localhost:8000/health
```

## 📝 Лицензия

MIT License