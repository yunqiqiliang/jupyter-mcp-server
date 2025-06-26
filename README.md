# Jupyter MCP Server

A Model Context Protocol (MCP) server that provides access to Jupyter notebooks and kernels.

## Overview

The Jupyter MCP Server enables seamless integration between MCP clients and Jupyter environments, allowing you to:

- Execute code in Jupyter kernels
- Access notebook content and metadata
- Manage kernel sessions
- Run notebooks programmatically

## Features

- **Kernel Management**: Start, stop, and manage Jupyter kernels
- **Code Execution**: Execute code cells in various languages (Python, R, Scala, etc.)
- **Notebook Access**: Read and write notebook files
- **Session Management**: Handle multiple concurrent kernel sessions
- **Resource Monitoring**: Track kernel resource usage

## Installation

```bash
# Install from source
git clone https://github.com/datalayer/jupyter-mcp-server.git
cd jupyter-mcp-server
pip install -e .
```

## Usage

### Starting the MCP Server

```bash
# Start the server
jupyter-mcp-server

# Or with custom configuration
jupyter-mcp-server --port 8080 --host localhost
```

### Using with MCP Clients

The server exposes several MCP tools for interacting with Jupyter:

- `execute_code`: Execute code in a kernel
- `get_notebook`: Read notebook content
- `list_kernels`: List available kernels
- `start_kernel`: Start a new kernel session
- `stop_kernel`: Stop a kernel session

### Configuration

Create a configuration file to customize server behavior:

```json
{
    "kernels": {
        "python": {
            "name": "python3",
            "display_name": "Python 3"
        }
    },
    "notebook_dir": "./notebooks",
    "max_kernels": 5
}
```

## Development

### Setup

```bash
# Install development dependencies
pip install -e ".[test,lint,typing]"

# Run tests
pytest

# Format code
ruff format .

# Type checking
mypy jupyter_mcp_server
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jupyter_mcp_server

# Run specific test file
pytest jupyter_mcp_server/tests/test_server.py
```

## Architecture

The server consists of several key components:

- **MCP Handler**: Handles MCP protocol communication
- **Kernel Manager**: Manages Jupyter kernel lifecycle
- **Notebook Manager**: Handles notebook file operations
- **Session Manager**: Tracks active sessions and resources

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

BSD 3-Clause License. See [LICENSE](LICENSE) for details.

## Links

- [Jupyter Project](https://jupyter.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Datalayer](https://datalayer.io/)