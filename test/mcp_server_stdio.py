from mcp.server.fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP("mcp-documentation-server")

# Register tool using FastMCP decorator
@mcp.tool()
def fetch_documentation(topic: str) -> dict:
    """Fetch documentation for a given topic from the database."""
    return {
        "title": f"Documentation for {topic}",
        "body": f"This is a mocked documentation entry for '{topic}'. In a real system, this would be fetched from a database.",
        "source": "mocked_database",
        "topic": topic
    }

if __name__ == "__main__":
    mcp.run("stdio")
