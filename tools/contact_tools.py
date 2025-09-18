"""Contact management tools for SendGrid MCP Server."""

import json
import logging
from typing import Any, Dict, Optional, Union
from fastmcp import Context
from tools import mcp
from client import SendGridClient

logger = logging.getLogger(__name__)


@mcp.tool(
    name="add_contact",
    description="Add or update a contact in your SendGrid account with optional custom fields",
    tags=["contacts", "sendgrid", "marketing"]
)
async def add_contact(
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    custom_fields: Optional[Union[str, Dict[str, Any]]] = None,
    list_ids: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Add or update a contact via SendGrid API."""
    try:
        if ctx:
            await ctx.info(f"Processing contact: {email}")

        # Build contact data
        contact_data = {"email": email}

        if first_name:
            contact_data["first_name"] = first_name
        if last_name:
            contact_data["last_name"] = last_name

        # Handle custom fields
        if custom_fields:
            if isinstance(custom_fields, str):
                try:
                    custom_data = json.loads(custom_fields)
                except json.JSONDecodeError as e:
                    error_msg = f"Invalid JSON in custom_fields: {str(e)}"
                    if ctx:
                        await ctx.error(error_msg)
                    raise ValueError(error_msg)
            else:
                custom_data = custom_fields
            contact_data.update(custom_data)

        # Parse list IDs if provided
        lists = []
        if list_ids:
            lists = [list_id.strip() for list_id in list_ids.split(",")]
            if ctx:
                await ctx.info(f"Adding contact to {len(lists)} list(s)")

        # Prepare request data
        request_data = {
            "contacts": [contact_data]
        }
        if lists:
            request_data["list_ids"] = lists

        if ctx:
            await ctx.info("Sending contact update request to SendGrid")

        client = SendGridClient.from_context(ctx)
        result = await client.make_api_request(
            method="PUT",
            endpoint="/marketing/contacts",
            data=request_data
        )

        if ctx:
            await ctx.info("Contact updated successfully")

        return result

    except Exception as e:
        error_msg = f"Failed to add/update contact {email}: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        raise RuntimeError(error_msg)



@mcp.tool(
    name="get_contact_lists",
    description="Retrieve all contact lists from your SendGrid account",
    tags=["contacts", "sendgrid", "marketing"]
)
async def get_contact_lists(ctx: Context = None) -> Dict[str, Any]:
    """Retrieve all contact lists via SendGrid API."""
    try:
        if ctx:
            await ctx.info("Fetching contact lists from SendGrid")

        client = SendGridClient.from_context(ctx)
        result = await client.make_api_request(
            method="GET",
            endpoint="/marketing/lists"
        )

        if ctx and result.get("result"):
            await ctx.info(f"Retrieved {len(result['result'])} contact list(s)")

        return result

    except Exception as e:
        error_msg = f"Failed to retrieve contact lists: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        raise RuntimeError(error_msg)


