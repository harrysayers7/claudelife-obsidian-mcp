# Claudelife Obsidian MCP Server

A FastMCP Cloud server providing full CRUD capabilities for Obsidian vaults. Built specifically for the claudelife vault using filesystem-based operations suitable for cloud deployment.

## Features

- **13 MCP Tools** for comprehensive vault operations
- **Full CRUD**: Create, Read, Update, Delete markdown files
- **Filesystem-based**: Works directly with vault files (no Obsidian REST API dependency)
- **Cloud-deployable**: Built with FastMCP framework for cloud hosting
- **PARA-aware**: Respects the PARA organizational structure
- **Frontmatter support**: Auto-generates and preserves YAML frontmatter

## Tools Overview

### Read Tools (8)

1. **list_vault_files** - List all markdown files in vault root
2. **list_directory_files** - List files in specific directory
3. **get_file_content** - Read single file content
4. **batch_get_files** - Read multiple files at once
5. **search_vault** - Full-text search across vault
6. **get_recent_files** - Get recently modified files
7. **get_daily_note** - Get or check today's daily note
8. **search_by_tag** - Find files by tag

### Write Tools (4)

9. **create_file** - Create new markdown file with auto-frontmatter
10. **update_file** - Replace entire file content
11. **append_to_file** - Append content to file end
12. **patch_file** - Insert content at specific heading

### Delete Tools (1)

13. **delete_file** - Delete file (requires confirmation)

## Installation

### Prerequisites

- Python 3.11+
- FastMCP CLI: `npm install -g fastmcp`

### Local Development

```bash
# Clone repository
git clone https://github.com/sayersauce/claudelife-obsidian-mcp.git
cd claudelife-obsidian-mcp

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set VAULT_PATH=/path/to/your/vault

# Test server locally
python server.py
```

## Deployment to FastMCP Cloud

### Step 1: Prepare Repository

```bash
# Ensure code is committed
git add .
git commit -m "Ready for FastMCP Cloud deployment"
git push origin main
```

### Step 2: Deploy with FastMCP CLI

```bash
# Login to FastMCP Cloud
fastmcp login

# Deploy server
fastmcp deploy server.py \
  --name claudelife-obsidian \
  --env VAULT_PATH=/Users/harrysayers/Developer/claudelife

# Server will be deployed and you'll receive a URL
# Example: https://api.fastmcp.cloud/servers/abc123/sse
```

### Step 3: Configure Claude Code

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "claudelife-obsidian": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "YOUR_DEPLOYED_URL_FROM_STEP_2"
      ]
    }
  }
}
```

Add to `.claude/settings.local.json`:

```json
{
  "enabledMcpjsonServers": [
    "claudelife-obsidian"
  ]
}
```

Restart Claude Code for changes to take effect.

## Usage Examples

### Read Operations

```python
# List all files in vault root
list_vault_files_tool()
# Returns: {"success": true, "files": ["CLAUDE.md", "README.md"], "count": 2}

# Get file content
get_file_content_tool("CLAUDE.md")
# Returns: {"success": true, "content": "...", "size": 1234}

# Search vault
search_vault_tool("automation", case_sensitive=False)
# Returns: {"success": true, "matches": [...], "file_count": 5}

# Get recent files
get_recent_files_tool(limit=10, days=7)
# Returns: {"success": true, "files": [...], "count": 10}

# Get today's daily note
get_daily_note_tool()
# Returns: {"success": true, "date": "2025-10-08", "file_path": "00-inbox/01-today/25-10-08 - Wed.md"}

# Search by tag
search_by_tag_tool("mokai")
# Returns: {"success": true, "matches": [...], "count": 15}
```

### Write Operations

```python
# Create new file
create_file_tool(
    file_path="00-inbox/new-note.md",
    content="# My New Note\n\nContent here...",
    add_frontmatter=True
)
# Returns: {"success": true, "message": "File created: 00-inbox/new-note.md"}

# Update existing file
update_file_tool(
    file_path="00-inbox/existing.md",
    content="# Updated Content"
)

# Append to file
append_to_file_tool(
    file_path="00-inbox/log.md",
    content="## 2025-10-08\n\nNew entry..."
)

# Insert at heading
patch_file_tool(
    file_path="01-areas/business/mokai/mokai-profile.md",
    content="- New service offering",
    heading="Services",
    position="after"
)
```

### Delete Operations

```python
# Delete file (requires confirmation)
delete_file_tool(
    file_path="00-inbox/temp.md",
    confirm=True  # MUST be True to actually delete
)
```

## Tool Details

### Frontmatter Auto-Generation

When `add_frontmatter=True` (default for `create_file`), files are created with:

```markdown
---
date: "YYYY-MM-DD HH:MM"
---

[Your content here]
```

### Path Validation

All file paths are:
- Validated against vault root (prevents directory traversal)
- Relative to vault root (e.g., `"00-inbox/note.md"`)
- Automatically resolved to absolute paths internally

### Error Handling

All tools return consistent response format:

```python
{
    "success": bool,
    "error": str,  # Only present if success=False
    # Additional fields vary by tool
}
```

## PARA Structure

The server respects the PARA organizational structure:

- `00-inbox/` - Capture area
- `01-areas/` - Ongoing responsibilities
- `02-projects/` - Active projects
- `03-resources/` - Reference materials
- `04-archive/` - Completed items

## Security Features

1. **Path Validation**: All paths validated against vault root
2. **Delete Confirmation**: Requires explicit `confirm=True`
3. **Frontmatter Preservation**: Never corrupts file frontmatter
4. **Error Handling**: Graceful failures with descriptive messages
5. **Read-only by Default**: Write operations require explicit parameters

## Development

### Project Structure

```
claudelife-obsidian-mcp/
├── server.py              # FastMCP server entrypoint
├── tools/
│   ├── read_tools.py      # Read operations
│   ├── write_tools.py     # Create/update operations
│   └── delete_tools.py    # Delete operations
├── utils/
│   ├── vault.py           # Vault path management
│   ├── frontmatter.py     # Frontmatter utilities
│   └── markdown.py        # Markdown parsing
├── requirements.txt
├── .env.example
├── design.md             # Architecture documentation
└── README.md
```

### Testing Locally

```bash
# Set environment variable
export VAULT_PATH=/path/to/test/vault

# Run server
python server.py

# In another terminal, test with MCP inspector
npx @modelcontextprotocol/inspector python server.py
```

## Troubleshooting

### "VAULT_PATH environment variable not set"

Make sure `.env` file exists with:
```
VAULT_PATH=/Users/harrysayers/Developer/claudelife
```

### "Path resolves outside vault"

All file paths must be relative to vault root. Use `"00-inbox/note.md"` not `"/Users/.../00-inbox/note.md"`.

### "File already exists"

Use `update_file_tool()` instead of `create_file_tool()` to modify existing files.

### Delete not working

Delete requires explicit confirmation:
```python
delete_file_tool("path/to/file.md", confirm=True)
```

## Contributing

This is a personal project for claudelife vault management. If you want to adapt it for your vault:

1. Fork the repository
2. Update `VAULT_PATH` in `.env`
3. Modify daily note logic in `tools/read_tools.py` if your format differs
4. Deploy to your own FastMCP Cloud instance

## License

MIT License - See LICENSE file for details

## Author

Harrison Robert Sayers (@sayersauce)

Built with [FastMCP](https://github.com/jlowin/fastmcp) by Marvin/Prefect
