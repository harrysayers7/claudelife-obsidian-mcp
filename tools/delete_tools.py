"""Delete operations for Obsidian vault."""
import os
from utils.vault import validate_relative_path, VaultPathError


def delete_file(file_path: str, confirm: bool = False) -> dict:
    """
    Delete a markdown file from the vault.

    Args:
        file_path: Relative path from vault root
        confirm: Safety confirmation (must be True to delete)

    Returns:
        Dict with success status
    """
    try:
        if not confirm:
            return {
                "success": False,
                "error": "Delete operation requires explicit confirmation. Set confirm=True to proceed."
            }

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

        # Delete file
        os.remove(full_path)

        return {
            "success": True,
            "file_path": file_path,
            "message": f"File deleted: {file_path}"
        }
    except VaultPathError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Error deleting file: {str(e)}"}
