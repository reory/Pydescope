import pytest
from pydescope.parser import ImportParser

@pytest.fixture
def mock_root(tmp_path):
    return tmp_path

@pytest.fixture
def sample_python_code():
    return """
import os
from .utils import is_internal_import
"""

def test_parse_file_imports(mock_root, sample_python_code):
    """Verify correct extraction of valid internal imports from a source file."""

    test_file = mock_root / "dummy_module.py"
    test_file.write_text(sample_python_code, encoding="utf-8")
    
    parser = ImportParser(root=mock_root)
    parsed_imports = parser.parse_file(test_file, package="pydescope")
    assert "pydescope.utils" in parsed_imports

def test_parse_file_syntax_error(mock_root):
    """Ensure invalid Python code returns an empty list instead of crashing."""

    broken_file = mock_root / "broken.py"
    broken_file.write_text("class Broken from syntax:", encoding="utf-8")
    
    parser = ImportParser(root=mock_root)
    assert parser.parse_file(broken_file) == []

def test_parse_project_walk(mock_root):
    """Verify recursive directory walking and correct exclusion of ignored paths."""

    # Create a valid file structure
    pkg_dir = mock_root / "pydescope"
    pkg_dir.mkdir()
    (pkg_dir / "core.py").write_text("import pydescope.utils", encoding="utf-8")
    
    # Create an ignored path file
    venv_dir = mock_root / "venv"
    venv_dir.mkdir()
    (venv_dir / "ignored.py").write_text("import secret", encoding="utf-8")
    
    parser = ImportParser(root=mock_root)
    results = parser.parse_project()
    
    # Assert valid modules are found and ignored ones are skipped
    assert "pydescope.core" in results
    assert "venv.ignored" not in results