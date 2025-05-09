# MCP Tekmetric

A Model Context Protocol (MCP) server designed to integrate AI assistants with Tekmetric. This project allows AI tools to interact with your Tekmetric data, enabling automation and intelligent workflows directly from your AI assistant.

Currently, this integration supports **read-only actions**, allowing your AI to retrieve information from your Tekmetric instance.

## Example Usage

Leverage your AI assistant to interact with your Tekmetric data:

- **📅 Check Appointment Details:** "What are the details for the appointment scheduled for tomorrow?"
- **🚗 Retrieve Shop Information:** "Find the contact information of a Shop."
- **📊 Get Repair Order Status:** "What is the current status of repair order #12345?"

![image](https://github.com/user-attachments/assets/b1140b51-0d0e-46e8-b77a-b4a687780555)

---

## 🔐 Authentication Setup

You need a Tekmetric API key to authenticate with the Tekmetric API. Obtain your API key from your Tekmetric account settings.

Set your API key as a system environment variable:

```bash
export TEKMETRIC_API_KEY="your_tekmetric_api_key"
```

---

## 🚀 Quick Start Guide

### Option 1: Run Locally (Python)

1. **Clone this repository**:

    ```bash
    git clone https://github.com/patclarke/mcp-tekmetric.git
    cd mcp-tekmetric
    ```

2. **Install dependencies**:

    ```bash
    pip install -e .
    ```

3. **Start the server**:

    ```bash
    uvicorn mcp_tekmetric.servers.main:asgi_app --host 0.0.0.0 --port 8080
    ```

---

### Option 2: Run with Docker

1. **Clone this repository**:

    ```bash
    git clone https://github.com/patclarke/mcp-tekmetric.git
    cd mcp-tekmetric
    ```

2. **Build the Docker image**:

    ```bash
    docker build -t mcp-tekmetric .
    ```

3. **Run the container** (pass your Tekmetric API key):

    ```bash
    docker run -e TEKMETRIC_API_KEY=your_tekmetric_api_key -p 8080:8080 mcp-tekmetric
    ```

This will expose the server on `http://localhost:8080`.

---

## 🤖 Connect Your AI Assistant

For VS Code Copilot or another AI assistant that supports MCP:

Example `.mcp.json` config:

```json
{
  "servers": {
    "local-tekmetric": {
      "type": "sse",
      "url": "http://localhost:8080/sse"
    }
  }
}
```

---

## 🧪 Health Check

To verify the server is running:

```bash
curl http://localhost:8080/healthz
```

You should see:

```json
{"status": "ok"}
```

---

## 📄 License

MIT License
