# Static analysis core

import ast
from pathlib import Path
from .utils import is_internal_import, normalise_module_name, get_logger

logger = get_logger(__name__)

class ImportParser:
    def __init__(self, root: Path):
        self.root = root

    def parse_file(self, file_path: Path, package: str = ""):
        
        logger.debug(f"Parsing imports in: {file_path}") # Log every turn
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(text)
        except SyntaxError:
            # Log the error
            logger.warning(f"Syntax error in {file_path}. Skipping.")
            return [] # Skip broken files

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(("absolute", alias.name))

            elif isinstance(node, ast.ImportFrom):
                if node.level > 0:
                    if node.module:
                        # Relative import — resolve to full dotted name
                        # e.g. "parser" inside pydescope/ becomes "pydescope.parser"
                        full_name = (
                            f"{package}.{node.module}" 
                            if package else node.module
                        )
                        imports.append(("relative", full_name))
                else:
                    if node.module:
                        imports.append(("absolute", node.module))
    
        # Assign the list to the variable.
        valid_imports = [
            name for kind, name in imports
            if kind == "relative" or is_internal_import(name, self.root)
        ]

        # Log the results
        logger.debug(
            f"Found {len(valid_imports)} internal imports in {file_path.name}")

        # return the variable
        return valid_imports

    def parse_project(self):
        EXCLUDE_DIRS = {
            "venv", ".venv", "__pycache__", 
            ".git", "*.egg-info",
            "node_modules", "build", "dist"
        }
        results = {}
        logger.info("Starting project walk...")
        for file in self.root.rglob("*.py"):

            # Skip any file whose path contains an excluded directory
            if any(part in EXCLUDE_DIRS for part in file.parts):
                # Only logs if verbose is used
                logger.debug(f"Ignoring excluded path: {file}")
                continue

            rel = file.relative_to(self.root)

            # Normalise the key: "pydescope\cli.py" -> "pydescope.cli"
            module_name = normalise_module_name(str(rel))

            # Package is everything left of the last dot: "pydescope.cli"
            package = ".".join(module_name.split(".")[:-1])

            results[module_name] = self.parse_file(file, package)

        logger.info(f"Scanning complete. Processed {len(results)} modules")  
        return results