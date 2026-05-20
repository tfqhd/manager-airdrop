"""Database commands."""
import click
from src.db.database import init_db, get_session
from src.db.models import Base


@click.group()
def db_group():
    """Database management commands."""
    pass


@db_group.command()
def init():
    """Initialize the database with all tables."""
    try:
        init_db()
        click.secho('✅ Database initialized successfully!', fg='green')
    except Exception as e:
        click.secho(f'❌ Error initializing database: {str(e)}', fg='red')


@db_group.command()
def reset():
    """Reset the database (WARNING: This deletes all data)."""
    if not click.confirm('⚠️  Are you sure? This will delete all data.'):
        click.echo('Cancelled.')
        return
    
    try:
        session = get_session()
        # Drop all tables
        Base.metadata.drop_all(bind=session.bind)
        session.commit()
        
        # Recreate tables
        init_db()
        click.secho('✅ Database reset successfully!', fg='green')
    except Exception as e:
        click.secho(f'❌ Error resetting database: {str(e)}', fg='red')


@db_group.command()
def status():
    """Check database connection status."""
    try:
        session = get_session()
        session.execute('SELECT 1')
        click.secho('✅ Database connection OK', fg='green')
    except Exception as e:
        click.secho(f'❌ Database connection failed: {str(e)}', fg='red')
