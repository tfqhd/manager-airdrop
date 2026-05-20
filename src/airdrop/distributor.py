"""Token distribution logic."""
from datetime import datetime
from src.db.models import AirdropRecipient, Task
from src.blockchain.ethereum import EthereumManager
from src.blockchain.solana import SolanaManager


class TokenDistributor:
    """Handle token distribution for airdrops."""
    
    def __init__(self, session):
        """Initialize distributor."""
        self.session = session
    
    def distribute(self, airdrop_id, batch_size=10, scheduled_time=None):
        """Distribute tokens in batches."""
        try:
            from src.airdrop.manager import AirdropManager
            manager = AirdropManager(self.session)
            airdrop = manager.get_airdrop(airdrop_id)
            
            if not airdrop:
                raise ValueError(f'Airdrop {airdrop_id} not found')
            
            # Get pending recipients
            pending_recipients = self.session.query(AirdropRecipient).filter(
                AirdropRecipient.airdrop_id == airdrop_id,
                AirdropRecipient.status == 'pending'
            ).all()
            
            # Create tasks for batches
            batches = [pending_recipients[i:i+batch_size] 
                      for i in range(0, len(pending_recipients), batch_size)]
            
            for batch_idx, batch in enumerate(batches):
                task = Task(
                    task_type='distribute',
                    airdrop_id=airdrop_id,
                    status='pending',
                    scheduled_time=scheduled_time or datetime.utcnow(),
                    batch_data=f'batch_{batch_idx}',
                    retry_count=0,
                    created_at=datetime.utcnow()
                )
                self.session.add(task)
            
            self.session.commit()
            
            return {
                'status': 'scheduled' if scheduled_time else 'pending',
                'batches': len(batches),
                'recipients': len(pending_recipients)
            }
        except Exception as e:
            self.session.rollback()
            raise Exception(f'Distribution failed: {str(e)}')
    
    def _send_to_blockchain(self, chain, recipients, token_address, private_key):
        """Send tokens to recipients on blockchain."""
        if chain.lower() == 'ethereum':
            manager = EthereumManager()
            # TODO: Implement actual distribution
        elif chain.lower() == 'solana':
            manager = SolanaManager()
            # TODO: Implement actual distribution
        else:
            raise ValueError(f'Unknown chain: {chain}')
