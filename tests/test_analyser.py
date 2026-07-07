import pytest # noqa
from hypothesis import given, strategies as st
from pydescope.analyser import DependencyAnalyser

def test_analyser_basic_edges():
    """Verify edge generation with known simple inputs."""
    
    imports_map = {
        "pydescope.cli": ["pydescope.parser", "pydescope.utils"],
        "pydescope.parser": ["pydescope.utils"],
        "pydescope.utils": []
    }
    
    analyser = DependencyAnalyser(imports_map)
    edges = analyser.build_edges()
    
    expected_edges = [
        ("pydescope.cli", "pydescope.parser"),
        ("pydescope.cli", "pydescope.utils"),
        ("pydescope.parser", "pydescope.utils")
    ]
    
    assert len(edges) == 3
    assert set(edges) == set(expected_edges)

@given(st.dictionaries(
    keys=st.text(min_size=1, max_size=10),
    values=st.lists(st.text(min_size=1, max_size=10), min_size=0, max_size=5),
    min_size=0,
    max_size=10
))
def test_analyser_with_arbitrary_maps(imports_map):
    """Property-based test ensuring every dependency maps to an edge."""

    analyser = DependencyAnalyser(imports_map)
    edges = analyser.build_edges()
    
    # Calculate exactly how many total edge connections we expect
    expected_total_count = sum(len(imports) for imports in imports_map.values())
    assert len(edges) == expected_total_count
    
    # Verify each edge correctly pairs the key with its imported item
    for module, imp in edges:
        assert module in imports_map
        assert imp in imports_map[module]