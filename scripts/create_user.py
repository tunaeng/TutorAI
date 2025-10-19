#!/usr/bin/env python3
"""
Скрипт для создания тестового пользователя
"""
import asyncio
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def create_initial_user():
    """Создание тестового пользователя"""
    try:
        from app.core.database import async_session, engine, Base
        from app.models.education import Student, CourseProgram
        from sqlalchemy import select

        async with async_session() as session:
            # Ensure tables are created if not using Alembic for this run
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            # Check if a CourseProgram exists, create one if not
            result = await session.execute(select(CourseProgram).limit(1))
            course_program = result.scalars().first()
            if not course_program:
                print("No CourseProgram found, creating a default one...")
                course_program = CourseProgram(
                    name="Default AI Course",
                    description="A default course program for AI Tutor",
                    total_hours=100
                )
                session.add(course_program)
                await session.commit()
                await session.refresh(course_program)
                print(f"Created CourseProgram with ID: {course_program.program_id}")

            # Check if the user already exists
            result = await session.execute(select(Student).filter_by(telegram_user_id=123456789))
            existing_user = result.scalars().first()

            if existing_user:
                print(f"User with Telegram ID 123456789 already exists: {existing_user.name}")
            else:
                print("Creating a new student user...")
                new_student = Student(
                    name="Test User",
                    phone="+79001234567",
                    telegram_user_id=123456789,
                    telegram_username="test_user",
                    is_active=True,
                    course_program_id=course_program.program_id
                )
                session.add(new_student)
                await session.commit()
                await session.refresh(new_student)
                print(f"Successfully created user: {new_student.name} with ID: {new_student.student_id}")

        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания пользователя: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(create_initial_user())
    sys.exit(0 if success else 1)
