"""SendGrid API client wrapper."""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union
import httpx
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, Content
from config import config

logger = logging.getLogger(__name__)


class SendGridClient:
    """Async wrapper for SendGrid API client."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize SendGrid API client with configuration."""
        self._api_key = api_key or config.sendgrid_api_key
        if not self._api_key:
            raise ValueError("SendGrid API key is required")
            
        self.client = SendGridAPIClient(api_key=self._api_key)
        self.base_url = "https://api.sendgrid.com/v3"
        
        # Rate limiting
        self._rate_limit = config.rate_limit
        self._last_request_time = 0.0

    @classmethod
    def from_context(cls, ctx=None) -> 'SendGridClient':
        """Create a client instance using API key from context or default.

        Args:
            ctx: FastMCP context that may contain authenticated Bearer token

        Returns:
            SendGridClient instance with appropriate API key
        """
        # Try to get API key from FastMCP context first (Bearer token)
        if ctx and hasattr(ctx, 'token') and ctx.token:
            # Use the Bearer token provided by the MCP client
            return cls(api_key=ctx.token)

        # Fall back to default API key from environment configuration
        return cls(api_key=config.sendgrid_api_key)
        
    async def _rate_limit_request(self) -> None:
        """Apply rate limiting delay between API requests."""
        if self._rate_limit > 0:
            current_time = asyncio.get_event_loop().time()
            time_since_last = current_time - self._last_request_time
            min_interval = 1.0 / self._rate_limit
            
            if time_since_last < min_interval:
                await asyncio.sleep(min_interval - time_since_last)
            
            self._last_request_time = asyncio.get_event_loop().time()
    
    async def send_email(
        self,
        to_emails: Union[str, List[str]],
        subject: str,
        content: str,
        content_type: str = "text/html",
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        template_id: Optional[str] = None,
        dynamic_template_data: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Send email via SendGrid API with optional template support."""
        await self._rate_limit_request()
        
        try:
            # Use defaults if not provided
            sender_email = from_email or config.default_from_email
            sender_name = from_name or config.default_from_name
            
            # Only use default template if it's a template-based email
            if dynamic_template_data:
                template_id = template_id or config.default_template_id
            
            if not sender_email:
                raise ValueError("From email is required")
            
            if dynamic_template_data and not template_id:
                raise ValueError("Template ID is required when using dynamic template data")
            
            # Template validation is handled by AI using MCP tools

            # Create the mail object
            from_addr = From(sender_email, sender_name)
            
            # Handle multiple recipients
            if isinstance(to_emails, str):
                to_emails = [to_emails]
            
            to_list = [To(email) for email in to_emails]
            
            mail = Mail(
                from_email=from_addr,
                to_emails=to_list,
                subject=Subject(subject)
            )
            
            # Add content
            if template_id:
                mail.template_id = template_id
                if dynamic_template_data:
                    mail.dynamic_template_data = dynamic_template_data
            else:
                mail.add_content(Content(content_type, content))
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    mail.add_attachment(attachment)
            
            # Send the email
            response = self.client.send(mail)
            
            return {
                "status_code": response.status_code,
                "message": "Email sent successfully",
                "message_id": response.headers.get("X-Message-Id"),
                "to_emails": to_emails
            }
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise
    
    async def make_api_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to SendGrid API endpoint."""
        await self._rate_limit_request()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                if response.content:
                    return response.json()
                else:
                    return {"status": "success", "status_code": response.status_code}
                    
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                raise


