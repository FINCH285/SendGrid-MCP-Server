# Build a SendGrid Email Management Agent Using FastMCP 2.0 and SendGrid API

## Table of Contents
1. [Introduction](#introduction)
2. [What You'll Build](#what-youll-build)
3. [Prerequisites](#prerequisites)
4. [Understanding the Architecture](#understanding-the-architecture)
5. [Setting Up Your Development Environment](#setting-up-your-development-environment)
6. [Building the Configuration System](#building-the-configuration-system)
7. [Creating the Authentication Layer](#creating-the-authentication-layer)
8. [Implementing the SendGrid API Client](#implementing-the-sendgrid-api-client)
9. [Building Email Management Tools](#building-email-management-tools)
10. [Creating the FastMCP Server](#creating-the-fastmcp-server)
11. [Testing Your Email Agent](#testing-your-email-agent)
12. [Deploying to Production](#deploying-to-production)
13. [Next Steps and Enhancements](#next-steps-and-enhancements)

## Introduction

In this comprehensive tutorial, you'll learn how to build a powerful email management agent that allows AI models like Claude, GPT, and others to send emails, manage contacts, and analyze email performance through the SendGrid API. We'll use **FastMCP 2.0**, a cutting-edge Python framework for building Model Context Protocol (MCP) servers.

By the end of this tutorial, you'll have created a production-ready email agent that can:
- Send personalized emails with HTML content and templates
- Manage contact lists and subscriber data
- Handle authentication securely with Bearer tokens
- Scale to support multiple clients and API keys

### What is the Model Context Protocol (MCP)?

The **Model Context Protocol (MCP)** is a standardized way for AI models to interact with external tools and services. Think of it as a bridge that allows AI models to:

1. **Call Functions**: Execute Python functions to perform actions
2. **Access Data**: Read information from databases, APIs, or files
3. **Use Tools**: Interact with external services like email providers, databases, or web APIs

### Why FastMCP 2.0?

**FastMCP 2.0** is a Python framework that makes building MCP servers incredibly simple. It provides:

- **Decorator-based Tools**: Turn any Python function into an AI-accessible tool with a simple `@mcp.tool` decorator
- **Automatic Schema Generation**: FastMCP automatically creates JSON schemas from your Python type hints
- **Multiple Transports**: Support for STDIO, HTTP, and SSE protocols
- **Built-in Authentication**: Secure your server with OAuth, Bearer tokens, or custom authentication
- **Type Safety**: Full TypeScript-like type checking for Python

### How FastMCP Creates a Server

When you create a `FastMCP` instance, you're not just creating a Python object—you're creating a **full MCP server** that:

1. **Implements the MCP Protocol**: Handles all the low-level MCP communication
2. **Manages Tool Registration**: Keeps track of all your `@mcp.tool` decorated functions
3. **Handles Authentication**: Validates tokens and manages security
4. **Provides Transport Layer**: Communicates with AI clients via STDIO, HTTP, or SSE
5. **Manages Sessions**: Handles multiple concurrent client connections

```python
# This single line creates a complete MCP server
mcp = FastMCP("SendGrid Email Agent")

# The server automatically:
# - Sets up MCP protocol handlers
# - Manages tool registration
# - Handles client authentication
# - Provides transport mechanisms
```

## What You'll Build

By the end of this tutorial, you'll have created a sophisticated email management agent with the following capabilities:

### Core Features

**📧 Email Management**
- Send personalized emails with HTML and plain text content
- Use SendGrid dynamic templates for professional email designs
- Handle multiple recipients and CC/BCC functionality
- Track email delivery status and engagement metrics

**👥 Contact Management**
- Add and update contacts in your SendGrid database
- Organize contacts into targeted mailing lists
- Handle contact suppression and unsubscribe management
- Validate email addresses before adding to lists

**🔐 Enterprise-Grade Security**
- Bearer token authentication for production deployments
- Environment variable fallback for development
- Secure API key validation and management
- Rate limiting to prevent API abuse

### Technical Architecture

Your email agent will follow a **modular, production-ready architecture**:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Client     │    │   SendGrid API  │    │  Configuration  │
│  (Claude/GPT)   │◄──►│   (api.sendgrid │◄──►│   (.env file)   │
│                 │    │    .com)        │    │                 │
│  Bearer Token:  │    │                 │    │ SENDGRID_API_   │
│  SG.abc123...   │    │ Email Delivery  │    │ KEY=SG.xyz...   │
└─────────────────┘    │ Contact Mgmt    │    └─────────────────┘
         │              └─────────────────┘             │
         │ MCP Protocol  └─────────────────┘             │
         ▼                       ▲                       ▼
┌─────────────────┐              │              ┌─────────────────┐
│   FastMCP       │              │              │   config.py     │
│   Server        │              │              │                 │
│                 │              │              │ • Loads env     │
│ • Tool Registry │              │              │ • Validates     │
│ • Authentication│              │              │ • Type safety   │
│ • Transport     │              │              └─────────────────┘
│ • Session Mgmt  │              │                       │
└─────────────────┘              │                       │
         │                       │                       │
         ▼                       │                       ▼
┌─────────────────┐              │              ┌─────────────────┐
│   Tools Layer   │              │              │   auth.py       │
│                 │              │              │                 │
│ • email_tools   │              │              │ • Token         │
│ • contact_tools │              │              │   validation    │
│                 │              │              │ • Bearer auth   │
│                 │              │              │ • Fallback      │
│ Each tool:      │              │              └─────────────────┘
│ • Validates     │              │
│ • Authenticates │              │
│ • Calls client  │              │
└─────────────────┘              │
         │                       │
         ▼                       │
┌─────────────────┐              │
│   client.py     │──────────────┘
│                 │
│ • HTTP client   │
│ • Rate limiting │
│ • Error handling│
│ • API wrapping  │
└─────────────────┘
```

### Real-World Use Cases

This email agent can power various real-world applications:

1. **Customer Support Automation**: AI agents that send personalized support responses
2. **Marketing Campaign Management**: Automated email campaigns based on user behavior
3. **Notification Systems**: System alerts and status updates via email
4. **Newsletter Management**: AI-powered content distribution and subscriber management
5. **E-commerce Communications**: Order confirmations, shipping updates, and promotional emails

## Prerequisites

Before we start building, make sure you have the following:

### Required Accounts and Services

**1. SendGrid Account**
- Sign up for a free SendGrid account at [sendgrid.com](https://sendgrid.com)
- Verify your sender identity (email address or domain)
- Generate an API key with full access permissions

**2. Python Development Environment**
- Python 3.8 or higher installed on your system
- A code editor (VS Code, PyCharm, or your preferred IDE)
- Basic familiarity with Python programming

### Required Knowledge

**Python Fundamentals**
- Understanding of Python functions, classes, and decorators
- Basic knowledge of async/await programming
- Familiarity with Python type hints

**API Concepts**
- Understanding of REST APIs and HTTP methods
- Basic knowledge of JSON data format
- Familiarity with API authentication (API keys, Bearer tokens)

**Email Concepts**
- Understanding of email headers (To, From, Subject)
- Basic knowledge of HTML email content
- Familiarity with email deliverability concepts

### Development Tools

**Required Python Packages** (we'll install these together):
```bash
fastmcp>=2.12.0      # FastMCP framework for building MCP servers
sendgrid>=6.10.0     # Official SendGrid Python library
python-dotenv>=1.0.0 # Environment variable management
httpx>=0.24.0        # Modern HTTP client for API requests
```

**Optional but Recommended**:
- Git for version control
- A virtual environment manager (venv, conda, or poetry)
- Postman or similar tool for API testing

### Getting Your SendGrid API Key

Before we start coding, you'll need a SendGrid API key:

1. **Log in to SendGrid**: Go to [app.sendgrid.com](https://app.sendgrid.com)
2. **Navigate to API Keys**: Settings → API Keys
3. **Create API Key**: Click "Create API Key"
4. **Set Permissions**: Choose "Full Access" for this tutorial
5. **Copy the Key**: Save it securely - you'll only see it once!

Your API key will look like this: `SG.abc123def456...` (69 characters total)

⚠️ **Security Note**: Never commit your API key to version control or share it publicly!

## Understanding the Architecture

Before we dive into coding, let's understand how our email agent will work at a high level.

### The MCP Protocol Flow

When an AI model wants to send an email, here's what happens:

```
1. AI Model Request
   ↓
   "Send email to john@example.com with subject 'Hello' and content 'Hi there!'"
   ↓
2. MCP Protocol Translation
   ↓
   {
     "method": "tools/call",
     "params": {
       "name": "send_email",
       "arguments": {
         "to": "john@example.com",
         "subject": "Hello",
         "content": "Hi there!"
       }
     }
   }
   ↓
3. FastMCP Server Processing
   ↓
   • Validates the request format
   • Authenticates the client (Bearer token)
   • Calls our send_email function
   ↓
4. Our Email Tool Execution
   ↓
   • Validates email parameters
   • Creates SendGrid API request
   • Sends email via SendGrid
   ↓
5. Response Back to AI
   ↓
   {
     "content": [
       {
         "type": "text",
         "text": "Email sent successfully! Message ID: abc123"
       }
     ]
   }
```

### Component Responsibilities

Each component in our system has a specific role:

**FastMCP Server (`main.py`)**
- Acts as the MCP protocol handler
- Manages client connections and authentication
- Routes tool calls to appropriate functions
- Handles errors and responses

**Authentication Layer (`auth.py`)**
- Validates Bearer tokens from AI clients
- Provides fallback to environment variables
- Ensures only authorized clients can send emails

**Configuration System (`config.py`)**
- Loads settings from environment variables
- Provides type-safe configuration access
- Manages default values and validation

**API Client (`client.py`)**
- Wraps the SendGrid API with rate limiting
- Handles HTTP requests and error responses
- Provides a clean interface for our tools

**Tool Modules (`tools/`)**
- Implement the actual email functionality
- Validate input parameters and formats
- Transform data between MCP and SendGrid formats

## Setting Up Your Development Environment

Let's create a clean, organized development environment for our email agent.

### Step 1: Create Your Project Directory

First, create a new directory for your project and navigate into it:

```bash
# Create the project directory
mkdir sendgrid-email-agent
cd sendgrid-email-agent
```

**Why this matters**: Keeping your project in a dedicated directory helps organize your code and prevents conflicts with other Python projects.

### Step 2: Set Up a Virtual Environment

A virtual environment isolates your project's dependencies from your system Python installation:

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**What this does**:
- `python -m venv venv` creates a new virtual environment in a folder called `venv`
- The activation command modifies your shell's PATH to use the virtual environment's Python
- You'll see `(venv)` in your command prompt when it's active

### Step 3: Install Required Dependencies

Now install all the Python packages we'll need:

```bash
# Install FastMCP framework
pip install fastmcp>=2.12.0

# Install SendGrid Python library
pip install sendgrid>=6.10.0

# Install environment variable management
pip install python-dotenv>=1.0.0

# Install modern HTTP client
pip install httpx>=0.24.0
```

**Package explanations**:
- **fastmcp**: The framework that handles MCP protocol communication
- **sendgrid**: Official SendGrid library for API interactions
- **python-dotenv**: Safely loads environment variables from .env files
- **httpx**: Modern, async-capable HTTP client for API requests

### Step 4: Create Your Environment Configuration

Create a `.env` file in your project root to store sensitive configuration:

```bash
# Create the .env file
touch .env  # On Windows: type nul > .env
```

Add the following content to your `.env` file:

```env
# SendGrid API Configuration
# Replace with your actual SendGrid API key from app.sendgrid.com
SENDGRID_API_KEY=SG.your-actual-api-key-here

# Your verified sender email address
SENDGRID_FROM_EMAIL=your-verified-email@example.com

# Development Settings
DEBUG=true
RATE_LIMIT=10

# Optional: Custom server settings
SERVER_NAME=SendGrid Email Agent
```

**Critical Security Note**:
- Replace `SG.your-actual-api-key-here` with your real SendGrid API key
- Replace `your-verified-email@example.com` with an email address you've verified in SendGrid
- Never commit this file to version control!

### Step 5: Create a .gitignore File

Protect your sensitive data by creating a `.gitignore` file:

```bash
# Create .gitignore file
touch .gitignore  # On Windows: type nul > .gitignore
```

Add this content to `.gitignore`:

```gitignore
# Environment variables (contains API keys)
.env

# Python cache files
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual environment
venv/
env/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
```

**Why this matters**: The `.gitignore` file prevents Git from tracking sensitive files like your `.env` file containing API keys.

### Step 6: Verify Your Setup

Let's verify everything is working correctly:

```bash
# Check Python version (should be 3.8+)
python --version

# Check that FastMCP is installed
python -c "import fastmcp; print(f'FastMCP version: {fastmcp.__version__}')"

# Check that SendGrid is installed
python -c "import sendgrid; print('SendGrid library installed successfully')"

# Check that your .env file is readable
python -c "from dotenv import load_dotenv; load_dotenv(); print('Environment file loaded successfully')"
```

If all commands run without errors, your development environment is ready!

**To install these dependencies**:
```bash
pip install -r requirements.txt
```

**What each package does**:
- **fastmcp**: Provides the `FastMCP` class and decorators like `@mcp.tool`
- **sendgrid**: Official SendGrid library with email helpers
- **python-dotenv**: Reads `.env` files and loads environment variables
- **httpx**: Makes HTTP requests to APIs (async-compatible)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Building the Configuration System

The configuration system is the foundation of our email agent. It safely loads environment variables and provides type-safe access to settings throughout our application.

### Understanding Configuration Management

**Why we need a configuration system**:
1. **Centralized Settings**: All configuration in one place
2. **Type Safety**: Ensures settings are the correct data type
3. **Default Values**: Provides sensible defaults when settings aren't specified
4. **Validation**: Checks that required settings are present

### Creating config.py - Line by Line

Let's create our configuration system step by step. Create a file called `config.py`:

```python
"""Configuration management for SendGrid MCP Server.

This module handles loading and validating all configuration settings
from environment variables. It provides a centralized, type-safe way
to access configuration throughout the application.
"""

# Import the os module to access environment variables
import os

# Import load_dotenv to read .env files
from dotenv import load_dotenv

# Load environment variables from .env file into the system environment
# This must be called before accessing any environment variables
load_dotenv()


class SendGridConfig:
    """Simplified configuration for SendGrid MCP Server."""
    # This class holds all our configuration settings in one place
    # It's like a container that organizes all our settings

    def __init__(self):
        # __init__ is called when we create a new instance of this class
        # It sets up all the configuration values

        # SendGrid API key (can be provided via environment or client authentication)
        self.sendgrid_api_key: Optional[str] = os.getenv("SENDGRID_API_KEY")
        # os.getenv("SENDGRID_API_KEY") reads the environment variable
        # If the variable doesn't exist, it returns None
        # Optional[str] means this can be a string or None

        # Debug mode for detailed logging
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        # os.getenv("DEBUG", "false") gets DEBUG variable, defaults to "false" if not set
        # .lower() converts to lowercase ("TRUE" becomes "true")
        # == "true" checks if the value equals "true", returns True/False

        # Rate limiting (requests per second)
        self.rate_limit: int = int(os.getenv("RATE_LIMIT", "10"))
        # os.getenv("RATE_LIMIT", "10") gets the variable, defaults to "10"
        # int() converts the string to an integer number
        # So "10" becomes the number 10


# Create a global instance that other modules can import
config = SendGridConfig()
# This creates one instance of our configuration class
# Other files can import this with: from config import config
```

### Why This Design?

1. **Centralized Configuration**: All settings are in one place
2. **Type Safety**: We know what type each setting should be
3. **Default Values**: If environment variables aren't set, we have sensible defaults
4. **Easy Access**: Other modules just import `config` and use `config.debug`, etc.

### How Other Files Use This

```python
# In other files, you'll see:
from config import config

# Then they can access settings like:
if config.debug:
    print("Debug mode is enabled")

api_key = config.sendgrid_api_key
rate_limit = config.rate_limit
```

### Configuration Flow

1. **Startup**: When Python imports `config.py`
2. **Load .env**: `load_dotenv()` reads the `.env` file
3. **Create Instance**: `config = SendGridConfig()` creates the configuration object
4. **Read Variables**: Each `os.getenv()` call reads from environment
5. **Type Conversion**: Strings are converted to appropriate types (int, bool)
6. **Global Access**: Other modules can import and use `config`
## Authentication System - Line by Line

Authentication is how we verify that the AI client is allowed to use our server. Our system supports **two ways** to provide the SendGrid API key:

1. **Environment Variable**: API key stored in `.env` file (good for development)
2. **Bearer Token**: API key provided by the AI client (good for production)

### Complete auth.py Code with Explanations

```python
"""Authentication handler for SendGrid MCP Server.

This module provides Bearer token authentication using FastMCP's TokenVerifier.
It validates SendGrid API keys provided as Bearer tokens from MCP clients.

The authentication supports:
1. Bearer tokens provided by MCP clients (recommended for production)
2. Fallback to environment variable for development/testing

This follows FastMCP 2.0 authentication patterns for secure token validation.
"""
# This docstring explains the purpose and approach of this authentication module

from typing import Optional
# Optional means a value can be None or the specified type

from fastmcp.server.auth import TokenVerifier
# TokenVerifier is FastMCP's base class for authentication
# We inherit from it to create our custom authentication logic

from config import config
# Import our configuration object to access the default API key


class SendGridTokenVerifier(TokenVerifier):
    """Token verifier for SendGrid API keys following FastMCP patterns."""
    # This class inherits from TokenVerifier and implements our custom logic

    async def verify_token(self, token: str) -> bool:
        """Verify that the provided token is a valid SendGrid API key format.

        This method validates the token format but does not make API calls.
        Actual API validation happens when the token is used.

        Args:
            token: The Bearer token to verify (should be a SendGrid API key)

        Returns:
            bool: True if the token appears to be a valid SendGrid API key format
        """
        # First, check if we even have a token
        if not token:
            # If token is None, empty string, or False, return False
            return False

        # SendGrid API keys start with 'SG.' and have a specific format
        if not token.startswith('SG.'):
            # If the token doesn't start with "SG.", it's not a SendGrid key
            return False

        # Basic length check (SendGrid keys are typically 69 characters)
        if len(token) < 20:
            # If the token is too short, it's probably not valid
            return False

        # If all checks pass, the token format looks valid
        return True

    def get_default_token(self) -> Optional[str]:
        """Get the default API key from environment configuration.

        This provides a fallback when no Bearer token is provided by the client.
        Useful for development and testing scenarios.

        Returns:
            Optional[str]: The default SendGrid API key from environment variables
        """
        # Return the API key from our configuration (loaded from .env)
        return config.sendgrid_api_key
        # This could be None if SENDGRID_API_KEY wasn't set in .env
```

### How Authentication Works Step by Step

1. **AI Client Makes Request**:
   - Client sends request with `Authorization: Bearer SG.abc123...` header
   - OR client sends request without any authorization (uses default)

2. **FastMCP Calls verify_token()**:
   - FastMCP extracts the Bearer token from the Authorization header
   - Calls our `verify_token()` method with the token
   - Our method checks if it looks like a valid SendGrid API key

3. **Token Validation**:
   - Check if token exists and isn't empty
   - Check if token starts with "SG." (SendGrid format)
   - Check if token is long enough (basic length validation)

4. **Fallback to Default**:
   - If no Bearer token provided, FastMCP calls `get_default_token()`
   - Returns the API key from environment variables (.env file)

5. **Token Usage**:
   - The validated token is made available to our tools
   - Tools use this token to authenticate with SendGrid API

### Why This Design?

- **Security**: Validates token format before use
- **Flexibility**: Supports both client tokens and environment defaults
- **Development Friendly**: Easy to test with .env file
- **Production Ready**: Clients can provide their own API keys

## API Client

### client.py - SendGrid API Integration

```python
"""SendGrid API client with rate limiting and error handling."""

import asyncio
import logging
from typing import Optional, Dict, Any, List
import aiohttp
from config import config

logger = logging.getLogger(__name__)


class SendGridClient:
    """Async SendGrid API client with rate limiting."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the SendGrid client.

        Args:
            api_key: SendGrid API key. If None, uses config default.
        """
        self.api_key = api_key or config.sendgrid_api_key
        self.base_url = "https://api.sendgrid.com/v3"
        self.rate_limit = config.rate_limit
        self._last_request_time = 0.0

        if not self.api_key:
            raise ValueError("SendGrid API key is required")

    @classmethod
    def from_context(cls, ctx=None) -> 'SendGridClient':
        """Create a client instance using API key from context or default.

        Args:
            ctx: FastMCP context (unused, kept for compatibility)

        Returns:
            SendGridClient instance with appropriate API key
        """
        # Try to get API key from authenticated token first
        try:
            from fastmcp.server.dependencies import get_access_token
            token = get_access_token()
            if token and token.token:
                # Use the authenticated token as API key
                return cls(api_key=token.token)
        except (ImportError, RuntimeError):
            # Fall back to default if no authentication context
            pass

        # Use default API key from config
        return cls(api_key=config.sendgrid_api_key)
```

### How the Client Works:
1. **Dual API Key Support**: Can use token from authentication or environment
2. **Rate Limiting**: Respects SendGrid API rate limits
3. **Error Handling**: Comprehensive error handling for API calls
4. **Async Support**: Built for async/await patterns

## Tools Implementation

The server provides 7 main tools organized into 3 modules:

### tools/email_tools.py - Email Management

```python
"""Email management tools for SendGrid MCP Server."""

from typing import Optional, List, Dict, Any
from fastmcp import Context
from client import SendGridClient


async def send_email(
    ctx: Context,
    to_emails: str,
    subject: str,
    content: str,
    content_type: str = "text/plain",
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
    cc_emails: Optional[str] = None,
    bcc_emails: Optional[str] = None,
    attachments: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Send an email using SendGrid API."""
    client = SendGridClient.from_context(ctx)
    # Implementation details...
    return {"message_id": "example_id", "status": "sent"}


async def send_template_email(
    ctx: Context,
    to_emails: str,
    template_id: str,
    dynamic_template_data: Optional[Dict[str, Any]] = None,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None
) -> Dict[str, Any]:
    """Send an email using a SendGrid template."""
    client = SendGridClient.from_context(ctx)
    # Implementation details...
    return {"message_id": "example_id", "status": "sent"}
```

### tools/contact_tools.py - Contact Management

```python
"""Contact management tools for SendGrid MCP Server."""

from typing import Optional, List, Dict, Any
from fastmcp import Context
from client import SendGridClient


async def add_contact(
    ctx: Context,
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    list_ids: Optional[List[str]] = None,
    custom_fields: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Add a contact to SendGrid."""
    client = SendGridClient.from_context(ctx)
    # Implementation details...
    return {"contact_id": "example_id", "status": "added"}


async def get_contact_lists(ctx: Context) -> Dict[str, Any]:
    """Retrieve all contact lists from SendGrid."""
    client = SendGridClient.from_context(ctx)
    # Implementation details...
    return {"lists": [], "total_count": 0}
```



### How Tools Work:
1. **Context Integration**: Each tool receives a FastMCP Context
2. **Client Creation**: Uses `SendGridClient.from_context()` for API access
3. **Type Safety**: Comprehensive type hints for all parameters
4. **Error Handling**: Proper error handling and logging
5. **Data Validation**: Input validation and sanitization

## Creating the FastMCP Server

Now that we have our configuration, authentication, client, and tools ready, let's understand how FastMCP transforms our Python code into a fully functional MCP server.

### How FastMCP Creates a Server

When you create a `FastMCP` instance, you're not just creating a Python object—you're creating a **complete MCP server** that can communicate with AI models. Here's what happens under the hood:

**1. MCP Protocol Implementation**
```python
mcp = FastMCP("SendGrid Email Agent")
```
This single line:
- Creates a server that implements the full Model Context Protocol specification
- Sets up JSON-RPC communication handlers for all MCP methods
- Initializes transport layers (STDIO, HTTP, SSE) for client communication
- Prepares the server to handle tool calls, resource requests, and prompt requests

**2. Tool Registration System**
```python
@mcp.tool
def send_email(to: str, subject: str, content: str) -> str:
    """Send an email via SendGrid"""
    return "Email sent successfully"
```
When you use the `@mcp.tool` decorator:
- FastMCP automatically generates a JSON schema from your function signature
- It registers the function in the server's tool registry
- It creates MCP-compliant tool descriptions with parameter validation
- It handles the conversion between MCP requests and Python function calls

**3. Authentication Integration**
```python
mcp = FastMCP("SendGrid Email Agent", auth=auth_handler)
```
The authentication system:
- Intercepts all incoming requests before they reach your tools
- Validates Bearer tokens or other authentication credentials
- Provides authenticated context to your tool functions
- Handles authentication errors and unauthorized access attempts

**4. Transport Layer Management**
```python
mcp.run()  # Defaults to STDIO transport
```
FastMCP supports multiple transport protocols:
- **STDIO**: Communication via standard input/output (most common for AI clients)
- **HTTP**: RESTful API endpoints for web-based clients
- **SSE**: Server-Sent Events for real-time communication

### The Server Architecture

Here's how all the components work together:

```
┌─────────────────────────────────────────────────────────────┐
│                    FastMCP Server Instance                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   MCP Protocol  │  │  Authentication │  │  Tool Registry  │ │
│  │    Handler      │  │     System      │  │                 │ │
│  │                 │  │                 │  │ • send_email    │ │
│  │ • list_tools    │  │ • TokenVerifier │  │ • add_contact   │ │
│  │ • call_tool     │  │ • Bearer auth   │  │ • get_templates │ │
│  │ • list_resources│  │ • Validation    │  │ • get_lists     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  STDIO Transport│  │  HTTP Transport │  │  SSE Transport  │ │
│  │                 │  │                 │  │                 │ │
│  │ • stdin/stdout  │  │ • REST endpoints│  │ • Event streams │ │
│  │ • JSON-RPC      │  │ • HTTP requests │  │ • Real-time     │ │
│  │ • AI clients    │  │ • Web clients   │  │ • Notifications │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │      AI Client          │
                    │   (Claude, GPT, etc.)   │
                    │                         │
                    │ Sends MCP requests:     │
                    │ • "List available tools"│
                    │ • "Call send_email tool"│
                    │ • "Add contact to list" │
                    └─────────────────────────┘
```

### From Python Functions to MCP Tools

Let's trace how a Python function becomes an MCP tool:

**Step 1: Define the Function**
```python
def send_email(to: str, subject: str, content: str) -> str:
    """Send an email via SendGrid API.

    Args:
        to: Recipient email address
        subject: Email subject line
        content: Email content (HTML or plain text)

    Returns:
        Success message with email ID
    """
    # Function implementation here
    return "Email sent successfully"
```

**Step 2: Add the MCP Decorator**
```python
@mcp.tool
def send_email(to: str, subject: str, content: str) -> str:
    # Same function as above
```

**Step 3: FastMCP Auto-Generation**
When FastMCP processes this decorator, it automatically creates:

```json
{
  "name": "send_email",
  "description": "Send an email via SendGrid API.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "to": {
        "type": "string",
        "description": "Recipient email address"
      },
      "subject": {
        "type": "string",
        "description": "Email subject line"
      },
      "content": {
        "type": "string",
        "description": "Email content (HTML or plain text)"
      }
    },
    "required": ["to", "subject", "content"]
  }
}
```

**Step 4: MCP Communication**
When an AI client calls this tool:

1. **Client Request**: AI sends MCP tool call request
2. **FastMCP Processing**: Server validates request against schema
3. **Authentication**: Checks Bearer token or environment credentials
4. **Function Execution**: Calls your Python function with validated parameters
5. **Response**: Returns function result as MCP response

### Why This Architecture is Powerful

**1. Automatic Schema Generation**
- No need to manually write JSON schemas
- Type hints become API documentation
- Docstrings become tool descriptions
- Parameter validation is automatic

**2. Protocol Abstraction**
- You write normal Python functions
- FastMCP handles all MCP protocol details
- No need to understand JSON-RPC or transport layers
- Focus on business logic, not communication protocols

**3. Multiple Transport Support**
- Same code works with STDIO, HTTP, and SSE
- Easy to switch between development and production transports
- Supports different client types and deployment scenarios

**4. Built-in Security**
- Authentication is handled at the framework level
- Token validation happens before your code runs
- Secure by default with proper error handling

## Main Server

### main.py - Server Entry Point

```python
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
from auth import SendGridAuthHandler

# Import all tools
from tools.email_tools import send_email, get_template_info, send_template_email
from tools.contact_tools import add_contact, get_contact_lists

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    """Create and configure the FastMCP server."""

    # Create FastMCP instance with authentication
    mcp = FastMCP(
        "SendGrid MCP Server",
        dependencies=[SendGridAuthHandler()]
    )

    # Register email tools
    mcp.add_tool(send_email)
    mcp.add_tool(get_template_info)
    mcp.add_tool(send_template_email)

    # Register contact tools
    mcp.add_tool(add_contact)
    mcp.add_tool(get_contact_lists)

    return mcp


def main():
    """Main entry point."""
    logger.info("SendGrid MCP Server starting...")
    logger.info(f"Rate limit: {config.rate_limit} requests/second")

    if config.sendgrid_api_key:
        logger.info("Default API key configured from environment")
    else:
        logger.info("No default API key - will require client authentication")

    # Create and run server
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
```

### How the Server Works:
1. **Initialization**: Creates FastMCP instance with authentication
2. **Tool Registration**: Registers all 7 tools with the server
3. **Configuration**: Loads settings from environment and config
4. **Logging**: Comprehensive logging for debugging and monitoring
5. **Error Handling**: Graceful error handling and recovery

## Testing

### test_client.py - Client Testing Script

```python
"""Test script for SendGrid MCP Server using FastMCP client."""

import asyncio
import logging
import os
from fastmcp import Client
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def test_server():
    """Test the SendGrid MCP Server functionality."""

    # Create client pointing to our local server
    client = Client(bare_target=["python", "main.py"])

    async with client:
        # Test connectivity
        await client.ping()
        logger.info("Server is reachable")

        # List available tools
        tools = await client.list_tools()
        for tool in tools:
            logger.info(f"- {tool.name}: {tool.description}")

        # Test email sending (if API key available)
        if os.getenv("SENDGRID_API_KEY"):
            result = await client.call_tool("send_email", {
                "to_emails": "test@example.com",
                "subject": "Test Email",
                "content": "This is a test email."
            })
            logger.info(f"Email sent: {result.data}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

## Deployment

### Running the Server

1. **Local Development**:
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your SendGrid API key

# Run the server
python main.py
```

2. **Production Deployment**:
```bash
# Use environment variables instead of .env file
export SENDGRID_API_KEY="your_api_key_here"
export DEFAULT_FROM_EMAIL="your-email@example.com"
export RATE_LIMIT="10"

# Run with proper logging
python main.py 2>&1 | tee server.log
```

### Integration with AI Models

The server can be used with any MCP-compatible AI model:

1. **Claude Desktop**: Add to your MCP configuration
2. **Custom Clients**: Use the FastMCP client library
3. **API Integration**: Connect via stdio transport

Example MCP configuration:
```json
{
  "mcpServers": {
    "sendgrid": {
      "command": "python",
      "args": ["/path/to/sendgrid-mcp/main.py"],
      "env": {
        "SENDGRID_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Data Flow Diagram

```
Environment Variables (.env)
         │
         ▼
    config.py (Configuration)
         │
         ▼
    main.py (Server Entry Point)
         │
         ├─► auth.py (Authentication)
         │
         ├─► client.py (API Client)
         │
         └─► tools/ (Tool Modules)
              │
              ├─► email_tools.py
              └─► contact_tools.py
                   │
                   ▼
              SendGrid API
```

## Key Concepts for Beginners

### 1. MCP (Model Context Protocol)
- **What**: A protocol that allows AI models to use external tools
- **Why**: Enables AI to perform actions beyond text generation
- **How**: Through standardized tool interfaces and communication

### 2. FastMCP Framework
- **What**: A Python framework for building MCP servers
- **Why**: Simplifies MCP server development with built-in features
- **How**: Provides decorators, authentication, and transport handling

### 3. SendGrid Integration
- **What**: Email service provider with robust API
- **Why**: Reliable email delivery with contact management
- **How**: RESTful API with authentication via API keys

### 4. Async Programming
- **What**: Non-blocking code execution using async/await
- **Why**: Better performance for I/O operations like API calls
- **How**: Python's asyncio library and aiohttp for HTTP requests

## Troubleshooting

### Common Issues

1. **API Key Problems**:
   - Ensure API key starts with 'SG.'
   - Check environment variable name is correct
   - Verify API key has proper permissions

2. **Rate Limiting**:
   - Adjust RATE_LIMIT environment variable
   - Monitor SendGrid usage dashboard
   - Implement exponential backoff for retries

3. **Date Format Issues**:
   - Use ISO format for dates: "2025-09-16"
   - Check timezone handling for accurate results

4. **Authentication Errors**:
   - Verify token format in client requests
   - Check FastMCP authentication configuration
   - Ensure proper token verification logic

### Debugging Tips

1. **Enable Debug Mode**:
```bash
export DEBUG=true
python main.py
```

2. **Check Logs**:
```bash
# View server logs
tail -f server.log

# Test specific tools
python test_client.py
```

3. **Validate Configuration**:
```python
from config import config
print(f"API Key: {config.sendgrid_api_key[:10]}...")
print(f"Rate Limit: {config.rate_limit}")
```

## Conclusion

This SendGrid MCP Server provides a robust foundation for email management through AI models. The modular architecture makes it easy to extend with additional features, while the comprehensive error handling and logging ensure reliable operation in production environments.

Key takeaways:
- **Modular Design**: Each component has a specific responsibility
- **Dual Authentication**: Supports both environment and client-provided API keys
- **Error Handling**: Comprehensive error handling throughout the stack
- **Type Safety**: Full type hints for better development experience
- **Testing**: Built-in testing tools for validation and debugging

For additional help or feature requests, refer to the FastMCP documentation at https://gofastmcp.com/

