# sokic

A modular graph visualization framework built with a plugin-based architecture. sokic provides flexible data source ingestion (YAML, JSON) and multiple visualization strategies (Block and Simple) through swappable plugins, all served via a Flask web interface.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
  - [1. Install dependencies](#1-install-dependencies)
  - [2. Install core packages and plugins](#2-install-core-packages-and-plugins)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Generating a Graph](#generating-a-graph)
  - [Running the Web Interface](#running-the-web-interface)
- [Plugins](#plugins)
  - [Data Source Plugins](#data-source-plugins)
  - [Visualizer Plugins](#visualizer-plugins)
- [Stylesheet Setup](#stylesheet-setup)
- [Platform Notes](#platform-notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Overview

sokic is designed around a clean separation of concerns:

- **`api`** — Defines the interfaces and contracts that all plugins must implement
- **`core`** — The engine that loads plugins, processes data, and orchestrates rendering
- **Data source plugins** — Read graph data from external formats (YAML, JSON)
- **Visualizer plugins** — Render graph data into visual outputs (interactive graph, bird's-eye view)

This architecture makes it straightforward to add new data formats or visualization strategies without modifying the core system.

---

## Project Structure

```
sokic/
├── api/                              # Plugin API contracts
├── core/                             # Core engine
├── plugins/
│   ├── data_source_plugin_yaml/      # YAML data source plugin
│   ├── data_source_plugin_json/      # JSON data source plugin
│   ├── block_visualizer/             # Graph / network visualizer
│   └── simple_visualizer/            # Bird's-eye view visualizer
├── flask/
│   ├── static/                       # Global stylesheet 
│   └── templates/                    # Html templates of the web application
├── graph_generator.py                # Entry point for graph generation
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## Requirements

- Python 3.8 or higher
- pip

---

## Installation

### 1. Install dependencies

Install all third-party Python packages:

```bash
pip install -r requirements.txt
```

### 2. Install core packages and plugins

Install the API, core engine, and all plugins as local packages:

```bash
pip install ./api ./core ./plugins/data_source_plugin_yaml ./plugins/data_source_plugin_json ./plugins/block_visualizer ./plugins/simple_visualizer
```

> **Note:** These packages are installed from local directories. Any changes you make to plugin source code will require reinstalling the affected package (or installing it in editable mode with `pip install -e ./plugins/<plugin_name>`).

#### Editable installs (recommended for development)

If you are actively developing or modifying plugins, install them in editable mode so changes take effect immediately without reinstalling:

```bash
pip install -e ./api -e ./core \
  -e ./plugins/data_source_plugin_yaml \
  -e ./plugins/data_source_plugin_json \
  -e ./plugins/block_visualizer \
  -e ./plugins/simple_visualizer
```

---

## Configuration

sokic discovers and loads plugins automatically at runtime. Ensure all plugins are installed before running the application. No additional configuration files are required for a basic setup.

---

## Usage

### Generating a Graph

Run the graph generator script from the project root:

**Windows:**
```bash
python graph_generator.py
```

**Linux / macOS:**
```bash
python3 graph_generator.py
```

This will process the configured data source and produce graph output using the active visualizer plugin.

### Running the Web Interface

sokic renders visualizations inside HTML templates served by Flask. To view the Graph and Bird View correctly, the global stylesheet must be linked in every template's `<head>`:

```html
<head>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
```

> **Important:** Without this stylesheet, the Graph and Bird View visualizations will not render correctly. See [Stylesheet Setup](#stylesheet-setup) for details.

Start the Flask development server (adjust the entry point to match your app's filename):

```bash
# Windows
python app.py

# Linux / macOS
python3 app.py
```

Then open your browser at `http://127.0.0.1:5000`.

---

## Plugins

### Data Source Plugins

sokic supports loading graph data from multiple file formats via swappable data source plugins.

| Plugin | Package Directory | Supported Format |
|--------|------------------|-----------------|
| YAML Data Source | `plugins/data_source_plugin_yaml` | `.yaml` / `.yml` |
| JSON Data Source | `plugins/data_source_plugin_json` | `.json` |

Each data source plugin reads a file, parses its structure, and produces a normalized graph representation consumed by the core engine.

### Visualizer Plugins

Visualizer plugins transform the normalized graph data into rendered output.

| Plugin | Package Directory | Output |
|--------|------------------|--------|
| Block Visualizer | `plugins/block_visualizer` | Interactive graph / network view |
| Simple Visualizer | `plugins/simple_visualizer` | Bird's-eye / overview render |

---

## Stylesheet Setup

The `static/style.css` file contains the CSS required for both the **Graph** and **Bird View** visualizers to render correctly. This file is served by Flask's static file handler.

**Every template that renders a visualization must include:**

```html
<head>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
```

Using `url_for('static', filename='style.css')` ensures Flask resolves the correct path regardless of where the template is served from. Hardcoding a relative path (e.g., `href="static/style.css"`) may break in nested routes.

---

## Platform Notes

| Platform | Command |
|----------|---------|
| Windows | `python graph_generator.py` |
| Linux | `python3 graph_generator.py` |
| macOS | `python3 graph_generator.py` |

On Linux and macOS, `python` may point to Python 2. Always use `python3` explicitly to ensure Python 3 is used.

To verify your Python version:
```bash
python3 --version
```

---

## Troubleshooting

**Graph or Bird View renders without styles**
Ensure the `<link rel="stylesheet">` tag using `url_for` is present in the `<head>` of your template. Verify that `static/style.css` exists and the Flask static folder is correctly configured.

**Plugin not found at runtime**
Confirm all plugins were installed successfully by running:
```bash
pip show data-source-plugin-yaml data-source-plugin-json block-visualizer simple-visualizer
```
If any are missing, re-run the install command from [Step 2](#2-install-core-packages-and-plugins).

**`python` command not found on Linux**
Use `python3` instead. You can also create an alias:
```bash
alias python=python3
```

**Changes to plugin code not taking effect**
If plugins were installed normally (not in editable mode), reinstall the modified plugin:
```bash
pip install ./plugins/<plugin_name>
```
Or switch to editable installs (see [Editable installs](#editable-installs-recommended-for-development)).

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-new-plugin`
3. Install packages in editable mode for development
4. Implement your changes, following the plugin API contracts defined in `./api`
5. Submit a pull request with a clear description of the change

When adding a new plugin, place it under `plugins/` and ensure it implements the interface defined in the `api` package.

---

