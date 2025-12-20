from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import contextlib
from test.mcp_server_multiple_http import mcp as email_mcp_server
from test.mcp_server_http import mcp as docs_mcp_server

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(docs_mcp_server.session_manager.run())
        await stack.enter_async_context(email_mcp_server.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# EXACTLY like the video:
app.mount("/docs", docs_mcp_server.streamable_http_app())
app.mount("/email", email_mcp_server.streamable_http_app())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=10000, log_level="debug")
