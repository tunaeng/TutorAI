#!/usr/bin/env python3
"""
Run Alembic migrations for PostgreSQL
"""

import asyncio
import subprocess
import sys
from app.core.config import settings


async def run_migrations():
    """Run Alembic migrations"""
    print("🔄 Running Alembic migrations...")
    
    try:
        # Run alembic upgrade
        result = subprocess.run([
            sys.executable, "-m", "alembic", "upgrade", "head"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Migrations completed successfully!")
            print(result.stdout)
        else:
            print("❌ Migration failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Failed to run migrations: {e}")
        return False
    
    return True


async def main():
    """Main function"""
    print("🚀 Starting migration process...")
    print(f"Database URL: {settings.database_url}")
    
    success = await run_migrations()
    
    if success:
        print("🎉 Migration process completed successfully!")
    else:
        print("💥 Migration process failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
