<!--
  ~ Copyright (c) 2023-2024 Datalayer, Inc.
  ~
  ~ BSD 3-Clause License
-->

[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# 🪐 ✨ Jupyter MCP Server

[![Github Actions Status](https://github.com/datalayer/jupyter-mcp-server/workflows/Build/badge.svg)](https://github.com/datalayer/jupyter-mcp-server/actions/workflows/build.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/jupyter-mcp-server)](https://pypi.org/project/jupyter-mcp-server)
[![smithery badge](https://smithery.ai/badge/@datalayer/jupyter-mcp-server)](https://smithery.ai/server/@datalayer/jupyter-mcp-server)

Jupyter MCP Server is a [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server implementation that provides interaction with 📓 Jupyter notebooks running in any JupyterLab (works also with your 💻 local JupyterLab).

![Jupyter MCP Server](https://assets.datalayer.tech/jupyter-mcp/jupyter-mcp-server-claude-demo.gif)

## Features

* Connects MCP clients (e.g., Claude Desktop) to a running JupyterLab instance.
* Provides a wide array of tools for notebook interaction, including:
    * **Cell Management:** Add, delete, move, split, edit source.
    * **Execution:** Execute specific cells or all cells, retrieve output.
    * **File System:** List directory contents, get file content (with image resizing).
    * **Kernel Introspection:** List kernel variables, list installed packages.
    * **Package Management:** Install packages into the kernel environment.
    * **Notebook State:** Search cells, get all cell info/outputs, set target notebook path.

## Requirements

* **Python:** >= 3.10 recommended. Using a dedicated environment manager like Conda/Miniconda is **strongly advised** (see Setup).
* **JupyterLab:** A running JupyterLab instance.
* **Jupyter Collaboration Extension:** Specifically version `jupyter_collaboration==2.0.1`.
* **`datalayer_pycrdt`:** Required dependency.
* **Docker:** Required to build and run the MCP server container (which includes necessary patches).
* **Pillow:** Required by the server (included in Docker build) for image handling.
* **An MCP Client:** Such as [Claude Desktop](https://claude.ai/download).

## Installation and Setup

Follow these steps carefully to create a stable environment based on debugging outcomes:

### 1. Create a Dedicated Conda Environment (Recommended):

Open your terminal (Anaconda Prompt or similar). Running the terminal **"As Administrator"** might be necessary for initial `pip` installs if conda base permissions are restricted on your system, although using a dedicated environment usually avoids this.

```bash
# Create a clean environment (Python 3.10 worked during debugging)
conda create -n jupyter_mcp_env python=3.10 -y

# Activate the environment
conda activate jupyter_mcp_env
```

or 

```bash
# Create a clean environment (Python 3.10 worked during debugging)
python3.10 -m venv jupyter_mcp_env
# Activate the environment
source jupyter_mcp_env/bin/activate
```


Remember to activate this environment in any terminal before running pip or jupyter lab commands for this project.

### 2. Install Core Jupyter Components:

```bash
# Use 'python -m pip' to ensure correct pip in the activated env
python -m pip install jupyterlab ipykernel
```

### 3. Install Specific jupyter_collaboration Version:

Newer versions caused issues during debugging. Version 2.0.1 is required.

```bash
# Install the required v2.0.1
python -m pip install "jupyter_collaboration==2.0.1"
```

### 4. Handle pycrdt Dependencies:

Follow the specific uninstall/reinstall sequence:

```bash
# Uninstall potentially conflicting versions
python -m pip uninstall -y pycrdt datalayer_pycrdt

# Install the required version
python -m pip install datalayer_pycrdt
```

### 5. Enable the Collaboration Extension:

Ensure the extension is enabled within your environment:

```bash
jupyter server extension enable jupyter_collaboration --py --sys-prefix
```

### 6. Build the Patched Docker Image:

The included Dockerfile contains patches identified during debugging. Build the image locally:

```bash
# Navigate to the directory containing the Dockerfile
# cd /path/to/your/jupyter-mcp-server/
docker build -t jupyter-mcp-server:latest .
```

### 7. Start JupyterLab:

#### Start Docker Compose

Download docker compose file from [here](https://github.com/yunqiqiliang/jupyter-mcp-server/blob/main/jupyter_lab_server/docker-compose.yml) 
```bash
docker compose up -d
```

#### Or Start Local Server

Make sure your `jupyter_mcp_env` conda environment is activated.

Create config.json file and set your login infor as below:

```json
{
    "username": "your clickzetta lakehouse user name",
    "password": "your clickzetta lakehouse password",
    "service": "api.clickzetta.com",
    "instance": "your clickzetta lakehouse instance name",
    "workspace": "your clickzetta lakehouse workspac name",
    "schema": "your clickzetta lakehouse schema",
    "vcluster": "your clickzetta lakehouse vcluster name",
    "sdk_job_timeout": 60,
    "hints": {
      "sdk.job.timeout": 60,
      "query_tag": "test_zettapark_vector_ns227206",
      "cz.storage.parquet.vector.index.read.memory.cache": "true",
      "cz.storage.parquet.vector.index.read.local.cache": "false",
      "cz.sql.table.scan.push.down.filter": "true",
      "cz.sql.table.scan.enable.ensure.filter": "true",
      "cz.storage.always.prefetch.internal": "true",
      "cz.optimizer.generate.columns.always.valid": "true",
      "cz.sql.index.prewhere.enabled": "true",
      "cz.storage.parquet.enable.io.prefetch": "false"
    }
  }
```

```bash
# Use a strong, unique token!
# --ip=0.0.0.0 allows the Docker container to connect
jupyter lab --port 8888 --IdentityProvider.token YOUR_SECURE_TOKEN --ip 0.0.0.0
```

* **Security:** Replace `YOUR_SECURE_TOKEN` with a strong, unique password or token. Do not use weak tokens.
* **Windows Terminal:** If using Windows Terminal/Command Prompt, ensure "QuickEdit Mode" is disabled for the terminal window running Jupyter Lab to prevent connection hangs (Right-click title bar -> Properties -> Options -> Untick QuickEdit Mode).
* **Firewall:** Ensure your OS firewall allows incoming connections on port 8888, especially from Docker's network interface.

## Configuration

The MCP server (running in Docker) reads its configuration from environment variables passed via the MCP client configuration (e.g., `claude_desktop_config.json`). Key variables:

* **SERVER_URL:** URL of your running JupyterLab (e.g., `http://host.docker.internal:8888` for Docker Desktop Win/Mac, `http://localhost:8888` for Linux with `--network=host`). Do not include the token here.
* **TOKEN:** The exact token used with `--IdentityProvider.token` for JupyterLab.
* **NOTEBOOK_PATH:** Initial target notebook path relative to JupyterLab's start directory (e.g., `notebook.ipynb`). Changeable via the `set_target_notebook` tool.
* **LOG_LEVEL:** Server logging verbosity (`DEBUG`, `INFO`, `WARNING`). Default: `INFO`.
* **OUTPUT_WAIT_DELAY:** Default wait time (seconds) for `get_cell_output`. Default: 0.5.

## Usage with Claude Desktop

1. Install Claude Desktop.
2. Locate `claude_desktop_config.json`.
3. Add/modify the `mcpServers` block, adapting for your OS and configuration:

### Claude Configuration (macOS / Windows with Docker Desktop)

```json
{
  "mcpServers": {
    "jupyter": {
      "command": "docker",
      "args": [
        "run",
        "-i", 
        "--rm", 
        "-e", "SERVER_URL", 
        "-e", "TOKEN",
        "-e", "NOTEBOOK_PATH",
        "-e", "LOG_LEVEL=INFO", 
        "jupyter-mcp-server:latest" 
      ],
      "env": {
        "SERVER_URL": "http://host.docker.internal:8888", 
        "TOKEN": "YOUR_SECURE_TOKEN", 
        "NOTEBOOK_PATH": "notebook.ipynb" 
      }
    }
  }
}
```

### Claude Configuration (Linux)

```json
{
  "mcpServers": {
    "jupyter": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--network=host", 
        "-e", "SERVER_URL",
        "-e", "TOKEN",
        "-e", "NOTEBOOK_PATH",
        "-e", "LOG_LEVEL=INFO",
        "jupyter-mcp-server:latest"
      ],
      "env": {
        "SERVER_URL": "http://localhost:8888", 
        "TOKEN": "YOUR_SECURE_TOKEN", 
        "NOTEBOOK_PATH": "notebook.ipynb" 
      }
    }
  }
}
```

4. Save the config file and restart Claude Desktop.

## Available Tools

This server provides the following tools for interacting with Jupyter:

* **list_notebook_directory()** → str
  * Lists files and directories in the same location as the current target notebook. Directories end with /.
* **get_file_content(file_path: str, max_image_dim: int = 1024)** → str
  * Retrieves file content. Text is returned directly. Images are resized if large (preserving aspect ratio, max dimension max_image_dim) and returned as a base64 Data URI string. Binary files described.
* **set_target_notebook(new_notebook_path: str)** → str
  * Changes the target notebook file path for subsequent tool calls (session only). Path must be relative.
* **add_cell(content: str, cell_type: str, index: Optional[int] = None)** → str
  * Adds a new cell ('code' or 'markdown') with specified content at index (appends if index is None or invalid). Uses robust Yjs type creation.
* **add_code_cell_on_bottom(cell_content: str)** → str
  * Adds a code cell at the end of the notebook.
* **execute_cell(cell_index: int)** → str
  * Sends execution request for a cell (fire-and-forget via asyncio.to_thread). Does not wait for completion. Returns confirmation message or error.
* **execute_all_cells()** → str
  * Sends execution requests for all code cells sequentially (fire-and-forget). Returns confirmation message or error.
* **get_cell_output(cell_index: int, wait_seconds: float = OUTPUT_WAIT_DELAY)** → str
  * Retrieves the combined text output(s) of a code cell, waiting briefly (wait_seconds). Returns output string or status message.
* **delete_cell(cell_index: int)** → str
  * Deletes a specific cell by its index.
* **move_cell(from_index: int, to_index: int)** → str
  * Moves a cell using a simple delete/re-insert approach for better live rendering stability.
* **search_notebook_cells(search_string: str, case_sensitive: bool = False)** → List[Dict[str, Any]]
  * Searches all cell sources for search_string. Returns list of matching cells [{'index', 'cell_type', 'source'}].
* **split_cell(cell_index: int, line_number: int)** → str
  * Splits a cell at a specific line_number (1-based). Uses robust Yjs type creation.
* **get_all_cells()** → list[dict[str, Any]]
  * Retrieves info for all cells [{'index', 'cell_type', 'source', 'execution_count'}]. Converts Yjs types to Python types.
* **edit_cell_source(cell_index: int, new_content: str)** → str
  * Replaces the source content of a specific cell. Uses correct Yjs Text API.
* **get_kernel_variables(wait_seconds: int = 2)** → str
  * Lists variables in the kernel namespace using %whos. Creates/executes/deletes a temporary cell.
* **get_all_outputs()** → dict[int, str]
  * Retrieves outputs for all code cells. Returns dict {index: output_string} or status like [No output], [Not executed].
* **install_package(package_name: str, timeout_seconds: int = 60)** → str
  * Installs a package into the kernel using !pip install. Creates/executes/deletes a temporary cell. Output includes pip logs.
* **list_installed_packages(wait_seconds: int = 5)** → str
  * Lists installed packages using !pip list. Creates/executes/deletes a temporary cell.

## Troubleshooting

If you encounter issues during setup or usage, please consult the detailed troubleshooting guide which includes solutions found during debugging.

➡️ **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## Building from Source

You can build the Docker image directly from the source code (which includes necessary patches):

```bash
# Make sure you are in the project's root directory (where Dockerfile is)
docker build -t jupyter-mcp-server:latest .
```

## Building

You can build the Docker image it from source.

```bash
make build-docker
```

## Installing via Smithery

To install Jupyter MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@datalayer/jupyter-mcp-server):

```bash
npx -y @smithery/cli install @datalayer/jupyter-mcp-server --client claude
```
