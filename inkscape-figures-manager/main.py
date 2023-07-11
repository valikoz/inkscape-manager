import os
from pathlib import Path
import click
from shutil import copy
from loguru import logger

from _handler import Watcher
from _picker import picker


@click.group()
def cli():
    pass


@cli.command()
@click.argument('title')
@click.argument(
    'root',
    default=os.getcwd(),
    type=click.Path(exists=False, file_okay=False, dir_okay=True)
)
def create(title, root):
    """
    Creates a figure.

    First argument is the title of the figure.
    Second argument is the figure directory.
    """
    title = title.strip()
    root = Path(root).absolute()
    if not root.exists():
        root.mkdir()

    figure_path = root / (title + '.svg')
    if figure_path.exists():
        logger.debug(f'''Name `{title}` already exists.
                     Create a new name and try again.''')
        return

    TEMPLATE = Path(__file__).parent.parent / 'config' / 'template.svg'
    copy(str(TEMPLATE), str(figure_path))
    # Open Inkscape and monitor file
    watcher = Watcher(figure_path)
    watcher.run()


@cli.command()
@click.argument(
    'root',
    default=os.getcwd(),
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def edit(root):
    """
    Edits a figure.

    First argument is the figure directory.
    """

    figures = Path(root).absolute()

    # Open a selection dialog using fzf.
    selected = picker(figures)
    if selected:
        watcher = Watcher(selected)
        watcher.run()
    else:
        logger.error("No file selected.")


if __name__ == '__main__':
    cli()
