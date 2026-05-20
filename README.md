# Manager Airdrop - Multichain Testnet Manager

Aplikasi CLI untuk manage airdrop di blockchain Ethereum dan Solana dengan fitur task scheduling, distribution token, tracking, dan authentication.

## Fitur Utama

✨ **Multichain Support**
- Ethereum testnet (Goerli, Sepolia)
- Solana testnet

✨ **User Management**
- Authentication dengan username/password
- Role-based access control

✨ **Airdrop Management**
- Create dan manage airdrop campaign
- Track eligibility dan distribution status
- Batch distribute token ke multiple addresses
- Monitor airdrop progress

✨ **Task Manager**
- Schedule airdrop tasks
- Automatic retry untuk failed tasks
- Task history dan logging
- Real-time task status monitoring

✨ **Database**
- SQLite untuk persistent storage
- Schema untuk users, airdrops, wallets, tasks

## Tech Stack

- **Language**: Python 3.8+
- **Framework**: Click (CLI), Web3.py (Ethereum), Solders (Solana)
- **Database**: SQLite3
- **Task Queue**: APScheduler
- **Crypto**: eth-keys, tweetnacl

## Instalasi

### Prerequisites
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

### Setup Project
```bash
# Clone repository
git clone https://github.com/tfqhd/manager-airdrop.git
cd manager-airdrop

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m src.cli init-db

# Create admin user
python -m src.cli create-user --username admin --password your_password
```

## Usage

### Authentication
```bash
python -m src.cli login --username admin --password your_password
```

### Create Airdrop Campaign
```bash
python -m src.cli airdrop create \
  --name "TestAirdrop" \
  --chain ethereum \
  --token-address "0x..." \
  --amount 100 \
  --recipients recipients.txt
```

### Distribute Token
```bash
python -m src.cli airdrop distribute \
  --airdrop-id 1 \
  --batch-size 10 \
  --schedule "2024-01-20 10:00:00"
```

### View Tasks
```bash
python -m src.cli task list
python -m src.cli task status <task_id>
```

### View Airdrop Status
```bash
python -m src.cli airdrop list
python -m src.cli airdrop status <airdrop_id>
```

## Project Structure

```
manager-airdrop/
├── src/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py           # Entry point CLI
│   │   ├── commands.py        # CLI commands
│   │   └── utils.py           # Helper functions
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth.py            # Authentication logic
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py          # Database models
│   │   └── database.py        # Database operations
│   ├── blockchain/
│   │   ├── __init__.py
│   │   ├── ethereum.py        # Ethereum operations
│   │   └── solana.py          # Solana operations
│   ├── airdrop/
│   │   ├── __init__.py
│   │   ├── manager.py         # Airdrop management
│   │   └── distributor.py     # Token distribution logic
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── scheduler.py       # Task scheduling
│   │   └── workers.py         # Task execution
│   └── config/
│       ├── __init__.py
│       └── config.py          # Configuration
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_airdrop.py
│   └── test_blockchain.py
├── .env.example
├── requirements.txt
├── setup.py
└── README.md
```

## Configuration

Create `.env` file:
```env
# Database
DATABASE_URL=sqlite:///airdrop.db

# Ethereum
ETHEREUM_RPC_URL=https://goerli.infura.io/v3/YOUR_KEY
ETHEREUM_CHAIN_ID=5

# Solana
SOLANA_RPC_URL=https://api.devnet.solana.com

# JWT Secret (untuk future enhancement)
JWT_SECRET=your_secret_key

# Log level
LOG_LEVEL=INFO
```

## Development

### Run Tests
```bash
pytest tests/
```

### Code Style
```bash
black src/
flake8 src/
```

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

Untuk issue atau pertanyaan, buka issue di GitHub atau hubungi tim development.
