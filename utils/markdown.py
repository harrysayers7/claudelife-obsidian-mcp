"""Markdown parsing utilities."""
import re
from typing import Optional, List, Tuple


def find_heading_position(content: str, heading: str) -> Optional[Tuple[int, int]]:
    """
    Find the position of a heading in markdown content.

    Args:
        content: Markdown content
        heading: Heading text to find (without # symbols)

    Returns:
        Tuple of (line_number, char_position) or None if not found
    """
    lines = content.split('\n')

    # Clean heading text for comparison
    heading_clean = heading.strip().lower()

    for i, line in enumerate(lines):
        # Match markdown headings (# Heading)
        match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if match:
            line_heading = match.group(2).strip().lower()
            if line_heading == heading_clean:
                # Calculate character position
                char_pos = sum(len(l) + 1 for l in lines[:i])  # +1 for newlines
                return (i, char_pos)

    return None


def insert_content_at_heading(
    content: str,
    heading: str,
    new_content: str,
    position: str = "after"
) -> str:
    """
    Insert content before or after a heading.

    Args:
        content: Original markdown content
        heading: Target heading (without # symbols)
        new_content: Content to insert
        position: "before" or "after"

    Returns:
        Updated content

    Raises:
        ValueError: If heading not found or invalid position
    """
    if position not in ["before", "after"]:
        raise ValueError(f"Invalid position: {position}. Must be 'before' or 'after'")

    lines = content.split('\n')
    heading_clean = heading.strip().lower()

    for i, line in enumerate(lines):
        match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if match:
            line_heading = match.group(2).strip().lower()
            if line_heading == heading_clean:
                if position == "before":
                    # Insert before heading
                    lines.insert(i, new_content)
                else:
                    # Insert after heading (and any content on same line)
                    lines.insert(i + 1, new_content)

                return '\n'.join(lines)

    raise ValueError(f"Heading not found: {heading}")


def get_headings(content: str) -> List[Tuple[int, str, str]]:
    """
    Extract all headings from markdown content.

    Args:
        content: Markdown content

    Returns:
        List of (level, heading_text, line_number) tuples
    """
    lines = content.split('\n')
    headings = []

    for i, line in enumerate(lines):
        match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if match:
            level = len(match.group(1))
            heading_text = match.group(2).strip()
            headings.append((level, heading_text, i))

    return headings


def extract_tags(content: str) -> List[str]:
    """
    Extract all hashtags from markdown content.

    Args:
        content: Markdown content

    Returns:
        List of unique tags (without # symbol)
    """
    # Find all hashtags (but not in code blocks)
    # Simple approach: match #word boundaries
    tags = re.findall(r'#([\w-]+)\b', content)

    # Also check frontmatter
    from utils.frontmatter import parse_frontmatter

    frontmatter, _ = parse_frontmatter(content)
    if 'tags' in frontmatter:
        tags_value = frontmatter['tags']
        if isinstance(tags_value, str):
            # Parse comma-separated or space-separated tags
            fm_tags = re.split(r'[,\s]+', tags_value)
            tags.extend(t.strip().lstrip('#') for t in fm_tags if t.strip())

    # Return unique tags
    return sorted(list(set(t for t in tags if t)))
