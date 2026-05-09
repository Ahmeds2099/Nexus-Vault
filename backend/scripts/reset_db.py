"""
scripts/reset_db.py — Utility to reset the database schema.

DANGER: This will DROP all tables and recreate them. 
All data in the 'items' table will be LOST.
Use this during the Phase 2 -> Phase 3 transition to apply the V2 schema.
"""

import sys
import os

# Add the 'app' directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
# We MUST import the models here so SQLAlchemy registers them with the Base
from app.models.item import Item 

def reset_database():
    print("🚀 Initializing Database Reset (MVP v2 migration)...")
    
    try:
        # 1. Drop all existing tables
        print("🗑️  Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        # 2. Create all tables with the new schema
        print("✨ Creating new tables from V2 schema...")
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Database migration successful!")
        print("   - Table 'items' recreated with v2 columns (raw_url, source, item_type, etc.)")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR during migration: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    reset_database()
