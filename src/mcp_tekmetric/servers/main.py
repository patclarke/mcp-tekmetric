"""Main FastMCP server setup for Tekmetric integration."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .tekmetric import tekmetric_mcp

logger = logging.getLogger("mcp-tekmetric.server.main")


async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for Kubernetes probes."""
    logger.debug("Received health check request.")
    return JSONResponse({"status": "ok"})


@asynccontextmanager
async def main_lifespan(app: FastMCP) -> AsyncIterator[None]:
    """Optional lifespan hook — currently unused."""
    logger.info("Tekmetric MCP server starting...")
    yield None
    logger.info("Tekmetric MCP server shutting down.")


main_mcp = FastMCP(
    name="Tekmetric MCP Root",
    description="Root MCP server for Tekmetric integration.",
    lifespan=main_lifespan,
)

# Mount the tekmetric sub-server
main_mcp.mount("tekmetric", tekmetric_mcp)


@main_mcp.custom_route("/healthz", methods=["GET"], include_in_schema=False)
async def _health_check_route(request: Request) -> JSONResponse:
    return await health_check(request)


# Uvicorn entrypoint
asgi_app = main_mcp.sse_app
