"""Task scheduler using APScheduler."""
from apscheduler.schedulers.background import BackgroundScheduler
from src.db.models import Task
from datetime import datetime


class TaskScheduler:
    """Manage task scheduling."""
    
    def __init__(self, session):
        """Initialize scheduler."""
        self.session = session
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
    
    def get_all_tasks(self):
        """Get all tasks."""
        return self.session.query(Task).all()
    
    def get_task(self, task_id):
        """Get task by ID."""
        return self.session.query(Task).filter_by(id=task_id).first()
    
    def schedule_task(self, task_type, scheduled_time, task_data=None):
        """Schedule a new task."""
        try:
            task = Task(
                task_type=task_type,
                status='pending',
                scheduled_time=scheduled_time,
                batch_data=task_data,
                retry_count=0,
                created_at=datetime.utcnow()
            )
            
            self.session.add(task)
            self.session.commit()
            return task
        except Exception as e:
            self.session.rollback()
            raise Exception(f'Failed to schedule task: {str(e)}')
    
    def retry_task(self, task_id):
        """Retry a failed task."""
        try:
            task = self.get_task(task_id)
            if task:
                task.status = 'pending'
                task.retry_count += 1
                task.last_error = None
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise Exception(f'Failed to retry task: {str(e)}')
