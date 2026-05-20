"""Airdrop campaign manager."""
from datetime import datetime
from src.db.models import Airdrop, AirdropRecipient


class AirdropManager:
    """Manage airdrop campaigns."""
    
    def __init__(self, session):
        """Initialize airdrop manager."""
        self.session = session
    
    def create_airdrop(self, name, chain, token_address, total_amount, recipients):
        """Create a new airdrop campaign."""
        try:
            airdrop = Airdrop(
                name=name,
                chain=chain,
                token_address=token_address,
                total_amount=total_amount,
                status='pending',
                created_at=datetime.utcnow()
            )
            
            self.session.add(airdrop)
            self.session.flush()
            
            # Add recipients
            amount_per_recipient = total_amount / len(recipients) if recipients else 0
            for recipient in recipients:
                airdrop_recipient = AirdropRecipient(
                    airdrop_id=airdrop.id,
                    recipient_address=recipient,
                    amount=amount_per_recipient,
                    status='pending'
                )
                self.session.add(airdrop_recipient)
            
            self.session.commit()
            return airdrop
        except Exception as e:
            self.session.rollback()
            raise Exception(f'Failed to create airdrop: {str(e)}')
    
    def get_airdrop(self, airdrop_id):
        """Get airdrop by ID."""
        return self.session.query(Airdrop).filter_by(id=airdrop_id).first()
    
    def get_all_airdrops(self):
        """Get all airdrops."""
        return self.session.query(Airdrop).all()
    
    def update_status(self, airdrop_id, status):
        """Update airdrop status."""
        try:
            airdrop = self.get_airdrop(airdrop_id)
            if airdrop:
                airdrop.status = status
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise Exception(f'Failed to update status: {str(e)}')
