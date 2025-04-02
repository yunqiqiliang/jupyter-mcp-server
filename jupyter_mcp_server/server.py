# Copyright (c) 2023-2024 Datalayer, Inc.
#
# BSD 3-Clause License

import logging
import os

from mcp.server.fastmcp import FastMCP

from jupyter_kernel_client import KernelClient
from jupyter_nbmodel_client import (
    get_jupyter_notebook_websocket_url,
    NbModelClient,
)


mcp = FastMCP("jupyter")


NOTEBOOK_PATH = os.getenv("NOTEBOOK_PATH", "notebook.ipynb")

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8888")

TOKEN = os.getenv("TOKEN", "MY_TOKEN")


logger = logging.getLogger(__name__)


kernel = KernelClient(server_url=SERVER_URL, token=TOKEN)
kernel.start()


@mcp.tool()
async def add_markdown_cell(cell_content: str) -> str:
    """Add a markdown cell in a Jupyter notebook.
    
    Args:
        cell_content: Markdown content
        
    Returns:
        str: Success message
    """    
    notebook = NbModelClient(get_jupyter_notebook_websocket_url(server_url=SERVER_URL, token=TOKEN, path=NOTEBOOK_PATH))
    await notebook.start()
    notebook.add_markdown_cell(cell_content)
    await notebook.stop()
    return "Jupyter Markdown cell added."


@mcp.tool()
async def add_execute_code_cell(cell_content: str) -> str:
    """Add and execute a code cell in a Jupyter notebook.
    
    Args:
        cell_content: Code content
        
    Returns:
        str: Success message
    """
    notebook = NbModelClient(get_jupyter_notebook_websocket_url(server_url=SERVER_URL, token=TOKEN, path=NOTEBOOK_PATH))
    await notebook.start()
    cell_index = notebook.add_code_cell(cell_content)
    notebook.execute_cell(cell_index, kernel)
    await notebook.stop()
    return "Jupyter Code Cell added and executed."


if __name__ == "__main__":
    mcp.run(transport='stdio')
