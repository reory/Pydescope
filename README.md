# 🐍 Pydescope: Python Project Dependency Visualiser

![Last Commit](https://img.shields.io/github/last-commit/reory/Pydescope?cacheSeconds=60)
![Repo Size](https://img.shields.io/github/repo-size/reory/Pydescope?cacheSeconds=60)
![License](https://img.shields.io/badge/License-MIT-green)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NetworkX](https://img.shields.io/badge/NetworkX-v3.0+-0052CC?style=for-the-badge&logo=networkx&logoColor=white)
![PyVis](https://img.shields.io/badge/PyVis-v0.3.0+-FF69B4?style=for-the-badge&logo=javascript&logoColor=green)
![Click](https://img.shields.io/badge/Click-v8.0+-3DDC84?style=for-the-badge&logo=python&logoColor=white)

Pydescope is a static analysis tool designed to help developers visualize the internal structure and dependencies of their Python projects. By parsing source code and mapping imports, it generates interactive 2D/3D graphs using NetworkX and PyVis, allowing you to see how different modules interact without the clutter of virtual environments or external libraries.

---

# 📸 Screenshots
* **Pydescope** renders an interactive dependency map of your codebase. 
* **Nodes** represent Python modules and packages, while 
* **Edges** visualize the directed import relationships between them. 
- The interface supports real-time filtering and neighborhood highlighting to help developers audit project coupling and structural integrity at a glance.

![](screenshots/djangocsvcleaner.png)
![](screenshots/internetradio.png)
![](screenshots/invoicefrauddetector.png)
![](screenshots/pydescope.png)

---

# 🧠 Key Features
- Static Analysis: Scans your .py files and directories to build a map of your code.
- Smart Filtering: Automatically ignores venv, __pycache__, and other non-source directories.
- Interactive Graphs: Generates an HTML-based visualization where you can drag nodes, zoom, and highlight neighborhoods.
- Module Tracking: Distinguishes between package initializations (__init__.py) and standard module files.
- Neighborhood Highlight: Click on a node to highlight its direct dependencies and dim the rest of the graph.
- Search/Filter: Use the built-in search bar (powered by TomSelect) to find specific modules.
- Physics Toggle: Enable or disable the physics engine to stabilize the graph layout.

---

# 🏗️ Project Architecture

```
pydescope/
├── .gitignore               # Standard git ignore rules
├── pyproject.toml           # Build system and dependency configuration
├── README.md                # Project documentation
├── CONTRIBUTING.md          # Contributing documentation
├── LICENSE.md               # License documentation
├── pydescope/               # Core logic package
│   ├── __init__.py          # Package initialization
│   ├── analyzer.py          # Logic for parsing imports and code analysis
│   ├── graph_builder.py     # NetworkX graph construction
|   ├── parser.py            # Identifes .py files in projects
│   ├── renderer.py          # PyVis conversion and HTML generation
│   └── utils.py             # Internal helper functions
|   └── cli.py               # User interaction tool
└── lib/                     # Static assets for the final output
    └── bindings/
        └── utils.js         # Custom JS for highlighting and interactivity
```

- Pydescope is built with a modular design to ensure efficient parsing and rendering:
* **parser.py**: The engine that walks through your project and identifies Python files.

* **analyser.py**: Scans individual files to extract import statements and determine relationships.

* **graph_builder.py**: Uses NetworkX to create a mathematical representation of the project dependency tree.

* **renderer.py**: Converts the NetworkX graph into an interactive PyVis HTML file.

* **cli.py**: Provides the Command Line Interface for users to interact with the tool.

---

# 🛠️ Installation
Clone your repository (or navigate to the project folder):

- Prerequisites
Before running Pydescope, ensure you have Python 3.9 or higher installed.

```Bash
cd pydescope
```
## Install in editable mode:
This installs the dependencies and allows you to run the pydescope command directly.

```Bash
pip install -e .
```
## How to Run
Once installed, you can run Pydescope from your terminal.

## Basic Usage
Point Pydescope at any Python project directory you want to analyze:

```Bash
pydescope <path_to_target_project>
Command Options
Output Name: Specify a custom name for your HTML report.
```

```Bash
pydescope <path_to_project> --output my_graph.html
Exclude Directories: Although it ignores venv by default, you can add more exclusions.
```

```Bash
pydescope <path_to_project> --exclude tests,docs
Visualisation Controls
The generated HTML file includes advanced JavaScript-based controls located in the lib/bindings/utils.js file:
```

---

# 💻 Tech Stack

* **NetworkX** Provides the data structure for the graphs and relationships between the files.
* **PyVis** Takes abstract math from NetworkX and converts it into a beautiful HTML/JS interace, that a user can open in a browser.
* **Click** Handles all CLI logic

---

# 📝 Notes for Developers

- The project uses repomix for codebase packing and analysis.
- Static assets for the visualization (CSS/JS) are stored in the lib/ directory.

---

- Built by Roy Peters.😁
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/roy-p-74980b382/)