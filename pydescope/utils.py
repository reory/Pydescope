# normalise module names
# colour internal modules differently
# detect architecture violations
# cluster internal modules

import logging
import sys
from pathlib import Path

def setup_logging(level=logging.INFO):
    """Initialises the global logging configuration"""

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def get_logger(name: str):
    return logging.getLogger(name)
    

def normalise_module_name(path: str) -> str:
    """Convert a file path like 'pydescope\\cli.py' into 'pydescope.cli'"""
    return path.replace("/", ".").replace("\\", ".").replace(".py", "")


def is_internal_import(import_name: str, project_root: Path) -> bool:
    """
    Returns True if the import resolves to a file or package inside the project.
    Handles both:
      - module files:   api/routes.py
      - packages:       api/__init__.py
    """
    parts = import_name.split(".")

    # Check for a plain module file e.g pydescope/parser.py
    as_file = project_root / Path("/".join(parts) + ".py")
    if as_file.exists():
        return True

    # Check for a package directory eg pydescope/__init__.py
    as_package = project_root / Path("/".join(parts)) / "__init__.py"
    if as_package.exists():
        return True
    return False
