"""Read-only tools for Obsidian vault operations."""
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from utils.vault import (
    get_vault_path,
    validate_relative_path,
    list_markdown_files,
    VaultPathError
)
from utils.markdown import extract_tags


def list_vault_files() -> dict:
    """
    List all markdown files in vault root directory.

    Returns:
        Dict with list of file paths
    """
    try:
        files = list_markdown_files(recursive=False)
        return {
            "success": True,
            "files": files,
            "count": len(files)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}


def list_directory_files(directory_path: str) -> dict:
    """
    List files in a specific directory within the vault.

    Args:
        directory_path: Relative path from vault root

    Returns:
        Dict with list of files and metadata
    """
    try:
        full_path = validate_relative_path(directory_path)

        if not full_path.exists():
            return {
                "success": False,
                "error": f"Directory not found: {directory_path}"
            }

        if not full_path.is_dir():
            return {
                "success": False,
                "error": f"Path is not a directory: {directory_path}"
            }

        files = list_markdown_files(directory=full_path, recursive=False)

        return {
            "success": True,
            "directory": directory_path,
            "files": files,
            "count": len(files)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}


def get_file_content(file_path: str) -> dict:
    """
    Read the content of a single markdown file.

    Args:
        file_path: Relative path from vault root

    Returns:
        Dict with file content
    """
    try:
        full_path = validate_relative_path(file_path)

        if not full_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }

        if not full_path.is_file():
            return {
                "success": False,
                "error": f"Path is not a file: {file_path}"
            }

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "success": True,
            "file_path": file_path,
            "content": content,
            "size": len(content)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Error reading file: {str(e)}"}


def batch_get_files(file_paths: list[str]) -> dict:
    """
    Read multiple markdown files at once.

    Args:
        file_paths: List of relative paths from vault root

    Returns:
        Dict mapping file paths to content
    """
    results = {}

    for file_path in file_paths:
        result = get_file_content(file_path)
        if result["success"]:
            results[file_path] = result["content"]
        else:
            results[file_path] = {"error": result.get("error")}

    return {
        "success": True,
        "files": results,
        "count": len(file_paths),
        "successful": sum(1 for v in results.values() if not isinstance(v, dict))
    }


def search_vault(query: str, case_sensitive: bool = False) -> dict:
    """
    Search for text across all markdown files in the vault.

    Args:
        query: Search term
        case_sensitive: If True, perform case-sensitive search

    Returns:
        Dict with matching files and context
    """
    try:
        vault_path = get_vault_path()
        matches = []

        # Get all markdown files recursively
        all_files = list_markdown_files(recursive=True)

        for file_path in all_files:
            full_path = vault_path / file_path

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Perform search
                search_content = content if case_sensitive else content.lower()
                search_query = query if case_sensitive else query.lower()

                if search_query in search_content:
                    # Find line with match
                    lines = content.split('\n')
                    matching_lines = []

                    for i, line in enumerate(lines):
                        check_line = line if case_sensitive else line.lower()
                        if search_query in check_line:
                            # Include context (line before and after)
                            context_start = max(0, i - 1)
                            context_end = min(len(lines), i + 2)
                            context = '\n'.join(lines[context_start:context_end])
                            matching_lines.append({
                                "line_number": i + 1,
                                "line": line,
                                "context": context
                            })

                    matches.append({
                        "file_path": file_path,
                        "match_count": len(matching_lines),
                        "matches": matching_lines[:5]  # Limit to first 5 matches per file
                    })

            except Exception as e:
                continue  # Skip files that can't be read

        return {
            "success": True,
            "query": query,
            "case_sensitive": case_sensitive,
            "matches": matches,
            "file_count": len(matches)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}


def get_recent_files(limit: int = 10, days: int = 7) -> dict:
    """
    Get recently modified markdown files.

    Args:
        limit: Maximum number of files to return
        days: Look back period in days

    Returns:
        Dict with recently modified files
    """
    try:
        vault_path = get_vault_path()
        cutoff_time = datetime.now() - timedelta(days=days)

        recent_files = []
        all_files = list_markdown_files(recursive=True)

        for file_path in all_files:
            full_path = vault_path / file_path

            try:
                mtime = datetime.fromtimestamp(full_path.stat().st_mtime)

                if mtime >= cutoff_time:
                    recent_files.append({
                        "file_path": file_path,
                        "modified": mtime.isoformat(),
                        "size": full_path.stat().st_size
                    })
            except Exception:
                continue

        # Sort by modification time (newest first)
        recent_files.sort(key=lambda x: x["modified"], reverse=True)

        return {
            "success": True,
            "files": recent_files[:limit],
            "count": len(recent_files[:limit]),
            "days": days,
            "total_matching": len(recent_files)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}


def get_daily_note(date: Optional[str] = None) -> dict:
    """
    Get today's daily note (or specific date).

    Args:
        date: Date in YYYY-MM-DD format (defaults to today)

    Returns:
        Dict with daily note path and content
    """
    try:
        if date:
            note_date = datetime.strptime(date, "%Y-%m-%d")
        else:
            note_date = datetime.now()

        # Format: YY-MM-DD - Day.md
        filename = note_date.strftime("%y-%m-%d") + " - " + note_date.strftime("%a") + ".md"
        file_path = f"00-inbox/01-today/{filename}"

        result = get_file_content(file_path)

        if result["success"]:
            return {
                "success": True,
                "date": note_date.strftime("%Y-%m-%d"),
                "file_path": file_path,
                "content": result["content"]
            }
        else:
            # Daily note doesn't exist yet
            return {
                "success": True,
                "date": note_date.strftime("%Y-%m-%d"),
                "file_path": file_path,
                "exists": False,
                "message": "Daily note not created yet"
            }
    except ValueError as e:
        return {"success": False, "error": f"Invalid date format: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_by_tag(tag: str) -> dict:
    """
    Find files containing a specific tag.

    Args:
        tag: Tag to search for (without # symbol)

    Returns:
        Dict with files containing the tag
    """
    try:
        vault_path = get_vault_path()
        tag_clean = tag.lstrip('#')
        matching_files = []

        all_files = list_markdown_files(recursive=True)

        for file_path in all_files:
            full_path = vault_path / file_path

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                tags = extract_tags(content)

                if tag_clean in tags:
                    matching_files.append({
                        "file_path": file_path,
                        "tags": tags
                    })
            except Exception:
                continue

        return {
            "success": True,
            "tag": tag_clean,
            "matches": matching_files,
            "count": len(matching_files)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}
