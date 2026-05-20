"""CLI entry point and main commands."""
import click
from src.cli.commands import auth, airdrop, task, db


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Manager Airdrop - Multichain Testnet Manager CLI."""
    pass


# Register command groups
cli.add_command(auth.auth_group, name='auth')
cli.add_command(airdrop.airdrop_group, name='airdrop')
cli.add_command(task.task_group, name='task')
cli.add_command(db.db_group, name='db')


if __name__ == '__main__':
    cli()
