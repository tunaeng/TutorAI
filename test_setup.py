#!/usr/bin/env python3
"""
Test script to verify PostgreSQL setup and configuration
"""

import asyncio
import sys
from app.core.config import settings
from app.core.database import get_engine, Base
from app.models import education


async def test_configuration():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    
    print(f"  - Environment: {settings.environment}")
    print(f"  - Database URL: {settings.database_url}")
    print(f"  - Debug mode: {settings.debug}")
    print(f"  - App name: {settings.app_name}")
    
    if "postgresql+asyncpg://" in settings.database_url:
        print("  ✅ PostgreSQL configuration detected")
        return True
    else:
        print("  ❌ PostgreSQL configuration not found")
        return False


async def test_database_connection():
    """Test database connection"""
    print("\n🔌 Testing database connection...")
    
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            if row and row[0] == 1:
                print("  ✅ Database connection successful")
                return True
            else:
                print("  ❌ Database connection failed - unexpected result")
                return False
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False


async def test_models_import():
    """Test that all models can be imported"""
    print("\n📋 Testing models import...")
    
    try:
        # Test that all models are accessible
        models = [
            education.Student,
            education.CourseProgram,
            education.Stream,
            education.Module,
            education.Lesson,
            education.CourseMaterial,
            education.Message,
            education.BotResponse,
            education.Meeting,
            education.Schedule,
            education.Assignment,
            education.Prompt,
            education.FAQResponse,
        ]
        
        print(f"  ✅ Successfully imported {len(models)} models")
        return True
    except Exception as e:
        print(f"  ❌ Models import failed: {e}")
        return False


async def test_tables_exist():
    """Test that tables exist in database"""
    print("\n🗄️  Testing database tables...")
    
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            
            expected_tables = [
                'students', 'course_programs', 'streams', 'modules', 
                'lessons', 'course_materials', 'messages', 'bot_responses',
                'meetings', 'schedule', 'assignments', 'prompts', 
                'faq_responses', 'students_streams'
            ]
            
            missing_tables = set(expected_tables) - set(tables)
            if missing_tables:
                print(f"  ❌ Missing tables: {missing_tables}")
                return False
            else:
                print(f"  ✅ All {len(expected_tables)} tables exist")
                for table in sorted(tables):
                    print(f"    - {table}")
                return True
                
    except Exception as e:
        print(f"  ❌ Table check failed: {e}")
        return False


async def test_enums():
    """Test that PostgreSQL ENUMs exist"""
    print("\n🏷️  Testing PostgreSQL ENUMs...")
    
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("""
                SELECT typname 
                FROM pg_type 
                WHERE typtype = 'e' 
                ORDER BY typname
            """))
            enums = [row[0] for row in result.fetchall()]
            
            expected_enums = [
                'materialcategory', 'sendertype', 'assignmentstatus', 'meetingtype'
            ]
            
            missing_enums = set(expected_enums) - set(enums)
            if missing_enums:
                print(f"  ❌ Missing ENUMs: {missing_enums}")
                return False
            else:
                print(f"  ✅ All {len(expected_enums)} ENUMs exist")
                for enum_name in sorted(enums):
                    print(f"    - {enum_name}")
                return True
                
    except Exception as e:
        print(f"  ❌ ENUM check failed: {e}")
        return False


async def main():
    """Main test function"""
    print("🚀 PostgreSQL Setup Verification")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_database_connection,
        test_models_import,
        test_tables_exist,
        test_enums,
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All {total} tests passed! PostgreSQL setup is complete.")
        print("\n✅ Your project is ready to use PostgreSQL!")
        print("\nNext steps:")
        print("1. Run: python -m app.main")
        print("2. Open: http://localhost:8000/docs")
        return True
    else:
        print(f"❌ {total - passed} out of {total} tests failed.")
        print("\nPlease check the errors above and fix them.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
