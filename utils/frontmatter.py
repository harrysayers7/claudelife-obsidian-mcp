"""Frontmatter parsing and generation for markdown files."""
import re
from datetime import datetime
from typing import Optional, Tuple


def parse_frontmatter(content: str) -> Tuple[dict, str]:
    """
    Parse YAML frontmatter from markdown content.

    Args:
        content: Full markdown file content

    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    frontmatter = {}
    body = content

    # Match YAML frontmatter (--- ... ---)
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if match:
        frontmatter_text = match.group(1)
        body = match.group(2)

        # Parse simple key: value pairs
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"\'')

    return frontmatter, body


def generate_frontmatter(date: Optional[datetime] = None) -> str:
    """
    Generate frontmatter with date.

    Args:
        date: Date to use (defaults to now)

    Returns:
        Formatted frontmatter string
    """
    if date is None:
        date = datetime.now()

    date_str = date.strftime("%Y-%m-%d %H:%M")

    return f"""---
date: "{date_str}"
---

"""


def ensure_frontmatter(content: str) -> str:
    """
    Ensure content has frontmatter, adding it if missing.

    Args:
        content: File content

    Returns:
        Content with frontmatter
    """
    frontmatter, body = parse_frontmatter(content)

    if frontmatter:
        # Already has frontmatter
        return content

    # Add frontmatter
    return generate_frontmatter() + body


def update_frontmatter_field(content: str, key: str, value: str) -> str:
    """
    Update or add a field in frontmatter.

    Args:
        content: File content
        key: Frontmatter key
        value: New value

    Returns:
        Updated content
    """
    frontmatter, body = parse_frontmatter(content)

    # Update frontmatter dict
    frontmatter[key] = value

    # Rebuild frontmatter
    fm_lines = ["---"]
    for k, v in frontmatter.items():
        if ' ' in v or ':' in v:
            fm_lines.append(f'{k}: "{v}"')
        else:
            fm_lines.append(f'{k}: {v}')
    fm_lines.append("---")
    fm_lines.append("")

    return '\n'.join(fm_lines) + body
