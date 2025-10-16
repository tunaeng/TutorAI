#!/usr/bin/env python3
"""
Create tables directly using SQLAlchemy
"""

import asyncio
from app.core.database import get_engine, Base
from app.models import education


async def create_tables():
    """Create all tables"""
    print("🚀 Creating database tables...")
    
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            # Import all models to ensure they are registered
            from app.models import education
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            
        print("✅ All tables created successfully!")
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False


async def main():
    """Main function"""
    success = await create_tables()
    
    if success:
        print("🎉 Database setup completed!")
    else:
        print("💥 Database setup failed!")
        return False
    
    return True


if __name__ == "__main__":
    asyncio.run(main())
