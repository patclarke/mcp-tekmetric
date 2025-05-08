# MCP Tekmetric

A Model Context Protocol (MCP) server designed to integrate AI assistants with Tekmetric. This project allows AI tools to interact with your Tekmetric data, enabling automation and intelligent workflows directly from your AI assistant.

Currently, this integration supports **read-only actions**, allowing your AI to retrieve information from your Tekmetric instance.

## Example Usage

Leverage your AI assistant to interact with your Tekmetric data:

- **📅 Check Appointment Details:** "What are the details for the appointment scheduled for tomorrow?"
- **🚗 Retrieve Vehicle Information:** "Find the service history for license plate ABC-123."
- **📊 Get Repair Order Status:** "What is the current status of repair order #12345?"
- **📦 Look up Parts:** "Search for part number XYZ in inventory."

## Quick Start Guide

Follow these steps to get the MCP Tekmetric server up and running:

### 1. Authentication Setup

You need a Tekmetric API key to authenticate with the Tekmetric API. Obtain your API key from your Tekmetric account settings (provide link or navigation path if possible).

Set your API key as a system environment variable named `TEKMETRIC_API_KEY`:

```
export TEKMETRIC_API_KEY="your_tekmetric_api_key"
```

### 2. Installation

Clone this repository:

```
git clone https://github.com/patclarke/mcp-tekmetric.git
cd mcp-tekmetric
```

Install the required dependencies:

```
pip install -e .
```

### 3. Run the MCP Server

Start the Uvicorn server:

```
uvicorn mcp_tekmetric.servers.main:asgi_app --host 0.0.0.0 --port 8080
```

This will start the MCP server, making it available for your AI assistant to connect to, typically on `http://localhost:8080`.

### 4. Connect Your AI Assistant

(This section depends heavily on the AI assistant being used. Provide generic guidance or specific instructions for popular assistants if possible).

For VSCode my mcp.json looks like this:

```
{
  "servers": {
    "local-tekmetric": {
      "type": "sse",
      "url": "http://localhost:8080/sse"
    }
  }
}
```