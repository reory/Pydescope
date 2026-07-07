import pytest # noqa
import networkx as nx
from click.testing import CliRunner
from unittest.mock import patch
from pydescope.cli import main

@patch("pydescope.cli.ImportParser")
@patch("pydescope.cli.DependencyAnalyser")
@patch("pydescope.cli.GraphBuilder")
@patch("pydescope.cli.PyVisRenderer")
def test_cli_happy_path(
    mock_renderer_cls, mock_builder_cls, 
    mock_analyser_cls, mock_parser_cls, tmp_path
    ):

    """Verify standard execution flow when no constraints are violated."""

    # 1. Setup mock instance returns
    mock_parser = mock_parser_cls.return_value
    mock_parser.parse_project.return_value = {"module": []}
    
    mock_analyser = mock_analyser_cls.return_value
    mock_analyser.build_edges.return_value = []
    
    mock_builder = mock_builder_cls.return_value
    mock_builder.build.return_value = nx.DiGraph()
    
    mock_renderer = mock_renderer_cls.return_value
    mock_renderer.render.return_value = "pydescope.html"

    # 2. Invoke the CLI tool via Click's test runner
    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--out", "test.html", "--verbose"])

    # 3. Assert correct output logs and clean exit codes
    assert result.exit_code == 0
    assert "Pydescope graph written to test.html" in result.output
    
    # Assert methods were properly called
    mock_parser.parse_project.assert_called_once()
    mock_analyser.build_edges.assert_called_once()
    mock_builder.build.assert_called_once()
    mock_renderer.render.assert_called_once_with("test.html")

@patch("pydescope.cli.ImportParser")
@patch("pydescope.cli.DependencyAnalyser")
@patch("pydescope.cli.GraphBuilder")
@patch("pydescope.cli.PyVisRenderer")
def test_cli_max_nodes_exception_handling(
    mock_renderer_cls, mock_builder_cls, 
    mock_analyser_cls, mock_parser_cls, tmp_path
    ):
    
    """Verify that a ValueError in the renderer terminates cleanly with exit code 1."""

    # Setup the renderer mock instance to throw the custom threshold ValueError
    mock_renderer = mock_renderer_cls.return_value
    mock_renderer.render.side_effect = ValueError("Graph to large to render safely!")

    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--max-nodes", "10"])

    # Check exit behavior
    assert result.exit_code == 1
    assert "Graph to large to render safely!" in result.output