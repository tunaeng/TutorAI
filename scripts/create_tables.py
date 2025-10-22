#!/usr/bin/env python3
"""
Скрипт для создания таблиц в базе данных
"""
import asyncio
import sys
import os
from pathlib import Path

# Добавляем путь к проекту
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def create_tables():
    """Создать все таблицы в базе данных"""
    try:
        from app.core.database import engine, Base
        from app.models import education  # Важно для импорта моделей
        
        print("Создаем таблицы в базе данных...")
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("Таблицы созданы успешно!")
        return True
        
    except Exception as e:
        print(f"Ошибка создания таблиц: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(create_tables())