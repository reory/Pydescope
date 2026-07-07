import pytest #noqa
import logging
from pydescope.utils import (
    setup_logging, 
    get_logger, 
    normalise_module_name, 
    is_internal_import
)

def test_setup_logging_and_get_logger():
    """Verify that logger setup initializes configuration and 
    retrieves a logger instance.
    """

    setup_logging(level=logging.DEBUG)
    logger = get_logger("test_suite_logger")
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_suite_logger"

def test_normalise_module_name():
    """Verify paths with Unix, Windows slashes, and extensions normalize correctly."""

    assert normalise_module_name("pydescope/cli.py") == "pydescope.cli"
    assert normalise_module_name("pydescope\\parser.py") == "pydescope.parser"
    assert normalise_module_name("pydescope/submodule/file.py") == "pydescope.submodule.file"

def test_is_internal_import_as_file(tmp_path):
    """Verify true is returned when the import maps directly to an internal .py file."""

    # Setup standard module structure: pydescope/parser.py
    pkg_dir = tmp_path / "pydescope"
    pkg_dir.mkdir()
    file_path = pkg_dir / "parser.py"
    file_path.write_text("# dummy", encoding="utf-8")
    
    assert is_internal_import("pydescope.parser", project_root=tmp_path) is True

def test_is_internal_import_as_package(tmp_path):
    """Verify true is returned when the import maps to a package containing __init__.py."""

    # Setup package structure: pydescope/__init__.py
    pkg_dir = tmp_path / "pydescope"
    pkg_dir.mkdir()
    init_path = pkg_dir / "__init__.py"
    init_path.write_text("# dummy init", encoding="utf-8")
    
    assert is_internal_import("pydescope", project_root=tmp_path) is True

def test_is_internal_import_not_found(tmp_path):
    """Verify false is returned when an import name does not exist internally."""
    
    assert is_internal_import("external_library.core", project_root=tmp_path) is False