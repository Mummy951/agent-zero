# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Agent Zero is a personal, organic agentic framework that grows and learns with you. It's designed to be dynamic, organically growing, and learning as you use it. The framework uses the computer as a tool to accomplish tasks and is fully transparent, readable, comprehensible, customizable, and interactive.

## Key Architecture Components

### Core Structure
- `agent.py` - Main agent implementation
- `models.py` - Model configuration and LLM integration
- `initialize.py` - Framework initialization
- `run_ui.py` - Main entry point for web UI and API
- `run_cli.py` - CLI interface (deprecated)

### Key Directories
- `/python` - Core Python codebase
  - `/api` - API endpoints
  - `/extensions` - Modular extensions
  - `/helpers` - Utility functions
  - `/tools` - Built-in tools
- `/prompts` - System and tool prompts
- `/memory` - Persistent agent memory
- `/knowledge` - Knowledge base
- `/instruments` - Custom scripts and tools
- `/docs` - Documentation

## Development Environment

### Prerequisites
1. Docker Desktop (primary runtime environment)
2. Python 3.10+ for local development
3. API keys for LLM providers (OpenAI, Anthropic, etc.)

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp example.env .env
# Edit .env with your API keys
```

## Common Commands

### Running the Application
```bash
# Primary way to run (includes both UI and API)
python run_ui.py

# Access at http://localhost:50001
```

### Docker Runtime (Recommended)
```bash
# Pull the image
docker pull agent0ai/agent-zero

# Run with data persistence
docker run -p 50001:80 -v ./data:/a0 agent0ai/agent-zero
```

## Testing
Tests are located in the `tests/` directory, primarily focused on MCP functionality.

## Key Features to Understand

1. **Hierarchical Agent Structure** - Agents can create subordinates for task delegation
2. **Tool System** - Extensible tools in `python/tools/` with prompt definitions in `prompts/`
3. **Memory System** - Persistent storage in `/memory` with automatic and manual management
4. **Prompt Architecture** - Modular prompts in `prompts/default/` that can be customized
5. **MCP Integration** - Model Context Protocol support for external tool integration
6. **Instruments** - Custom scripts in `/instruments` that don't affect token count
7. **Extensions** - Modular system in `python/extensions/` for extending functionality

## Customization Points

1. **Prompts** - Modify files in `prompts/default/` or create custom prompt sets
2. **Tools** - Add new tools in `python/tools/` following existing patterns
3. **Instruments** - Add scripts in `instruments/custom/`
4. **Extensions** - Add Python files to appropriate subdirectories in `python/extensions/`