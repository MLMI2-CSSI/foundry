"""Foundry MCP (Model Context Protocol) server.

This module provides an MCP server that allows AI agents to interact
with Foundry datasets programmatically.

The MCP server exposes tools for:
- Searching datasets
- Getting dataset schemas
- Loading data
- Listing available datasets

Usage:
    # From command line
    foundry mcp start

    # Programmatically
    from foundry.mcp.server import run_server
    run_server()
"""

from .server import create_server, run_server

__all__ = ["create_server", "run_server"]
