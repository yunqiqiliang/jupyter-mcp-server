import logging

from jupyter_nbmodel_client import NbModelClient, get_jupyter_notebook_websocket_url
from jupyter_kernel_client import KernelClient
from mcp.server.fastmcp import FastMCP
import os

# Initialize FastMCP server
mcp = FastMCP("notebook")

# Constants
NOTEBOOK_PATH = os.getenv("NOTEBOOK_PATH", "notebook.ipynb")
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8888")
TOKEN = os.getenv("TOKEN", "MY_TOKEN")

logger = logging.getLogger(__name__)


@mcp.tool()
def add_execute_code_cell(cell_content: str) -> str:
    """Add and execute a code cell in a Jupyter notebook.
    
    Args:
        cell_content: Code content
        
    Returns:
        str: Success message
    """
    kernel = KernelClient(server_url=SERVER_URL, token=TOKEN)
    kernel.start()
    notebook = NbModelClient(get_jupyter_notebook_websocket_url(server_url=SERVER_URL, token=TOKEN, path=NOTEBOOK_PATH))
    notebook.start()
    
    cell_index = notebook.add_code_cell(cell_content)
    notebook.execute_cell(cell_index, kernel)
    
    notebook.stop()
    kernel.stop()
    
    return "Cell executed"
        
        
@mcp.tool()
def add_markdown_cell(cell_content: str) -> str:
    """Add a markdown cell in a Jupyter notebook.
    
    Args:
        cell_content: Markdown content
        
    Returns:
        str: Success message
    """    
    notebook = NbModelClient(get_jupyter_notebook_websocket_url(server_url=SERVER_URL, token=TOKEN, path=NOTEBOOK_PATH))
    notebook.start()
    
    notebook.add_markdown_cell(cell_content)
    notebook.stop()
    
    return "Markdown cell added"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')