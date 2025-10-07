"""Write/update tools for Obsidian vault operations."""
from utils.vault import (
    get_vault_path,
    validate_relative_path,
    ensure_parent_dir,
    VaultPathError
)
from utils.frontmatter import generate_frontmatter, ensure_frontmatter
from utils.markdown import insert_content_at_heading


def create_file(
    file_path: str,
    content: str,
    add_frontmatter: bool = True
) -> dict:
    """
    Create a new markdown file.

    Args:
        file_path: Relative path from vault root
        content: File content
        add_frontmatter: If True, auto-add date frontmatter

    Returns:
        Dict with success status
    """
    try:
        full_path = validate_relative_path(file_path)

        # Check if file already exists
        if full_path.exists():
            return {
                "success": False,
                "error": f"File already exists: {file_path}. Use update_file to modify."
            }

        # Ensure parent directory exists
        ensure_parent_dir(full_path)

        # Add frontmatter if requested
        if add_frontmatter and not content.startswith('---'):
            content = generate_frontmatter() + content

        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "success": True,
            "file_path": file_path,
            "message": f"File created: {file_path}",
            "size": len(content)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Error creating file: {str(e)}"}


def update_file(file_path: str, content: str) -> dict:
    """
    Replace entire file content.

    Args:
        file_path: Relative path from vault root
        content: New content

    Returns:
        Dict with success status
    """
    try:
        full_path = validate_relative_path(file_path)

        if not full_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}. Use create_file to create new files."
            }

        # Preserve frontmatter if content doesn't have it
        if not content.startswith('---'):
            # Read existing content to check for frontmatter
            with open(full_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()

            if existing_content.startswith('---'):
                # Preserve existing frontmatter
                from utils.frontmatter import parse_frontmatter
                frontmatter, _ = parse_frontmatter(existing_content)

                # Rebuild with existing frontmatter
                fm_lines = ["---"]
                for k, v in frontmatter.items():
                    if ' ' in str(v) or ':' in str(v):
                        fm_lines.append(f'{k}: "{v}"')
                    else:
                        fm_lines.append(f'{k}: {v}')
                fm_lines.append("---")
                fm_lines.append("")

                content = '\n'.join(fm_lines) + content

        # Write updated content
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "success": True,
            "file_path": file_path,
            "message": f"File updated: {file_path}",
            "size": len(content)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Error updating file: {str(e)}"}


def append_to_file(file_path: str, content: str) -> dict:
    """
    Append content to the end of a file.

    Args:
        file_path: Relative path from vault root
        content: Content to append

    Returns:
        Dict with success status
    """
    try:
        full_path = validate_relative_path(file_path)

        if not full_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }

        # Read existing content
        with open(full_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

        # Append new content
        updated_content = existing_content.rstrip('\n') + '\n\n' + content

        # Write back
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return {
            "success": True,
            "file_path": file_path,
            "message": f"Content appended to: {file_path}",
            "size": len(updated_content)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Error appending to file: {str(e)}"}


def patch_file(
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
        position: "before" or "after" the heading

    Returns:
        Dict with success status
    """
    try:
        full_path = validate_relative_path(file_path)

        if not full_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }

        # Read existing content
        with open(full_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

        # Insert content at heading
        try:
            updated_content = insert_content_at_heading(
                existing_content,
                heading,
                content,
                position
            )
        except ValueError as e:
            return {"success": False, "error": str(e)}

        # Write back
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return {
            "success": True,
            "file_path": file_path,
            "message": f"Content inserted {position} heading '{heading}' in {file_path}",
            "size": len(updated_content)
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Error patching file: {str(e)}"}
