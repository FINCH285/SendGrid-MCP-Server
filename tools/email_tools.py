"""Email sending and template tools for SendGrid MCP Server."""

import logging
from typing import Any, Dict, Optional, Union
from fastmcp import Context
from tools import mcp
from client import SendGridClient
from config import config

logger = logging.getLogger(__name__)


@mcp.tool(
    name="send_email",
    description="Send an email with text or HTML content to one or more recipients",
    tags=["email", "sendgrid"]
)
async def send_email(
    to_emails: str,
    subject: str,
    content: str,
    content_type: str = "text/html",
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send email with text/HTML content via SendGrid API."""
    try:
        # Parse multiple emails if comma-separated
        email_list = [email.strip() for email in to_emails.split(",")]
        
        if ctx:
            await ctx.info(f"Sending email to {len(email_list)} recipient(s)")
        
        client = SendGridClient.from_context(ctx)
        result = await client.send_email(
            to_emails=email_list,
            subject=subject,
            content=content,
            content_type=content_type,
            from_email=from_email,
            from_name=from_name
        )
        
        if ctx:
            await ctx.info("Email sent successfully")
        
        return result

    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        raise RuntimeError(error_msg)

@mcp.tool(
    name="get_template_info",
    description="Get detailed information about a SendGrid template for AI analysis",
    tags=["email", "sendgrid", "templates"]
)
async def get_template_info(
    template_id: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Fetch template information from SendGrid API for AI analysis.
    If template_id is not provided, uses the default template ID from config.
    """
    try:
        # Use default template ID if none provided
        template_id = template_id or config.default_template_id
        
        if not template_id:
            error_msg = "Template ID is required but none was provided or found in config"
            if ctx:
                await ctx.error(error_msg)
            raise ValueError(error_msg)
        
        if ctx:
            await ctx.info(f"Fetching template information for ID: {template_id}")
        
        client = SendGridClient.from_context(ctx)
        template_response = await client.make_api_request(
            "GET",
            f"templates/{template_id}"
        )
        
        if ctx:
            await ctx.info("Template information retrieved successfully")
        
        return template_response
        
    except Exception as e:
        error_msg = f"Failed to get template info: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        raise RuntimeError(error_msg)


@mcp.tool(
    name="send_template_email",
    description="""Send an email using a SendGrid dynamic template with personalized data.
First use get_template_info to understand the template structure, required fields ({{name}}, etc), then customize dynamic_template_data.""",
    tags=["email", "sendgrid", "templates"]
)
async def send_template_email(
    to_emails: str,
    dynamic_template_data: Dict[str, Any],
    template_id: Optional[str] = None,
    subject: Optional[str] = None,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send email using SendGrid dynamic template with data substitution."""
    try:
        # Validate template_id
        template_id = template_id or config.default_template_id
        if not template_id:
            error_msg = "Template ID is required but none was provided or found in config"
            if ctx:
                await ctx.error(error_msg)
            raise ValueError(error_msg)
        
        # Parse multiple emails if comma-separated
        email_list = [email.strip() for email in to_emails.split(",")]
        
        if ctx:
            await ctx.info(f"Sending template email to {len(email_list)} recipient(s)")
            await ctx.info(f"Using template ID: {template_id}")
        
        client = SendGridClient.from_context(ctx)
        result = await client.send_email(
            to_emails=email_list,
            subject=subject or "Email from Template",
            content="",  # Content comes from template
            template_id=template_id,
            dynamic_template_data=dynamic_template_data,
            from_email=from_email,
            from_name=from_name
        )
        
        if ctx:
            await ctx.info("Template email sent successfully")
        
        return result
        
    except Exception as e:
        error_msg = f"Failed to send template email: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        raise RuntimeError(error_msg)


