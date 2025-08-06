from flask.cli import with_appcontext
from .models import db
import click

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database (for development/preview/demo)."""
    db.create_all()
    click.echo("Initialized the database.")
