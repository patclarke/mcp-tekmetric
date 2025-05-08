"""Tekmetric FastMCP server instance and tool definitions."""

import json
import logging
import os
from typing import Annotated, Any

import httpx
from fastmcp import Context, FastMCP
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

tekmetric_mcp = FastMCP(
    name="Tekmetric API MCP",
    description="Provides tools for interacting with the Tekmetric API.",
    streamable=True,
    transport="sse",
)


@tekmetric_mcp.tool(
    name="get_shops",
    tags={"tekmetric", "read"},
)
async def get_shops(ctx: Context[Any, None]) -> str:
    """
    Return the list of shops accessible to the provided Tekmetric API token.

    Args:
        ctx: The FastMCP context.

    Returns:
        JSON string containing a list of shops with:
        - id, name, nickname, phone, email, website, fullAddress
    """
    token = os.getenv("TEKMETRIC_API_KEY")
    if not token:
        logger.error("Missing TEKMETRIC_API_KEY environment variable.")
        return json.dumps({"error": "Missing TEKMETRIC_API_KEY environment variable."}, indent=2)

    url = "https://sandbox.tekmetric.com/api/v1/shops"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.exception("Failed to fetch shops from Tekmetric")
            return json.dumps({"error": f"Failed to fetch shops: {str(e)}"}, indent=2)

        shops = response.json()
        simplified = [
            {
                "id": shop["id"],
                "name": shop["name"],
                "nickname": shop.get("nickname", ""),
                "phone": shop.get("phone", ""),
                "email": shop.get("email", ""),
                "website": shop.get("website", ""),
                "fullAddress": shop.get("address", {}).get("fullAddress", "")
            }
            for shop in shops
        ]
        return json.dumps(simplified, indent=2)


@tekmetric_mcp.custom_route("/healthz", methods=["GET"], include_in_schema=False)
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})
