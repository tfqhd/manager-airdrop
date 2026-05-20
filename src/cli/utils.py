"""CLI utility functions."""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
    else:
        raise FileNotFoundError('.env file not found. Please create it from .env.example')


def validate_address(chain, address):
    """Validate blockchain address format."""
    if chain.lower() == 'ethereum':
        # Ethereum address should be 42 chars (0x + 40 hex)
        if not address.startswith('0x') or len(address) != 42:
            raise ValueError(f'Invalid Ethereum address: {address}')
    elif chain.lower() == 'solana':
        # Solana address should be 44 chars (base58)
        if len(address) != 44:
            raise ValueError(f'Invalid Solana address: {address}')
    else:
        raise ValueError(f'Unknown chain: {chain}')
    
    return True


def parse_recipients_file(file_path):
    """Parse recipients from file."""
    recipients = []
    with open(file_path, 'r') as f:
        for line in f:
            addr = line.strip()
            if addr and not addr.startswith('#'):
                recipients.append(addr)
    return recipients
