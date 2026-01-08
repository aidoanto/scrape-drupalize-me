"""Obsidian vault structure management."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class VaultManager:
    """Manages Obsidian vault directory structure."""

    def __init__(self, vault_root: Path):
        """
        Initialize vault manager.

        Args:
            vault_root: Root directory of the Obsidian vault
        """
        self.vault_root = Path(vault_root)
        self.guides_dir = self.vault_root / "Guides"
        self.topics_dir = self.vault_root / "Topics"
        self.assets_dir = self.vault_root / "assets"
        self.images_dir = self.assets_dir / "images"
        self.videos_dir = self.assets_dir / "videos"
        self.metadata_dir = self.vault_root / "_metadata"

    def initialize(self):
        """Create vault directory structure."""
        self.vault_root.mkdir(parents=True, exist_ok=True)
        self.guides_dir.mkdir(exist_ok=True)
        self.topics_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        self.videos_dir.mkdir(exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)

    def get_guide_path(self, guide_name: str) -> Path:
        """
        Get path for a guide directory.

        Args:
            guide_name: Name of the guide

        Returns:
            Path to guide directory
        """
        safe_name = self._sanitize_dirname(guide_name)
        return self.guides_dir / safe_name

    def get_tutorial_path(self, guide_path: Path, tutorial_name: str, subfolder: Optional[str] = None) -> Path:
        """
        Get path for a tutorial markdown file.

        Args:
            guide_path: Path to guide directory
            tutorial_name: Name of the tutorial
            subfolder: Optional subfolder within the guide

        Returns:
            Path to tutorial markdown file
        """
        if subfolder:
            tutorial_dir = guide_path / self._sanitize_dirname(subfolder)
            tutorial_dir.mkdir(parents=True, exist_ok=True)
        else:
            tutorial_dir = guide_path

        safe_name = self._sanitize_filename(tutorial_name)
        return tutorial_dir / f"{safe_name}.md"

    def create_guide_index(self, guide_path: Path, guide_name: str, tutorials: List[Dict]) -> Path:
        """
        Create an index file for a guide.

        Args:
            guide_path: Path to guide directory
            guide_name: Name of the guide
            tutorials: List of tutorial metadata dictionaries

        Returns:
            Path to the index file
        """
        index_path = guide_path / "_index.md"

        content_lines = [
            f"# {guide_name}",
            "",
            "## Tutorials",
            "",
        ]

        # Group tutorials by subfolder if applicable
        tutorials_by_folder: Dict[str, List[Dict]] = {}
        for tutorial in tutorials:
            folder = tutorial.get("subfolder", "")
            if folder not in tutorials_by_folder:
                tutorials_by_folder[folder] = []
            tutorials_by_folder[folder].append(tutorial)

        for folder, folder_tutorials in tutorials_by_folder.items():
            if folder:
                content_lines.append(f"### {folder}\n")
            for tutorial in folder_tutorials:
                title = tutorial.get("title", "Untitled")
                filename = tutorial.get("filename", "")
                if filename:
                    content_lines.append(f"- [[{title}]]")
                else:
                    content_lines.append(f"- {title}")
            content_lines.append("")

        content = "\n".join(content_lines)

        index_path.write_text(content, encoding="utf-8")
        return index_path

    def create_topic_index(self, topic: str, tutorials: List[Dict]) -> Path:
        """
        Create an index file for a topic.

        Args:
            topic: Topic name
            tutorials: List of tutorial metadata dictionaries

        Returns:
            Path to the topic index file
        """
        safe_topic = self._sanitize_filename(topic)
        index_path = self.topics_dir / f"{safe_topic}.md"

        content_lines = [
            f"# {topic}",
            "",
            f"All tutorials related to **{topic}**.",
            "",
            "## Tutorials",
            "",
        ]

        for tutorial in tutorials:
            title = tutorial.get("title", "Untitled")
            guide = tutorial.get("guide", "")
            filename = tutorial.get("filename", "")
            if filename:
                content_lines.append(f"- [[{title}]] ({guide})")
            else:
                content_lines.append(f"- {title} ({guide})")

        content = "\n".join(content_lines)
        index_path.write_text(content, encoding="utf-8")
        return index_path

    def _sanitize_dirname(self, name: str) -> str:
        """
        Sanitize a name for use as a directory name.

        Args:
            name: Name to sanitize

        Returns:
            Sanitized directory name
        """
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, "_")
        # Remove leading/trailing spaces and dots
        name = name.strip(" .")
        return name

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a name for use as a filename.

        Args:
            name: Name to sanitize

        Returns:
            Sanitized filename (without extension)
        """
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, "_")
        # Remove leading/trailing spaces and dots
        name = name.strip(" .")
        # Limit length
        if len(name) > 200:
            name = name[:200]
        return name

    def save_metadata(self, metadata: Dict, filename: str = "scrape_log.json"):
        """
        Save metadata to JSON file.

        Args:
            metadata: Metadata dictionary to save
            filename: Name of the metadata file
        """
        metadata_path = self.metadata_dir / filename
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def load_metadata(self, filename: str = "scrape_log.json") -> Dict:
        """
        Load metadata from JSON file.

        Args:
            filename: Name of the metadata file

        Returns:
            Metadata dictionary
        """
        metadata_path = self.metadata_dir / filename
        if metadata_path.exists():
            with open(metadata_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
