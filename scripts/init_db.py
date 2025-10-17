#!/usr/bin/env python3
"""
Database initialization script for AI Tutor Backend
Provides convenient CLI for database setup and migration
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path
from typing import Optional
import asyncpg
from sqlalchemy import text
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_engine
from app.core.config import settings


class DatabaseInitializer:
    """Database initialization and management class"""
    
    def __init__(self):
        self.database_url = settings.database_url
        self.db_name = "ai_tutor_local"
        self.schema_file = project_root / "db" / "schema.sql"
        
    def _get_postgres_url(self) -> str:
        """Get PostgreSQL URL without database name for connection"""
        # Convert postgresql+asyncpg:// to postgresql://
        url = self.database_url.replace("postgresql+asyncpg://", "postgresql://")
        # Remove database name from URL
        if "/" in url:
            url = url.rsplit("/", 1)[0] + "/postgres"
        return url
    
    async def check_database_exists(self) -> bool:
        """Check if database exists"""
        try:
            postgres_url = self._get_postgres_url()
            conn = await asyncpg.connect(postgres_url)
            
            result = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", 
                self.db_name
            )
            await conn.close()
            return result is not None
        except Exception as e:
            print(f"❌ Error checking database existence: {e}")
            return False
    
    async def create_database(self) -> bool:
        """Create database if it doesn't exist"""
        try:
            if await self.check_database_exists():
                print(f"✅ Database '{self.db_name}' already exists")
                return True
            
            postgres_url = self._get_postgres_url()
            conn = await asyncpg.connect(postgres_url)
            
            # Create database
            await conn.execute(f'CREATE DATABASE "{self.db_name}"')
            await conn.close()
            
            print(f"✅ Database '{self.db_name}' created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False
    
    async def execute_schema(self) -> bool:
        """Execute SQL schema from file"""
        try:
            if not self.schema_file.exists():
                print(f"❌ Schema file not found: {self.schema_file}")
                return False
            
            print(f"📄 Reading schema from {self.schema_file}")
            schema_sql = self.schema_file.read_text(encoding='utf-8')
            
            engine = get_engine()
            async with engine.begin() as conn:
                # Split schema into individual statements
                statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
                
                for i, statement in enumerate(statements, 1):
                    if statement:
                        try:
                            await conn.execute(text(statement))
                            print(f"  ✅ Statement {i}/{len(statements)} executed")
                        except Exception as e:
                            # Skip if already exists (for ENUMs, etc.)
                            if "already exists" in str(e).lower():
                                print(f"  ⚠️  Statement {i}/{len(statements)} skipped (already exists)")
                            else:
                                print(f"  ❌ Statement {i}/{len(statements)} failed: {e}")
                                return False
            
            print("✅ Schema executed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error executing schema: {e}")
            return False
    
    async def run_migrations(self) -> bool:
        """Run Alembic migrations"""
        try:
            print("🔄 Running Alembic migrations...")
            
            import subprocess
            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Migrations completed successfully")
                return True
            else:
                print(f"❌ Migration failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error running migrations: {e}")
            return False
    
    async def seed_test_data(self) -> bool:
        """Load test data into database"""
        try:
            print("🌱 Loading test data...")
            
            engine = get_engine()
            async with engine.begin() as conn:
                # Insert test course program
                await conn.execute(text("""
                    INSERT INTO course_programs (name, description, total_hours)
                    VALUES ('Python для начинающих', 'Базовый курс Python программирования', 120)
                    ON CONFLICT DO NOTHING
                """))
                
                # Insert test student
                await conn.execute(text("""
                    INSERT INTO students (phone, name, telegram_user_id, telegram_username, course_program_id)
                    VALUES ('+79991234567', 'Иван Тестов', 123456789, 'ivan_test', 1)
                    ON CONFLICT (phone) DO NOTHING
                """))
                
                # Insert test stream
                await conn.execute(text("""
                    INSERT INTO streams (program_id, name, start_date, end_date, description)
                    VALUES (1, 'Python Stream 2024', '2024-01-15', '2024-06-15', 'Основной поток Python курса')
                    ON CONFLICT DO NOTHING
                """))
                
                # Insert test module
                await conn.execute(text("""
                    INSERT INTO modules (program_id, order_num, name, description, duration_hours, 
                                       lecture_hours, practice_hours, independent_hours)
                    VALUES (1, 1, 'Основы Python', 'Введение в Python программирование', 20, 10, 8, 2)
                    ON CONFLICT DO NOTHING
                """))
                
                # Insert test lesson
                await conn.execute(text("""
                    INSERT INTO lessons (module_id, order_num, name, description, duration_hours)
                    VALUES (1, 1, 'Переменные и типы данных', 'Изучение основных типов данных Python', 2)
                    ON CONFLICT DO NOTHING
                """))
                
                # Insert test prompt
                await conn.execute(text("""
                    INSERT INTO prompts (prompt_type, prompt_text, description, version, is_active)
                    VALUES ('question_classifier', 'Classify this question about Python programming', 
                           'Default question classifier prompt', 1, true)
                    ON CONFLICT DO NOTHING
                """))
                
                # Insert test FAQ
                await conn.execute(text("""
                    INSERT INTO faq_responses (category, keywords, question, answer_text, is_active)
                    VALUES ('python', 'переменные, типы', 'Что такое переменная в Python?', 
                           'Переменная в Python - это именованная область памяти для хранения данных', true)
                    ON CONFLICT DO NOTHING
                """))
            
            print("✅ Test data loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error loading test data: {e}")
            return False
    
    async def verify_setup(self) -> bool:
        """Verify database setup"""
        try:
            print("🔍 Verifying database setup...")
            
            engine = get_engine()
            async with engine.begin() as conn:
                # Check tables
                result = await conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name
                """))
                tables = [row[0] for row in result.fetchall()]
                
                expected_tables = [
                    'students', 'course_programs', 'streams', 'students_streams',
                    'messages', 'bot_responses', 'modules', 'lessons', 'course_materials',
                    'meetings', 'schedule', 'assignments', 'prompts', 'faq_responses'
                ]
                
                missing_tables = set(expected_tables) - set(tables)
                if missing_tables:
                    print(f"❌ Missing tables: {missing_tables}")
                    return False
                
                # Check ENUMs
                result = await conn.execute(text("""
                    SELECT typname 
                    FROM pg_type 
                    WHERE typtype = 'e' 
                    ORDER BY typname
                """))
                enums = [row[0] for row in result.fetchall()]
                
                expected_enums = ['materialcategory', 'sendertype', 'assignmentstatus', 'meetingtype', 'prompttype']
                missing_enums = set(expected_enums) - set(enums)
                if missing_enums:
                    print(f"❌ Missing ENUMs: {missing_enums}")
                    return False
                
                # Check indexes
                result = await conn.execute(text("""
                    SELECT indexname 
                    FROM pg_indexes 
                    WHERE schemaname = 'public' 
                    AND indexname LIKE 'idx_%'
                    ORDER BY indexname
                """))
                indexes = [row[0] for row in result.fetchall()]
                
                print(f"✅ Found {len(tables)} tables, {len(enums)} ENUMs, {len(indexes)} indexes")
                print("✅ Database setup verified successfully")
                return True
                
        except Exception as e:
            print(f"❌ Error verifying setup: {e}")
            return False


async def main():
    """Main function with CLI argument parsing"""
    parser = argparse.ArgumentParser(description="AI Tutor Database Initialization")
    parser.add_argument("--create", action="store_true", help="Create database and tables")
    parser.add_argument("--migrate", action="store_true", help="Run Alembic migrations")
    parser.add_argument("--seed", action="store_true", help="Load test data")
    parser.add_argument("--verify", action="store_true", help="Verify database setup")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    print("🚀 AI Tutor Database Initialization")
    print("=" * 50)
    
    initializer = DatabaseInitializer()
    
    success = True
    
    # Create database and tables
    if args.create:
        print("\n📦 Creating database and tables...")
        if not await initializer.create_database():
            success = False
        if not await initializer.execute_schema():
            success = False
    
    # Run migrations
    if args.migrate:
        print("\n🔄 Running migrations...")
        if not await initializer.run_migrations():
            success = False
    
    # Load test data
    if args.seed:
        print("\n🌱 Loading test data...")
        if not await initializer.seed_test_data():
            success = False
    
    # Verify setup
    if args.verify or (args.create or args.migrate):
        print("\n🔍 Verifying setup...")
        if not await initializer.verify_setup():
            success = False
    
    # Default action if no arguments provided
    if not any([args.create, args.migrate, args.seed, args.verify]):
        print("\n📋 Available commands:")
        print("  python scripts/init_db.py --create          # Create DB and tables")
        print("  python scripts/init_db.py --migrate         # Run migrations only")
        print("  python scripts/init_db.py --create --seed   # Create DB + test data")
        print("  python scripts/init_db.py --verify          # Verify setup")
        return
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Database initialization completed successfully!")
        print("\n📝 Next steps:")
        print("  1. Start the application: python -m app.main")
        print("  2. Access admin panel: http://localhost:8000/admin")
        print("  3. View API docs: http://localhost:8000/docs")
    else:
        print("❌ Database initialization failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
