from mcp.server.fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP("mcp-email-server")

# Register tool using FastMCP decorator
@mcp.tool()
def get_emails() -> dict:
    """Returns email data from a database."""
    return {
        "title": "Emails",
        "body": "This is a mocked email entry from the database.",
        "source": "mocked_database"
    }


@mcp.tool()
def write_email(subject: str, body: str) -> dict:
    """Writes an email to a database."""
    return {
        "title": "Email Written",
        "body": f"Email with subject '{subject}' and body '{body}' has been written to the database.",
        "source": "mocked_database"
    }



if __name__ == "__main__":
    mcp.run("streamable-http")