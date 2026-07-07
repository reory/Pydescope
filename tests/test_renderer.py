import pytest
import networkx as nx
from pydescope.renderer import PyVisRenderer, MAX_NODES_DEFAULT

def test_renderer_happy_path(tmp_path):
    """Verify that a small graph renders successfully and writes an HTML file."""

    # Create a clean small graph
    g = nx.DiGraph()
    g.add_edge("module_a", "module_b")
    
    output_html = tmp_path / "test_output.html"
    
    # Initialize renderer well under default max limit
    renderer = PyVisRenderer(graph=g, max_nodes=5)
    result_path = renderer.render(output_path=str(output_html))
    
    # Assertions
    assert result_path == str(output_html)
    assert output_html.exists()
    
    # Verify it actually produced PyVis / HTML content
    html_content = output_html.read_text(encoding="utf-8")
    assert "html" in html_content.lower()
    assert "div" in html_content.lower()

def test_renderer_guard_clause_exceeded():
    """Verify that the renderer raises a ValueError when the node limit is exceeded."""

    # Create a graph with 3 nodes
    g = nx.DiGraph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    
    # Set max_nodes to a value less than 3 (e.g., 2) to trigger the error
    renderer = PyVisRenderer(graph=g, max_nodes=2)
    
    # Assert that it raises the ValueError with the custom error snippet
    with pytest.raises(ValueError) as exc_info:
        renderer.render(output_path="should_not_be_created.html")
        
    assert "Graph to large to render safely!" in str(exc_info.value)
    assert "Limit      : 2" in str(exc_info.value)

def test_renderer_default_max_nodes():
    """Verify that the default max_nodes constant is set correctly on init."""
    
    g = nx.DiGraph()
    renderer = PyVisRenderer(graph=g)
    assert renderer.max_nodes == MAX_NODES_DEFAULT