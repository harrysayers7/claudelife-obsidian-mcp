# Deployment Guide

## FastMCP Cloud Deployment

⚠️ **Important**: FastMCP Cloud deployment is currently done through their web interface at https://fastmcp.cloud, not via CLI.

### Prerequisites

1. ✅ GitHub repository: https://github.com/harrysayers7/claudelife-obsidian-mcp
2. FastMCP Cloud account (sign up at https://fastmcp.cloud)
3. Python 3.11+ runtime

### Deployment Steps

#### Option A: Web Interface (Recommended)

1. **Sign up/Login** to https://fastmcp.cloud
2. **Create New Server**:
   - Click "New Server" or "Deploy"
   - Connect your GitHub account if needed
   - Select repository: `harrysayers7/claudelife-obsidian-mcp`
   - Branch: `main`
   - Entry point: `server.py`
3. **Configure Environment**:
   - Add environment variable: `VAULT_PATH=/Users/harrysayers/Developer/claudelife`
   - Select Python version: 3.11
4. **Deploy**: Click "Deploy" button
5. **Get URL**: Copy the server URL provided (format: `https://api.fastmcp.cloud/servers/YOUR_ID/sse`)

#### Option B: CLI Deployment (When Available)

If FastMCP CLI supports deployment in future:

```bash
npm install -g fastmcp
fastmcp login
fastmcp deploy server.py \
  --name claudelife-obsidian \
  --env VAULT_PATH=/Users/harrysayers/Developer/claudelife
```

Save the deployment URL for configuration.

### Step 5: Configure Claude Code

#### Add to .mcp.json

In your claudelife project, add to `.mcp.json`:

```json
{
  "mcpServers": {
    "claudelife-obsidian": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "YOUR_FASTMCP_CLOUD_URL_FROM_STEP_4"
      ]
    }
  }
}
```

#### Enable in settings

Add to `.claude/settings.local.json`:

```json
{
  "enabledMcpjsonServers": [
    "claudelife-obsidian"
  ]
}
```

### Step 6: Restart Claude Code

Restart Claude Code to load the new MCP server.

### Step 7: Test Connection

In Claude Code, try:

```
List files in my vault
```

Claude should now be able to use the MCP tools to interact with your vault.

## Alternative: Local MCP Server (Development)

For local development without FastMCP Cloud:

### Step 1: Install Dependencies

```bash
cd /Users/harrysayers/Developer/claudelife-obsidian-mcp
pip install -r requirements.txt
```

### Step 2: Configure for Local Use

In `.mcp.json`:

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

### Step 3: Enable and Restart

Add to `enabledMcpjsonServers` in `.claude/settings.local.json` and restart Claude Code.

## Troubleshooting

### Deployment Fails

Check:
- Python version is 3.11+
- All dependencies in requirements.txt are compatible
- Environment variables are set correctly

### MCP Connection Fails

Check:
- Server URL is correct in `.mcp.json`
- Server is listed in `enabledMcpjsonServers`
- Claude Code was restarted after configuration

### Tools Not Working

Check:
- VAULT_PATH environment variable is set correctly
- Path points to actual vault directory
- Vault directory is accessible from server location

### Read/Write Errors

Check:
- File paths are relative to vault root (not absolute)
- Vault directory has proper permissions
- Files are valid markdown (.md extension)

## Monitoring

FastMCP Cloud provides monitoring dashboard at https://fastmcp.cloud/dashboard

Monitor:
- Request counts
- Error rates
- Response times
- Tool usage patterns

## Updating

To update the deployed server:

```bash
# Make code changes
git add .
git commit -m "Update: description"
git push

# Redeploy
fastmcp deploy server.py \
  --name claudelife-obsidian \
  --env VAULT_PATH=/Users/harrysayers/Developer/claudelife
```

## Security Notes

- VAULT_PATH is set as environment variable (not in code)
- Server validates all file paths against vault root
- Delete operations require explicit confirmation
- Consider restricting server access via FastMCP Cloud settings

## Support

- FastMCP Documentation: https://github.com/jlowin/fastmcp
- FastMCP Cloud: https://fastmcp.cloud
- Issues: https://github.com/harrysayers7/claudelife-obsidian-mcp/issues
