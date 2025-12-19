from mcp.server.fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP("mcp-documentation-server")

# Register tool using FastMCP decorator
@mcp.tool()
def get_documentation_from_database() -> dict:
    """Returns documentation data from a database."""
    return {
        "title": "How to Use MCP Servers",
        "body": "This is a mocked documentation entry from the database. MCP servers expose tools to LLMs.",
        "source": "mocked_database"
    }

if __name__ == "__main__":
    mcp.run("stdio")
