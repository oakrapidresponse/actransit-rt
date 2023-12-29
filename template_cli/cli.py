#!/usr/bin/env python3

"""
Basic CLI Template

Example usage:
    poetry run template-cli version

"""
import click
import dotenv


@click.group()
def cli() -> None:
    """Run cli commands"""
    dotenv.load_dotenv()


@cli.command()
def version() -> None:
    """Get the cli version."""
    click.echo(click.style("0.1.0", bold=True))


if __name__ == "__main__":
    cli()
