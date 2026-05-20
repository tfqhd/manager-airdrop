"""Airdrop management commands."""
import click
from src.airdrop.manager import AirdropManager
from src.airdrop.distributor import TokenDistributor
from src.db.database import get_session
from tabulate import tabulate


@click.group()
def airdrop_group():
    """Airdrop management commands."""
    pass


@airdrop_group.command()
@click.option('--name', prompt='Airdrop name', help='Campaign name')
@click.option('--chain', type=click.Choice(['ethereum', 'solana']), prompt=True, help='Blockchain')
@click.option('--token-address', prompt='Token address', help='Token contract address')
@click.option('--amount', type=float, prompt='Total amount', help='Total tokens to distribute')
@click.option('--recipients', type=click.File('r'), prompt='Recipients file', help='File with recipient addresses')
def create(name, chain, token_address, amount, recipients):
    """Create a new airdrop campaign."""
    try:
        session = get_session()
        manager = AirdropManager(session)
        
        # Parse recipients from file
        recipient_list = [line.strip() for line in recipients if line.strip()]
        
        airdrop = manager.create_airdrop(
            name=name,
            chain=chain,
            token_address=token_address,
            total_amount=amount,
            recipients=recipient_list
        )
        
        click.secho(f'✅ Airdrop "{name}" created successfully!', fg='green')
        click.echo(f'Campaign ID: {airdrop.id}')
        click.echo(f'Recipients: {len(recipient_list)}')
        click.echo(f'Amount per recipient: {amount / len(recipient_list):.6f}')
    except Exception as e:
        click.secho(f'❌ Error: {str(e)}', fg='red')


@airdrop_group.command()
def list():
    """List all airdrop campaigns."""
    try:
        session = get_session()
        manager = AirdropManager(session)
        airdrops = manager.get_all_airdrops()
        
        if not airdrops:
            click.echo('No airdrops found.')
            return
        
        data = []
        for airdrop in airdrops:
            data.append([
                airdrop.id,
                airdrop.name,
                airdrop.chain,
                airdrop.total_amount,
                airdrop.status,
                airdrop.created_at
            ])
        
        headers = ['ID', 'Name', 'Chain', 'Amount', 'Status', 'Created']
        click.echo(tabulate(data, headers=headers, tablefmt='grid'))
    except Exception as e:
        click.secho(f'❌ Error: {str(e)}', fg='red')


@airdrop_group.command()
@click.option('--airdrop-id', type=int, prompt='Airdrop ID', help='Airdrop campaign ID')
def status(airdrop_id):
    """View airdrop campaign status."""
    try:
        session = get_session()
        manager = AirdropManager(session)
        airdrop = manager.get_airdrop(airdrop_id)
        
        if not airdrop:
            click.secho(f'❌ Airdrop {airdrop_id} not found', fg='red')
            return
        
        click.echo(f'\nAirdrop: {airdrop.name}')
        click.echo(f'Chain: {airdrop.chain}')
        click.echo(f'Status: {airdrop.status}')
        click.echo(f'Total Amount: {airdrop.total_amount}')
        click.echo(f'Recipients: {len(airdrop.recipients)}')
        click.echo(f'Distributed: {airdrop.distributed_count}')
        click.echo(f'Failed: {airdrop.failed_count}')
    except Exception as e:
        click.secho(f'❌ Error: {str(e)}', fg='red')


@airdrop_group.command()
@click.option('--airdrop-id', type=int, prompt='Airdrop ID', help='Airdrop campaign ID')
@click.option('--batch-size', type=int, default=10, help='Batch size for distribution')
@click.option('--schedule', default=None, help='Schedule time (YYYY-MM-DD HH:MM:SS)')
def distribute(airdrop_id, batch_size, schedule):
    """Distribute tokens for an airdrop campaign."""
    try:
        session = get_session()
        distributor = TokenDistributor(session)
        
        if schedule:
            click.echo(f'📅 Scheduled distribution at: {schedule}')
        
        result = distributor.distribute(
            airdrop_id=airdrop_id,
            batch_size=batch_size,
            scheduled_time=schedule
        )
        
        click.secho(f'✅ Distribution started!', fg='green')
        click.echo(f'Batches: {result.get("batches", 0)}')
        click.echo(f'Status: {result.get("status", "pending")}')
    except Exception as e:
        click.secho(f'❌ Error: {str(e)}', fg='red')
