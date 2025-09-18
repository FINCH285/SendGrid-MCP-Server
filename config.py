"""Configuration management for SendGrid MCP Server."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SendGridConfig:
    """Simplified configuration for SendGrid MCP Server."""

    def __init__(self):
        # SendGrid API key (can be provided via environment or client authentication)
        self.sendgrid_api_key: Optional[str] = os.getenv("SENDGRID_API_KEY")

        # Optional default sender settings
        self.default_from_email: Optional[str] = os.getenv("DEFAULT_FROM_EMAIL")
        self.default_from_name: Optional[str] = os.getenv("DEFAULT_FROM_NAME")

        # Optional template settings
        self.default_template_id: Optional[str] = os.getenv("DEFAULT_TEMPLATE_ID")

        # Rate limiting (requests per second)
        self.rate_limit: int = int(os.getenv("RATE_LIMIT", "10"))

        # Debug mode
        self.debug: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")


# Global configuration instance
config = SendGridConfig()
