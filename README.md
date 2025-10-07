# AI Tutor FastAPI Backend

Бэкенд для ИИ-агента тьютора на FastAPI с SQLAlchemy моделями для курса "Инструменты искусственного интеллекта в сфере культуры".

## Описание

Проект реализует REST API для управления образовательным процессом через Telegram-бота, включая:
- Управление студентами и потоками обучения
- Структуру курсов с модулями, уроками и материалами
- Систему заданий и аттестации
- Хранение сообщений и промптов для ИИ

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **PostgreSQL** - основная база данных
- **Pydantic** - валидация данных
- **Alembic** - миграции базы данных

## Установка и запуск

### 1. Клонирование репозитория
git clone <repository-url>
cd ai-tutor-backend

text

### 2. Создание виртуального окружения
Windows
python -m venv venv
venv\Scripts\activate

macOS/Linux
python3 -m venv venv
source venv/bin/activate

text

### 3. Установка зависимостей
pip install -r requirements.txt

text

### 4. Настройка переменных окружения
Создайте файл `.env` в корне проекта:
DATABASE_URL=postgresql://username:password@localhost/database_name
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development

text

### 5. Инициализация базы данных
Создание миграций
alembic init alembic

Применение миграций
alembic upgrade head

text

### 6. Запуск приложения
Режим разработки с автоперезагрузкой
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Продакшен режим
uvicorn main:app --host 0.0.0.0 --port 8000

text

Приложение будет доступно по адресу: http://localhost:8000

### 7. Документация API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc