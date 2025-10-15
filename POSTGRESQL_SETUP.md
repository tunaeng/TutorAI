# PostgreSQL Setup Guide

## Требования

- PostgreSQL 12+ 
- Python 3.8+
- pip

## Установка PostgreSQL

### Windows
1. Скачайте PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/
2. Установите PostgreSQL с настройками по умолчанию
3. Запомните пароль для пользователя `postgres`

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS
```bash
brew install postgresql
brew services start postgresql
```

## Настройка базы данных

### 1. Создание пользователя и базы данных

Подключитесь к PostgreSQL как суперпользователь:

```bash
sudo -u postgres psql
```

Выполните следующие команды:

```sql
-- Создание пользователя
CREATE USER "user" WITH PASSWORD 'password';

-- Создание базы данных
CREATE DATABASE ai_tutor_local OWNER "user";

-- Предоставление прав
GRANT ALL PRIVILEGES ON DATABASE ai_tutor_local TO "user";

-- Выход
\q
```

### 2. Настройка переменных окружения

Файл `.env` уже создан с правильными настройками:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_tutor_local
ENVIRONMENT=LOCAL
DEBUG=True
```

**Важно:** Измените пароль в `.env` файле на тот, который вы установили для пользователя `user`.

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Инициализация базы данных

Запустите скрипт инициализации:

```bash
python init_db.py
```

Этот скрипт:
- Создаст базу данных если она не существует
- Проверит подключение
- Создаст все таблицы

### 5. Запуск миграций

```bash
python run_migrations.py
```

Или напрямую через Alembic:

```bash
alembic upgrade head
```

## Проверка работы

### Тест подключения

```bash
python -c "
import asyncio
from app.core.database import get_engine
async def test():
    engine = get_engine()
    async with engine.begin() as conn:
        result = await conn.execute('SELECT 1')
        print('✅ Database connection successful!')
asyncio.run(test())
"
```

### Проверка таблиц

```bash
python -c "
import asyncio
from app.core.database import get_engine
async def test():
    engine = get_engine()
    async with engine.begin() as conn:
        result = await conn.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'\")
        tables = result.fetchall()
        print('📋 Created tables:')
        for table in tables:
            print(f'  - {table[0]}')
asyncio.run(test())
"
```

## Структура базы данных

Проект использует полную схему PostgreSQL с:

- **Студенты** (`students`) - информация о студентах
- **Программы курсов** (`course_programs`) - образовательные программы
- **Потоки** (`streams`) - потоки обучения с датами
- **Модули** (`modules`) - разделы курса с типами часов
- **Уроки** (`lessons`) - темы в модулях
- **Материалы** (`course_materials`) - материалы курса (лекции, задания, методические)
- **Сообщения** (`messages`) - сообщения студентов
- **Ответы бота** (`bot_responses`) - ответы ИИ
- **Встречи** (`meetings`) - занятия с типами
- **Расписание** (`schedule`) - расписание занятий
- **Задания** (`assignments`) - задания студентов
- **Промпты** (`prompts`) - промпты для ИИ
- **FAQ** (`faq_responses`) - часто задаваемые вопросы

## Миграции

Для создания новых миграций:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

Для отката миграций:

```bash
alembic downgrade -1
```

## Переключение на продакшн

Для переключения на продакшн базу данных просто измените `DATABASE_URL` в `.env` файле:

```env
DATABASE_URL=postgresql+asyncpg://prod_user:prod_password@prod_host:5432/ai_tutor_prod
ENVIRONMENT=PROD
```

## Устранение неполадок

### Ошибка подключения
- Убедитесь, что PostgreSQL запущен
- Проверьте правильность учетных данных в `.env`
- Убедитесь, что база данных существует

### Ошибки миграций
- Убедитесь, что все модели импортированы в `alembic/env.py`
- Проверьте, что база данных пуста перед первой миграцией

### Проблемы с правами
- Убедитесь, что пользователь имеет права на создание таблиц
- Проверьте, что база данных принадлежит правильному пользователю
