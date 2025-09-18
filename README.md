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

### Authentication

The server supports two authentication methods:

1. **Environment Variable**: Set `SENDGRID_API_KEY` in your `.env` file
2. **Bearer Token**: Pass API key via Authorization header in MCP requests

## 📚 SendGrid Configuration example

```python
{
  "mcpServers": {
    "sendgrid-mcp": {
      "command": "/path/to/your/project/venv/Scripts/python.exe",
      "args": ["/path/to/your/project/main.py"],
      "cwd": "/path/to/your/project",
      "disabled": false,
      "env": {
        "SENDGRID_API_KEY": "SG.your-actual-api-key-here"
      }
    }
  }
}
```
For Windows users, use paths like:

```json
"command": "C:\\Users\\YourUsername\\project-folder\\venv\\Scripts\\python.exe"
"args": ["C:\\Users\\YourUsername\\project-folder\\main.py"]  
"cwd": "C:\\Users\\YourUsername\\project-folder"
```
For macOS/Linux users, use paths like:

```json
"command": "/Users/yourusername/project-folder/venv/bin/python"
"args": ["/Users/yourusername/project-folder/main.py"]
"cwd": "/Users/yourusername/project-folder"
```
Key configuration elements:

- "sendgrid-mcp": The server name/identifier (customizable)

- command: Points to your virtual environment's Python executable

- args: Specifies the path to your main.py file

- cwd: Sets the working directory to your project folder

- disabled: Set to false to enable the server

- env: Contains your SendGrid API key (replace with your actual key starting with "SG.")

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
