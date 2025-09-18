# SendGrid MCP Server

A production-ready **Model Context Protocol (MCP) Server** for SendGrid email services, built with **FastMCP 2.0**. This server enables AI models like Claude, GPT, and others to send emails, manage contacts, and interact with SendGrid's powerful email platform.

## 🚀 Features

- **📧 Email Management**: Send HTML/text emails with templates and attachments
- **👥 Contact Management**: Add contacts and manage mailing lists
- **🔐 Secure Authentication**: Bearer token authentication with fallback support
- **⚡ Rate Limiting**: Built-in API rate limiting to prevent abuse
- **🛡️ Production Ready**: Comprehensive error handling and logging
- **🔧 Easy Configuration**: Environment-based configuration management

## 📋 Requirements

- Python 3.8+
- SendGrid API Key
- FastMCP 2.0

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FINCH285/SendGrid-MCP-Server.git
   cd SendGrid-MCP-Server
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your SendGrid configuration:
   ```env
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   DEFAULT_FROM_EMAIL=your-verified-email@example.com
   DEFAULT_FROM_NAME=Your Name
   DEFAULT_TEMPLATE_ID=your-template-id
   RATE_LIMIT=10
   DEBUG=false
   ```

## 🚀 Usage

### Running the Server

```bash
python main.py
```

The server will start and listen for MCP connections via STDIO.

### Available Tools

#### Email Tools
- **`send_email`** - Send HTML/text emails to multiple recipients
- **`get_template_info`** - Fetch SendGrid template details
- **`send_template_email`** - Send emails using dynamic templates

#### Contact Tools
- **`add_contact`** - Add/update contacts with custom fields
- **`get_contact_lists`** - Retrieve all contact lists

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SENDGRID_API_KEY` | Your SendGrid API key | Yes | - |
| `DEFAULT_FROM_EMAIL` | Default sender email (must be verified) | No | - |
| `DEFAULT_FROM_NAME` | Default sender name | No | - |
| `DEFAULT_TEMPLATE_ID` | Default template ID for template emails | No | - |
| `RATE_LIMIT` | API requests per second limit | No | `10` |
| `DEBUG` | Enable debug logging | No | `false` |

### Authentication

The server supports two authentication methods:

1. **Environment Variable**: Set `SENDGRID_API_KEY` in your `.env` file
2. **Bearer Token**: Pass API key via Authorization header in MCP requests

## 📚 API Examples

### Send Email
```python
# Via MCP client
result = await mcp_client.call_tool("send_email", {
    "to_emails": ["recipient@example.com"],
    "subject": "Hello from SendGrid MCP!",
    "html_content": "<h1>Hello World!</h1>",
    "from_email": "sender@example.com"
})
```

### Add Contact
```python
# Via MCP client
result = await mcp_client.call_tool("add_contact", {
    "email": "contact@example.com",
    "first_name": "John",
    "last_name": "Doe"
})
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Model      │◄──►│   FastMCP       │◄──►│   SendGrid      │
│  (Claude/GPT)   │    │   Server        │    │     API         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │ MCP Protocol          │ HTTP/REST            │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Tools Layer   │    │   Auth Layer    │    │   Config Layer  │
│ • email_tools   │    │ • Bearer Token  │    │ • Environment   │
│ • contact_tools │    │ • API Key Auth  │    │ • Rate Limits   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/FINCH285/SendGrid-MCP-Server/issues)
- **SendGrid Documentation**: [SendGrid API Docs](https://docs.sendgrid.com/)
- **FastMCP Documentation**: [FastMCP Docs](https://github.com/jlowin/fastmcp)

## 🙏 Acknowledgments

- [SendGrid](https://sendgrid.com/) for their excellent email API
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP framework
- [Anthropic](https://anthropic.com/) for the Model Context Protocol specification
