# Command Line Interface

import click
import logging
from pathlib import Path
from .utils import setup_logging, get_logger

from .parser import ImportParser
from .analyser import DependencyAnalyser
from .graph_builder import GraphBuilder
from .renderer import PyVisRenderer, MAX_NODES_DEFAULT

@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--out", default="pydescope.html", help="Output HTML file")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed processing logs")
@click.option(
    "--max-nodes", 
    default=MAX_NODES_DEFAULT, 
    show_default=True,
    help="Abort rendering if node count exceeds this limit"
)
def main(path, out, verbose, max_nodes):
    
    # Initialise logging first!
    log_level = logging.DEBUG if verbose else logging.INFO
    setup_logging(level=log_level)
    
    logger = get_logger("pydescope.cli")

    root = Path(path)
    logger.info(f"Targeting project root: {root.absolute()}")

    parser = ImportParser(root)
    imports_map = parser.parse_project()

    analyser = DependencyAnalyser(imports_map)
    edges = analyser.build_edges()

    builder = GraphBuilder(edges)
    graph = builder.build()

    renderer = PyVisRenderer(graph, max_nodes=max_nodes)

    try:
        renderer.render(out)
        click.echo(f"Pydescope graph written to {out}")
    except ValueError as e:
        # print the error message to the stderr so it can be logged properly
        click.echo(str(e), err=True)
        # exit the program with a code 1 signalling a failure
        raise SystemExit(1)