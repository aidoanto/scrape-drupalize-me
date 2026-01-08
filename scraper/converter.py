"""Convert extracted content to Obsidian-compatible Markdown."""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse

from markdownify import markdownify as md

from scraper.extractor import TutorialContent


class MarkdownConverter:
    """Converts tutorial content to Obsidian-compatible Markdown."""

    def __init__(self, vault_root: Path):
        """
        Initialize markdown converter.

        Args:
            vault_root: Root directory of the Obsidian vault
        """
        self.vault_root = vault_root
        self.assets_dir = vault_root / "assets"
        self.images_dir = self.assets_dir / "images"
        self.videos_dir = self.assets_dir / "videos"

    def convert_tutorial(self, tutorial: TutorialContent, guide_path: Path = None) -> str:
        """
        Convert tutorial content to Markdown.

        Args:
            tutorial: TutorialContent object to convert
            guide_path: Optional path to guide directory for relative links

        Returns:
            Markdown string
        """
        # Build frontmatter
        frontmatter = self._build_frontmatter(tutorial)

        # Convert content sections
        sections = []

        # Title
        sections.append(f"# {tutorial.title}\n")

        # Goal
        if tutorial.goal:
            sections.append(f"## Goal\n\n{tutorial.goal}\n")

        # Prerequisites
        if tutorial.prerequisites:
            sections.append("## Prerequisites\n")
            for prereq in tutorial.prerequisites:
                # Convert to Obsidian wiki-link
                link_text = self._sanitize_filename(prereq)
                sections.append(f"- [[{prereq}]]")
            sections.append("")

        # Main content
        if tutorial.content:
            content_md = self._convert_html_to_markdown(tutorial.content, guide_path)
            sections.append(f"## Content\n\n{content_md}\n")

        # Recap
        if tutorial.recap:
            sections.append(f"## Recap\n\n{tutorial.recap}\n")

        # Further Understanding
        if tutorial.further_understanding:
            sections.append(f"## Further Your Understanding\n\n{tutorial.further_understanding}\n")

        # Additional Resources
        if tutorial.additional_resources:
            sections.append("## Additional Resources\n")
            for resource in tutorial.additional_resources:
                sections.append(f"- [{resource['text']}]({resource['url']})")
            sections.append("")

        # Combine frontmatter and content
        markdown = f"{frontmatter}\n\n" + "\n".join(sections)

        return markdown

    def _build_frontmatter(self, tutorial: TutorialContent) -> str:
        """Build YAML frontmatter for the tutorial."""
        frontmatter_lines = [
            "---",
            f'title: "{tutorial.title}"',
            f"source_url: {tutorial.url}",
            f"scraped_at: {datetime.now().isoformat()}",
        ]

        if tutorial.topics:
            topics_str = ", ".join([f'"{t}"' for t in tutorial.topics])
            frontmatter_lines.append(f"topics: [{topics_str}]")

        if tutorial.drupal_versions:
            versions_str = ", ".join([f'"{v}"' for v in tutorial.drupal_versions])
            frontmatter_lines.append(f"drupal_versions: [{versions_str}]")

        frontmatter_lines.append("---")
        return "\n".join(frontmatter_lines)

    def _convert_html_to_markdown(self, html: str, guide_path: Path = None) -> str:
        """
        Convert HTML to Markdown with Obsidian-specific formatting.

        Args:
            html: HTML content to convert
            guide_path: Optional path for resolving relative image/video links

        Returns:
            Markdown string
        """
        # Convert HTML to markdown
        markdown = md(
            html,
            heading_style="ATX",
            bullets="-",
            strip=["script", "style", "nav", "header", "footer"],
        )

        # Convert internal links to Obsidian wiki-links
        markdown = self._convert_internal_links(markdown)

        # Update image paths to relative paths
        markdown = self._update_media_paths(markdown, guide_path)

        return markdown

    def _convert_internal_links(self, markdown: str) -> str:
        """Convert internal Drupalize.me links to Obsidian wiki-links."""
        # Pattern for drupalize.me links
        pattern = r"\[([^\]]+)\]\(https://drupalize\.me/(?:tutorial|guide)/([^\)]+)\)"

        def replace_link(match):
            link_text = match.group(1)
            url_path = match.group(2)
            # Extract tutorial/guide name from URL
            name = url_path.split("/")[-1].replace("-", " ").title()
            # Use link text if it looks like a title, otherwise use extracted name
            if len(link_text) > 3 and not link_text.startswith("http"):
                return f"[[{link_text}]]"
            return f"[[{name}]]"

        markdown = re.sub(pattern, replace_link, markdown)
        return markdown

    def _update_media_paths(self, markdown: str, guide_path: Path = None) -> str:
        """
        Update image and video paths to relative paths.

        Args:
            markdown: Markdown content
            guide_path: Path to guide directory for calculating relative paths

        Returns:
            Updated markdown with relative paths
        """
        # Pattern for image links
        img_pattern = r"!\[([^\]]*)\]\(([^\)]+)\)"

        def replace_image(match):
            alt_text = match.group(1)
            url = match.group(2)

            # If it's already a relative path, keep it
            if not url.startswith("http"):
                return match.group(0)

            # Extract filename from URL
            parsed = urlparse(url)
            filename = Path(parsed.path).name
            if not filename:
                filename = "image.png"

            # Calculate relative path
            if guide_path:
                # Relative from guide directory to assets
                rel_path = Path("..") / "assets" / "images" / filename
            else:
                rel_path = Path("assets") / "images" / filename

            return f"![{alt_text}]({rel_path.as_posix()})"

        markdown = re.sub(img_pattern, replace_image, markdown)

        # Pattern for video links (if any)
        video_pattern = r"\[([^\]]*)\]\(([^\)]+\.(mp4|webm|ogg|mov|avi))\)"

        def replace_video(match):
            link_text = match.group(1)
            url = match.group(2)

            # Extract filename from URL
            parsed = urlparse(url)
            filename = Path(parsed.path).name

            # Calculate relative path
            if guide_path:
                rel_path = Path("..") / "assets" / "videos" / filename
            else:
                rel_path = Path("assets") / "videos" / filename

            return f"[{link_text}]({rel_path.as_posix()})"

        markdown = re.sub(video_pattern, replace_video, markdown)

        return markdown

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a name for use in filenames or wiki-links.

        Args:
            name: Name to sanitize

        Returns:
            Sanitized name
        """
        # Remove special characters but keep spaces for wiki-links
        # Obsidian wiki-links can have spaces
        return name.strip()

    def get_media_paths(self, tutorial: TutorialContent) -> Dict[str, List[str]]:
        """
        Get paths for media files relative to vault root.

        Args:
            tutorial: TutorialContent object

        Returns:
            Dictionary with 'images' and 'videos' lists of URLs
        """
        return {
            "images": tutorial.images,
            "videos": tutorial.videos,
        }
