import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from typing import Any, List

import httpx
from pydantic import BaseModel

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession


class Article(BaseModel):
    title: str | None = None
    description: str | None = None
    content: str | None = None
    url: str | None = None
    image: str | None = None
    publishedAt: str | None = None
    source: dict | None = None


class SearchResult(BaseModel):
    total: int
    articles: List[Article]


@asynccontextmanager
async def lifespan(_server: FastMCP):
    # Load .env file if present so local dev is simple
    load_dotenv()

    api_key = os.environ.get("GNEWS_API_KEY")
    if not api_key:
        raise RuntimeError("GNEWS_API_KEY environment variable is required")

    client = httpx.AsyncClient(base_url="https://gnews.io/api/v4", timeout=10.0)
    try:
        yield {"http_client": client, "api_key": api_key}
    finally:
        await client.aclose()


# Create FastMCP instance (stateless JSON recommended for scale)
mcp = FastMCP("GNews MCP", stateless_http=True, json_response=True, lifespan=lifespan)


@mcp.tool(title="GNews: Search")
async def search(query: str, max: int = 10, lang: str | None = None, country: str | None = None, ctx: Context[ServerSession, dict] | None = None) -> SearchResult:
    """Search news articles matching `query` using the GNews Search endpoint."""
    lc = ctx.request_context.lifespan_context
    client: httpx.AsyncClient = lc["http_client"]
    token: str = lc["api_key"]

    params: dict[str, Any] = {"q": query, "token": token, "max": max}
    if lang:
        params["lang"] = lang
    if country:
        params["country"] = country

    resp = await client.get("/search", params=params)
    resp.raise_for_status()
    data = resp.json()

    articles = [Article(**a) for a in data.get("articles", [])]
    total = data.get("totalArticles") or len(articles)
    return SearchResult(total=total, articles=articles)


@mcp.tool(title="GNews: Top Headlines")
async def top_headlines(topic: str | None = None, max: int = 10, lang: str | None = None, country: str | None = None, ctx: Context[ServerSession, dict] | None = None) -> SearchResult:
    """Return top headlines from GNews.

    `topic` can be one of: world, nation, business, technology, entertainment, sports, science, health
    """
    lc = ctx.request_context.lifespan_context
    client: httpx.AsyncClient = lc["http_client"]
    token: str = lc["api_key"]

    params: dict[str, Any] = {"token": token, "max": max}
    if topic:
        params["topic"] = topic
    if lang:
        params["lang"] = lang
    if country:
        params["country"] = country

    resp = await client.get("/top-headlines", params=params)
    resp.raise_for_status()
    data = resp.json()

    articles = [Article(**a) for a in data.get("articles", [])]
    total = data.get("totalArticles") or len(articles)
    return SearchResult(total=total, articles=articles)


if __name__ == "__main__":
    # Run with streamable-http transport (recommended). Set GNEWS_API_KEY in env first.
    mcp.run(transport="streamable-http")
