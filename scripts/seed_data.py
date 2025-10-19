#!/usr/bin/env python3
"""
Скрипт для загрузки тестовых данных в базу
"""
import asyncio
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def seed_data():
    """Загрузка тестовых данных"""
    try:
        from app.core.database import async_session, engine
        from app.models.education import (
            CourseProgram, Student, Stream, Module, Lesson,
            CourseMaterial, Schedule, Assignment, Message, BotResponse
        )
        from sqlalchemy.ext.asyncio import AsyncSession
        
        print("🌱 Загружаем тестовые данные...")
        
        async with async_session() as session:
            # Создаем программу курса
            program = CourseProgram(
                name="Специалист по работе с системами ИИ в сфере культуры",
                description="Комплексная программа обучения работе с ИИ",
                total_hours=144
            )
            session.add(program)
            await session.flush()
            
            # Создаем модули
            modules_data = [
                {"name": "Введение в ИИ", "order_num": 1, "duration_hours": 15},
                {"name": "Большие языковые модели", "order_num": 2, "duration_hours": 44},
                {"name": "Диффузионные нейросети", "order_num": 3, "duration_hours": 11},
                {"name": "ИИ в исследованиях", "order_num": 4, "duration_hours": 11},
                {"name": "Виртуальные ассистенты", "order_num": 5, "duration_hours": 11}
            ]
            
            modules = []
            for module_data in modules_data:
                module = Module(
                    program_id=program.program_id,
                    **module_data
                )
                session.add(module)
                modules.append(module)
            
            await session.flush()
            
            # Создаем студента
            student = Student(
                phone="+79123456789",
                name="Иван Петров",
                telegram_user_id=123456789,
                telegram_username="ivan_petrov",
                is_active=True,
                course_program_id=program.program_id
            )
            session.add(student)
            await session.flush()
            
            # Создаем поток
            stream = Stream(
                program_id=program.program_id,
                name="Октябрь 2025",
                start_date="2025-10-01",
                end_date="2025-12-31"
            )
            session.add(stream)
            await session.flush()
            
            # Создаем сообщение
            message = Message(
                chat_id=123456789,
                sender_type="user",
                sender_id=student.student_id,
                text_content="Привет! Расскажи про ИИ в культуре"
            )
            session.add(message)
            await session.flush()
            
            # Создаем ответ бота
            bot_response = BotResponse(
                message_id=message.message_id,
                text_content="Привет! ИИ в культуре - это увлекательная область..."
            )
            session.add(bot_response)
            
            await session.commit()
            print("✅ Тестовые данные загружены успешно!")
            
    except Exception as e:
        print(f"❌ Ошибка загрузки данных: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(seed_data())