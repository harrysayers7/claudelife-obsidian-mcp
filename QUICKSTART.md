# Quick Start Guide

Get the claudelife Obsidian MCP server running in 5 minutes.

## For Local Use (Fastest)

### 1. Clone and Install

```bash
cd /Users/harrysayers/Developer
git clone https://github.com/harrysayers7/claudelife-obsidian-mcp.git
cd claudelife-obsidian-mcp
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env to set VAULT_PATH=/Users/harrysayers/Developer/claudelife
```

### 3. Add to Claude Code

Edit `/Users/harrysayers/Developer/claudelife/.mcp.json`:

```json
{
  "mcpServers": {
    "claudelife-obsidian": {
      "command": "python",
      "args": ["/Users/harrysayers/Developer/claudelife-obsidian-mcp/server.py"],
      "env": {
        "VAULT_PATH": "/Users/harrysayers/Developer/claudelife"
      }
    }
  }
}
```

### 4. Enable Server

Edit `/Users/harrysayers/Developer/claudelife/.claude/settings.local.json`:

```json
{
  "enabledMcpjsonServers": [
    "claudelife-obsidian"
  ]
}
```

### 5. Restart Claude Code

Restart Claude Code for changes to take effect.

### 6. Test

In Claude Code:

```
List files in my vault
```

## For Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for FastMCP Cloud deployment instructions.

## Troubleshooting

### "VAULT_PATH not set"
Check `.env` file exists and contains correct path.

### "Module not found"
Run: `pip install -r requirements.txt`

### "Tools not available"
1. Check server is in `enabledMcpjsonServers`
2. Restart Claude Code
3. Check for errors in Claude Code MCP logs

### "Permission denied"
Ensure vault directory has read/write permissions.

## Example Commands

Once configured, you can ask Claude:

- "Show me my recent files"
- "Search for 'automation' in my vault"
- "Create a new note in 00-inbox"
- "Get today's daily note"
- "Find all files tagged with 'mokai'"
- "Append a task to my TODO list"

## Available Tools

- **Read**: 8 tools for browsing and searching
- **Write**: 4 tools for creating and updating
- **Delete**: 1 tool (requires confirmation)

See [README.md](README.md) for complete tool documentation.

## Next Steps

1. ✅ Server configured locally
2. ⏭️ Deploy to FastMCP Cloud (see DEPLOYMENT.md)
3. ⏭️ Configure for remote access
4. ⏭️ Build automations using MCP tools

## Support

- Report issues: https://github.com/harrysayers7/claudelife-obsidian-mcp/issues
- FastMCP docs: https://github.com/jlowin/fastmcp
