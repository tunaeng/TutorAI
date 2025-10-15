#!/usr/bin/env python3
"""
Database initialization script for PostgreSQL
This script creates the database and runs migrations
"""

import asyncio
import asyncpg
import os
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.core.database import Base
from app.models import education


async def create_database():
    """Create database if it doesn't exist"""
    # Connect to postgres database to create our database
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="postgres",  # Default postgres user
        password="password",  # Change this to your postgres password
        database="postgres"
    )
    
    # Check if database exists
    result = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1", "ai_tutor_local"
    )
    
    if not result:
        print("Creating database 'ai_tutor_local'...")
        await conn.execute('CREATE DATABASE "ai_tutor_local"')
        print("Database created successfully!")
    else:
        print("Database 'ai_tutor_local' already exists.")
    
    await conn.close()


async def test_connection():
    """Test connection to our database"""
    try:
        # Try to connect with the credentials from .env
        conn = await asyncpg.connect(settings.database_url.replace("postgresql+asyncpg://", "postgresql://"))
        print("✅ Connection to PostgreSQL successful!")
        await conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


async def create_tables():
    """Create tables using SQLAlchemy"""
    try:
        engine = create_async_engine(settings.database_url, echo=True)
        async with engine.begin() as conn:
            # Import all models to ensure they are registered
            from app.models import education
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully!")
        await engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False


async def main():
    """Main initialization function"""
    print("🚀 Initializing PostgreSQL database...")
    
    # Step 1: Create database
    try:
        await create_database()
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        print("Please make sure PostgreSQL is running and you have the correct credentials.")
        return
    
    # Step 2: Test connection
    if not await test_connection():
        print("Please check your database credentials in .env file")
        return
    
    # Step 3: Create tables
    await create_tables()
    
    print("🎉 Database initialization completed!")


if __name__ == "__main__":
    asyncio.run(main())
