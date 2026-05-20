"""Authentication commands."""
import click
from src.auth.auth import AuthManager
from src.db.database import get_session


@click.group()
def auth_group():
    """Authentication commands."""
    pass


@auth_group.command()
@click.option('--username', prompt='Username', help='Username for login')
@click.option('--password', prompt=True, hide_input=True, help='Password')
def login(username, password):
    """Login to the application."""
    try:
        session = get_session()
        auth_manager = AuthManager(session)
        user = auth_manager.authenticate(username, password)
        
        if user:
            click.secho(f'✅ Login successful! Welcome {username}', fg='green')
        else:
            click.secho('❌ Invalid credentials', fg='red')
    except Exception as e:
        click.secho(f'❌ Login failed: {str(e)}', fg='red')


@auth_group.command()
@click.option('--username', prompt='Username', help='New username')
@click.option('--password', prompt=True, hide_input=True, help='Password')
@click.option('--role', default='user', type=click.Choice(['user', 'admin']), help='User role')
def create_user(username, password, role):
    """Create a new user."""
    try:
        session = get_session()
        auth_manager = AuthManager(session)
        user = auth_manager.create_user(username, password, role)
        
        if user:
            click.secho(f'✅ User {username} created successfully with role: {role}', fg='green')
        else:
            click.secho(f'❌ Failed to create user {username}', fg='red')
    except Exception as e:
        click.secho(f'❌ Error: {str(e)}', fg='red')
