"""FastMCP server for claudelife Obsidian vault operations."""
import os
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Import all tool functions
from tools.read_tools import (
    list_vault_files,
    list_directory_files,
    get_file_content,
    batch_get_files,
    search_vault,
    get_recent_files,
    get_daily_note,
    search_by_tag
)
from tools.write_tools import (
    create_file,
    update_file,
    append_to_file,
    patch_file
)
from tools.delete_tools import delete_file

# Initialize FastMCP server
mcp = FastMCP("claudelife-obsidian")


# ============================================================================
# READ TOOLS
# ============================================================================

@mcp.tool()
def list_vault_files_tool() -> dict:
    """
    List all markdown files in the vault root directory.

    Returns dict with:
    - success: bool
    - files: list[str] (file paths)
    - count: int
    """
    return list_vault_files()


@mcp.tool()
def list_directory_files_tool(directory_path: str) -> dict:
    """
    List markdown files in a specific directory.

    Args:
        directory_path: Relative path from vault root (e.g., "00-inbox/01-today")

    Returns dict with:
    - success: bool
    - directory: str
    - files: list[str]
    - count: int
    """
    return list_directory_files(directory_path)


@mcp.tool()
def get_file_content_tool(file_path: str) -> dict:
    """
    Read the content of a single markdown file.

    Args:
        file_path: Relative path from vault root (e.g., "CLAUDE.md")

    Returns dict with:
    - success: bool
    - file_path: str
    - content: str
    - size: int
    """
    return get_file_content(file_path)


@mcp.tool()
def batch_get_files_tool(file_paths: list[str]) -> dict:
    """
    Read multiple markdown files at once.

    Args:
        file_paths: List of relative paths from vault root

    Returns dict with:
    - success: bool
    - files: dict[str, str] (path -> content)
    - count: int
    - successful: int
    """
    return batch_get_files(file_paths)


@mcp.tool()
def search_vault_tool(query: str, case_sensitive: bool = False) -> dict:
    """
    Search for text across all markdown files in the vault.

    Args:
        query: Search term
        case_sensitive: If True, perform case-sensitive search

    Returns dict with:
    - success: bool
    - query: str
    - matches: list[dict] (file_path, match_count, matches)
    - file_count: int
    """
    return search_vault(query, case_sensitive)


@mcp.tool()
def get_recent_files_tool(limit: int = 10, days: int = 7) -> dict:
    """
    Get recently modified markdown files.

    Args:
        limit: Maximum number of files to return (default: 10)
        days: Look back period in days (default: 7)

    Returns dict with:
    - success: bool
    - files: list[dict] (file_path, modified, size)
    - count: int
    - days: int
    - total_matching: int
    """
    return get_recent_files(limit, days)


@mcp.tool()
def get_daily_note_tool(date: str = None) -> dict:
    """
    Get today's daily note (or specific date).

    Args:
        date: Date in YYYY-MM-DD format (defaults to today)

    Returns dict with:
    - success: bool
    - date: str
    - file_path: str
    - content: str (if exists)
    - exists: bool
    """
    return get_daily_note(date)


@mcp.tool()
def search_by_tag_tool(tag: str) -> dict:
    """
    Find files containing a specific tag.

    Args:
        tag: Tag to search for (without # symbol)

    Returns dict with:
    - success: bool
    - tag: str
    - matches: list[dict] (file_path, tags)
    - count: int
    """
    return search_by_tag(tag)


# ============================================================================
# WRITE TOOLS
# ============================================================================

@mcp.tool()
def create_file_tool(
    file_path: str,
    content: str,
    add_frontmatter: bool = True
) -> dict:
    """
    Create a new markdown file.

    Args:
        file_path: Relative path from vault root (e.g., "00-inbox/new-note.md")
        content: File content
        add_frontmatter: If True, auto-add date frontmatter (default: True)

    Returns dict with:
    - success: bool
    - file_path: str
    - message: str
    - size: int
    """
    return create_file(file_path, content, add_frontmatter)


@mcp.tool()
def update_file_tool(file_path: str, content: str) -> dict:
    """
    Replace entire file content (preserves frontmatter if not in new content).

    Args:
        file_path: Relative path from vault root
        content: New content

    Returns dict with:
    - success: bool
    - file_path: str
    - message: str
    - size: int
    """
    return update_file(file_path, content)


@mcp.tool()
def append_to_file_tool(file_path: str, content: str) -> dict:
    """
    Append content to the end of a file.

    Args:
        file_path: Relative path from vault root
        content: Content to append

    Returns dict with:
    - success: bool
    - file_path: str
    - message: str
    - size: int
    """
    return append_to_file(file_path, content)


@mcp.tool()
def patch_file_tool(
    file_path: str,
    content: str,
    heading: str,
    position: str = "after"
) -> dict:
    """
    Insert content at a specific location relative to a heading.

    Args:
        file_path: Relative path from vault root
        content: Content to insert
        heading: Target heading (without # symbols)
        position: "before" or "after" the heading (default: "after")

    Returns dict with:
    - success: bool
    - file_path: str
    - message: str
    - size: int
    """
    return patch_file(file_path, content, heading, position)


# ============================================================================
# DELETE TOOLS
# ============================================================================

@mcp.tool()
def delete_file_tool(file_path: str, confirm: bool = False) -> dict:
    """
    Delete a markdown file from the vault.

    CAUTION: This permanently deletes files. Use with care.

    Args:
        file_path: Relative path from vault root
        confirm: Safety confirmation (MUST be True to delete)

    Returns dict with:
    - success: bool
    - file_path: str
    - message: str
    """
    return delete_file(file_path, confirm)


# ============================================================================
# SERVER INFO
# ============================================================================

@mcp.resource("vault://info")
def get_vault_info() -> str:
    """Get information about the configured vault."""
    vault_path = os.getenv("VAULT_PATH", "Not configured")
    return f"""Claudelife Obsidian Vault MCP Server

Vault Path: {vault_path}

Available Tools:
- Read: list_vault_files, list_directory_files, get_file_content, batch_get_files, search_vault, get_recent_files, get_daily_note, search_by_tag
- Write: create_file, update_file, append_to_file, patch_file
- Delete: delete_file (requires confirm=True)

Total Tools: 13
"""


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()
