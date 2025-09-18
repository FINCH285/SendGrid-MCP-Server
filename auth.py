"""Authentication handler for SendGrid MCP Server.

This module provides Bearer token authentication support:
1. Using an API key from environment variables (configured in .env)
2. Allowing clients to provide their own API key via Bearer token

This enables both:
- Simple setup with a single configured API key
- Multi-tenant usage where different clients can use different SendGrid accounts
"""

from typing import Optional
from fastmcp.server.auth import TokenVerifier
from config import config

class SendGridTokenVerifier(TokenVerifier):
    """Bearer token authentication handler for SendGrid using API key."""

    def __init__(self):
        """Initialize with default API key from config."""
        self.default_token = config.sendgrid_api_key

    async def verify_token(self, token: str) -> bool:
        """Verify that the provided token is a valid SendGrid API key format."""
        # SendGrid API keys start with 'SG.' and are 69 characters long
        if not token:
            return False

        # Basic format validation for SendGrid API keys
        if token.startswith('SG.') and len(token) == 69:
            return True

        # Also accept if it matches our default token (for backwards compatibility)
        if self.default_token and token == self.default_token:
            return True

        return False

    def get_default_token(self) -> Optional[str]:
        """Return the default token if available."""
        return self.default_token