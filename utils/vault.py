"""Vault path management and validation."""
import os
from pathlib import Path
from typing import Optional


class VaultPathError(Exception):
    """Raised when vault path operations fail."""
    pass


def get_vault_path() -> Path:
    """Get the configured vault path from environment."""
    vault_path_str = os.getenv("VAULT_PATH")
    if not vault_path_str:
        raise VaultPathError("VAULT_PATH environment variable not set")

    vault_path = Path(vault_path_str).expanduser().resolve()

    if not vault_path.exists():
        raise VaultPathError(f"Vault path does not exist: {vault_path}")

    if not vault_path.is_dir():
        raise VaultPathError(f"Vault path is not a directory: {vault_path}")

    return vault_path


def validate_relative_path(relative_path: str) -> Path:
    """
    Validate and resolve a relative path within the vault.

    Args:
        relative_path: Path relative to vault root

    Returns:
        Absolute path within vault

    Raises:
        VaultPathError: If path is invalid or outside vault
    """
    vault_path = get_vault_path()

    # Normalize the relative path
    relative_path = relative_path.strip().lstrip("/")

    # Resolve to absolute path
    full_path = (vault_path / relative_path).resolve()

    # Ensure path is within vault (prevent directory traversal)
    try:
        full_path.relative_to(vault_path)
    except ValueError:
        raise VaultPathError(
            f"Path '{relative_path}' resolves outside vault: {full_path}"
        )

    return full_path


def ensure_parent_dir(file_path: Path) -> None:
    """Ensure parent directory exists for file path."""
    file_path.parent.mkdir(parents=True, exist_ok=True)


def list_markdown_files(directory: Optional[Path] = None, recursive: bool = False) -> list[str]:
    """
    List markdown files in directory.

    Args:
        directory: Directory to list (defaults to vault root)
        recursive: If True, list recursively

    Returns:
        List of file paths relative to vault root
    """
    vault_path = get_vault_path()
    search_path = directory or vault_path

    if not search_path.exists():
        return []

    markdown_files = []

    if recursive:
        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith('.md'):
                    full_path = Path(root) / file
                    try:
                        relative_path = str(full_path.relative_to(vault_path))
                        markdown_files.append(relative_path)
                    except ValueError:
                        continue
    else:
        for item in search_path.iterdir():
            if item.is_file() and item.suffix == '.md':
                try:
                    relative_path = str(item.relative_to(vault_path))
                    markdown_files.append(relative_path)
                except ValueError:
                    continue

    return sorted(markdown_files)
