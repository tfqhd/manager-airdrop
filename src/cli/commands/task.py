"""Task management commands."""
import click
from src.tasks.scheduler import TaskScheduler
from src.db.database import get_session
from tabulate import tabulate


@click.group()
def task_group():
    """Task management commands."""
    pass


@task_group.command()
def list():
    """List all scheduled tasks."""
    try:
        session = get_session()
        scheduler = TaskScheduler(session)
        tasks = scheduler.get_all_tasks()
        
        if not tasks:
            click.echo('No tasks found.')
            return
        
        data = []
        for task in tasks:
            data.append([
                task.id,
                task.task_type,
                task.status,
                task.scheduled_time,
                task.retry_count,
                task.created_at
            ])
        
        headers = ['ID', 'Type', 'Status', 'Scheduled', 'Retries', 'Created']
        click.echo(tabulate(data, headers=headers, tablefmt='grid'))
    except Exception as e:
        click.secho(f'❌ Error: {str(e)}', fg='red')


@task_group.command()
@click.option('--task-id', type=int, prompt='Task ID', help='Task ID')
def status(task_id):
    """View task status and details."""
    try:
        session = get_session()
        scheduler = TaskScheduler(session)
        task = scheduler.get_task(task_id)
        
        if not task:
            click.secho(f'❌ Task {task_id} not found', fg='red')
            return
        
        click.echo(f'\nTask ID: {task.id}')
        click.echo(f'Type: {task.task_type}')
        click.echo(f'Status: {task.status}')
        click.echo(f'Scheduled: {task.scheduled_time}')
        click.echo(f'Retry Count: {task.retry_count}')
        click.echo(f'Last Error: {task.last_error}')
        click.echo(f'Created: {task.created_at}')
    except Exception as e:
        click.secho(f'❌ Error: {str(e)}', fg='red')


@task_group.command()
@click.option('--task-id', type=int, prompt='Task ID', help='Task ID to retry')
def retry(task_id):
    """Retry a failed task."""
    try:
        session = get_session()
        scheduler = TaskScheduler(session)
        result = scheduler.retry_task(task_id)
        
        if result:
            click.secho(f'✅ Task {task_id} retried successfully', fg='green')
        else:
            click.secho(f'❌ Failed to retry task {task_id}', fg='red')
    except Exception as e:
        click.secho(f'❌ Error: {str(e)}', fg='red')
