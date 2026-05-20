import hashlib
import secrets
import logging
from typing import Optional, Tuple
from src.db import get_db

logger = logging.getLogger(__name__)

class AuthManager:
    """Authentication manager"""
    
    def __init__(self):
        self.db = get_db()
        self.current_user: Optional[str] = None
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        password_hash = hash_obj.hex()
        return password_hash, salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """Verify password"""
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        computed_hash = hash_obj.hex()
        return computed_hash == password_hash
    
    def create_user(self, username: str, password: str) -> bool:
        """Create new user"""
        try:
            # Check if user exists
            existing = self.db.execute_one(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            )
            if existing:
                logger.warning(f"User already exists: {username}")
                return False
            
            # Hash password
            password_hash, salt = self.hash_password(password)
            
            # Store combined hash (hash:salt)
            combined = f"{password_hash}:{salt}"
            
            # Insert user
            self.db.insert(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, combined)
            )
            logger.info(f"User created: {username}")
            return True
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return False
    
    def login(self, username: str, password: str) -> bool:
        """Login user"""
        try:
            user = self.db.execute_one(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,)
            )
            
            if not user:
                logger.warning(f"User not found: {username}")
                return False
            
            # Extract hash and salt
            hash_and_salt = user['password_hash'].split(':')
            if len(hash_and_salt) != 2:
                logger.error(f"Invalid password hash format for user: {username}")
                return False
            
            password_hash, salt = hash_and_salt
            
            # Verify password
            if self.verify_password(password, password_hash, salt):
                self.current_user = username
                logger.info(f"User logged in: {username}")
                return True
            else:
                logger.warning(f"Invalid password for user: {username}")
                return False
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            logger.info(f"User logged out: {self.current_user}")
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[str]:
        """Get current user"""
        return self.current_user
    
    def get_user_id(self, username: str) -> Optional[int]:
        """Get user ID by username"""
        user = self.db.execute_one(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        return user['id'] if user else None

# Singleton instance
_auth = None

def get_auth() -> AuthManager:
    """Get auth manager instance"""
    global _auth
    if _auth is None:
        _auth = AuthManager()
    return _auth
