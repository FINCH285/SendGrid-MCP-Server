"""Tools package for SendGrid MCP Server."""

from fastmcp import FastMCP
from typing import Optional

# Global MCP server instance
mcp: Optional[FastMCP] = None

def init_tools(server_instance: FastMCP):
    """Initialize tools with the FastMCP server instance."""
    global mcp
    mcp = server_instance

    # Import all tool modules to register them with the MCP server
    from . import email_tools
    from . import contact_tools

__all__ = [
    "email_tools",
    "contact_tools",
    "init_tools"
]
