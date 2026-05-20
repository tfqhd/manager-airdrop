import sqlite3
import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from src.config import get_config
from .models import SCHEMA

logger = logging.getLogger(__name__)

class Database:
    """SQLite Database manager"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(get_config().DB_PATH)
        self._init_db()
    
    def _init_db(self):
        """Initialize database with schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(SCHEMA)
                conn.commit()
                logger.info(f"Database initialized: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute SELECT query"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Execute SELECT query and return first result"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def insert(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT query and return last row id"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.lastrowid
    
    def update(self, query: str, params: tuple = ()) -> int:
        """Execute UPDATE query and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.rowcount
    
    def delete(self, query: str, params: tuple = ()) -> int:
        """Execute DELETE query and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.rowcount
    
    def close(self):
        """Close database connection"""
        pass

# Singleton instance
_db = None

def get_db() -> Database:
    """Get database instance"""
    global _db
    if _db is None:
        _db = Database()
    return _db
