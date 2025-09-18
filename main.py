"""Main entry point for SendGrid MCP Server.

This module initializes and runs the SendGrid MCP Server with FastMCP 2.0.
The server provides email management capabilities through the SendGrid API
with support for dual authentication (environment variables or client tokens).

Key Features:
- Email sending with templates and attachments
- Contact and list management
- Rate limiting and error handling
"""

import logging
import sys
from fastmcp import FastMCP
from config import config
from auth import SendGridTokenVerifier
from tools import init_tools

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if config.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize authentication
auth_handler = SendGridTokenVerifier()

# Create FastMCP server instance
mcp = FastMCP(
    name="SendGrid MCP Server",
    instructions="""
    SendGrid MCP Server provides email management capabilities through the SendGrid API.
    
    Authentication:
    - Uses SendGrid API key for authentication
    - Can be provided via environment variable SENDGRID_API_KEY
    - Or via Authorization header: 'Bearer YOUR-API-KEY'
    
    Available Features:
    1. Email Management:
       - Send emails with HTML/text content
       - Use dynamic templates
       - Track delivery and engagement

    2. Contact Management:
       - Add/update contacts
       - Manage contact lists
    
    Example:
    To send an email, use the send_email tool:
    - Provide recipient(s), subject, and content
    - Optionally set custom sender and content type
    """,
    auth=auth_handler,
    on_duplicate_tools="error",
    on_duplicate_resources="warn",
    on_duplicate_prompts="replace",
    include_fastmcp_meta=True
)


# Initialize tools with the server instance
init_tools(mcp)

if __name__ == "__main__":
    try:
        logger.info("SendGrid MCP Server starting...")
        logger.info(f"Rate limit: {config.rate_limit} requests/second")
        
        if config.sendgrid_api_key:
            logger.info("Default API key configured from environment")
        else:
            logger.info("No default API key - clients must provide their own")
            
        # Run the server with default STDIO transport
        mcp.run()
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)
