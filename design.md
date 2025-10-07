# Claudelife Obsidian MCP - FastMCP Cloud Design

## Architecture

This is a FastMCP Cloud implementation of an Obsidian MCP server that provides full CRUD capabilities for the claudelife vault located at `/Users/harrysayers/Developer/claudelife`.

**Key Difference from Original**: Uses direct filesystem operations instead of Obsidian Local REST API plugin, making it suitable for cloud deployment.

## Tools Design (13 total)

### 1. list_vault_files
**Purpose**: List all markdown files in vault root
**Parameters**: None
**Returns**: List of file paths
**Implementation**: `os.listdir()` + filter for `.md` files

### 2. list_directory_files
**Purpose**: List files in specific directory
**Parameters**:
- `directory_path: str` - Relative path from vault root
**Returns**: List of file paths with metadata
**Implementation**: `os.listdir()` on directory path

### 3. get_file_content
**Purpose**: Read single file content
**Parameters**:
- `file_path: str` - Relative path from vault root
**Returns**: File content as string with frontmatter
**Implementation**: Read file, preserve frontmatter

### 4. batch_get_files
**Purpose**: Read multiple files at once
**Parameters**:
- `file_paths: list[str]` - List of relative paths
**Returns**: Dict mapping paths to content
**Implementation**: Loop through paths, read each file

### 5. search_vault
**Purpose**: Simple text search across all markdown files
**Parameters**:
- `query: str` - Search term
- `case_sensitive: bool = False`
**Returns**: List of matching files with context
**Implementation**: Walk vault directory, search file contents

### 6. create_file
**Purpose**: Create new markdown file
**Parameters**:
- `file_path: str` - Relative path from vault root
- `content: str` - File content
- `add_frontmatter: bool = True` - Auto-add date frontmatter
**Returns**: Success message
**Implementation**: Create file with frontmatter template

### 7. update_file
**Purpose**: Replace entire file content
**Parameters**:
- `file_path: str` - Relative path from vault root
- `content: str` - New content
**Returns**: Success message
**Implementation**: Write new content, preserve frontmatter if exists

### 8. append_to_file
**Purpose**: Append content to end of file
**Parameters**:
- `file_path: str` - Relative path from vault root
- `content: str` - Content to append
**Returns**: Success message
**Implementation**: Read existing, append new content

### 9. patch_file
**Purpose**: Insert content at specific location (heading/block)
**Parameters**:
- `file_path: str` - Relative path from vault root
- `content: str` - Content to insert
- `heading: str | None` - Target heading
- `position: str = "after"` - "before" or "after"
**Returns**: Success message
**Implementation**: Parse markdown, find heading, insert content

### 10. delete_file
**Purpose**: Delete markdown file
**Parameters**:
- `file_path: str` - Relative path from vault root
- `confirm: bool = False` - Safety confirmation
**Returns**: Success message
**Implementation**: `os.remove()` with confirmation check

### 11. get_recent_files
**Purpose**: Get recently modified files
**Parameters**:
- `limit: int = 10` - Number of files to return
- `days: int = 7` - Look back period
**Returns**: List of files sorted by modification time
**Implementation**: Walk vault, sort by `os.path.getmtime()`

### 12. get_daily_note
**Purpose**: Get or create today's daily note
**Parameters**:
- `date: str | None` - Date in YYYY-MM-DD format (defaults to today)
**Returns**: File path and content
**Implementation**: Check for file in `00-inbox/01-today/`, create if missing

### 13. search_by_tag
**Purpose**: Find files containing specific tags
**Parameters**:
- `tag: str` - Tag to search for (without #)
**Returns**: List of files containing the tag
**Implementation**: Search file contents for `#tag` or frontmatter tags

## File Structure

```
claudelife-obsidian-mcp/
├── server.py              # FastMCP server entrypoint
├── tools/
│   ├── __init__.py
│   ├── read_tools.py      # Tools 1-5, 11-13 (read operations)
│   ├── write_tools.py     # Tools 6-9 (create/update)
│   └── delete_tools.py    # Tool 10 (delete)
├── utils/
│   ├── __init__.py
│   ├── vault.py           # Vault path management
│   ├── frontmatter.py     # Frontmatter parsing/generation
│   └── markdown.py        # Markdown parsing utilities
├── .env.example
├── README.md
└── requirements.txt
```

## Environment Variables

```
VAULT_PATH=/Users/harrysayers/Developer/claudelife
```

## Deployment Flow

1. Create GitHub repository: `sayersauce/claudelife-obsidian-mcp`
2. Implement FastMCP server with all 13 tools
3. Deploy to FastMCP Cloud via agent guide workflow
4. Configure in Claude Code `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "claudelife-obsidian": {
         "command": "npx",
         "args": ["-y", "mcp-remote", "DEPLOYED_URL_FROM_FASTMCP_CLOUD"]
       }
     }
   }
   ```

## PARA Method Integration

Tools respect the PARA structure in claudelife:
- `00-inbox/` - Capture area
- `01-areas/` - Ongoing responsibilities
- `02-projects/` - Active projects
- `03-resources/` - Reference materials
- `04-archive/` - Completed items

## Safety Features

1. **Path validation**: All file paths validated against vault root
2. **Delete confirmation**: Requires explicit `confirm=True` parameter
3. **Frontmatter preservation**: Never corrupt file frontmatter
4. **Error handling**: Graceful failures with descriptive messages
5. **Read-only by default**: Write operations require explicit parameters

## Next Steps

1. Implement server.py with FastMCP framework
2. Implement all 13 tools across read/write/delete modules
3. Add comprehensive error handling
4. Create README with usage examples
5. Deploy to FastMCP Cloud
6. Configure Claude Code integration
