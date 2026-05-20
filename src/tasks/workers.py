"""Background task workers."""
from src.db.database import get_session
from src.db.models import Task, AirdropRecipient
from src.airdrop.manager import AirdropManager
from src.blockchain.ethereum import EthereumManager
from src.blockchain.solana import SolanaManager
from datetime import datetime


class TaskWorker:
    """Execute background tasks."""
    
    @staticmethod
    def process_distribution_task(task_id):
        """Process distribution task."""
        session = get_session()
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if not task:
                return False
            
            # Get airdrop
            airdrop = session.query(AirdropRecipient).filter(
                AirdropRecipient.airdrop_id == task.airdrop_id
            ).all()
            
            # TODO: Implement actual distribution logic
            
            task.status = 'completed'
            task.completed_at = datetime.utcnow()
            session.commit()
            return True
        except Exception as e:
            task.status = 'failed'
            task.last_error = str(e)
            task.retry_count += 1
            session.commit()
            return False
        finally:
            session.close()
    
    @staticmethod
    def process_task(task_id):
        """Process any task based on type."""
        session = get_session()
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if not task:
                return False
            
            if task.task_type == 'distribute':
                return TaskWorker.process_distribution_task(task_id)
            
            return False
        finally:
            session.close()
