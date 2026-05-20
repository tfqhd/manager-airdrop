import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///airdrop.db")
    
    # Ethereum
    ETHEREUM_RPC_URL = os.getenv(
        "ETHEREUM_RPC_URL",
        "https://sepolia.infura.io/v3/YOUR_KEY"
    )
    ETHEREUM_CHAIN_ID = int(os.getenv("ETHEREUM_CHAIN_ID", "11155111"))
    ETHEREUM_PRIVATE_KEY = os.getenv("ETHEREUM_PRIVATE_KEY", "")
    
    # Solana
    SOLANA_RPC_URL = os.getenv(
        "SOLANA_RPC_URL",
        "https://api.devnet.solana.com"
    )
    SOLANA_PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY", "")
    
    # App
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Project root
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DB_PATH = PROJECT_ROOT / "airdrop.db"

# Create singleton instance
_config = None

def get_config() -> Config:
    """Get configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config
