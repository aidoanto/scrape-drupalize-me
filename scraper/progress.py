"""Progress tracking and resume capability."""

import json
from pathlib import Path
from typing import Dict, List, Set


class ProgressTracker:
    """Tracks scraping progress and enables resuming."""

    def __init__(self, metadata_dir: Path):
        """
        Initialize progress tracker.

        Args:
            metadata_dir: Directory to store progress metadata
        """
        self.metadata_dir = Path(metadata_dir)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.progress_file = self.metadata_dir / "progress.json"

    def load(self) -> Dict:
        """
        Load progress from file.

        Returns:
            Progress dictionary
        """
        if self.progress_file.exists():
            with open(self.progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "completed_guides": [],
            "completed_tutorials": [],
            "failed_tutorials": [],
        }

    def save(self, progress: Dict):
        """
        Save progress to file.

        Args:
            progress: Progress dictionary to save
        """
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

    def is_guide_completed(self, guide_url: str) -> bool:
        """
        Check if a guide has been completed.

        Args:
            guide_url: URL of the guide

        Returns:
            True if guide is completed
        """
        progress = self.load()
        return guide_url in progress.get("completed_guides", [])

    def is_tutorial_completed(self, tutorial_url: str) -> bool:
        """
        Check if a tutorial has been completed.

        Args:
            tutorial_url: URL of the tutorial

        Returns:
            True if tutorial is completed
        """
        progress = self.load()
        return tutorial_url in progress.get("completed_tutorials", [])

    def mark_guide_completed(self, guide_url: str):
        """
        Mark a guide as completed.

        Args:
            guide_url: URL of the guide
        """
        progress = self.load()
        if "completed_guides" not in progress:
            progress["completed_guides"] = []
        if guide_url not in progress["completed_guides"]:
            progress["completed_guides"].append(guide_url)
        self.save(progress)

    def mark_tutorial_completed(self, tutorial_url: str):
        """
        Mark a tutorial as completed.

        Args:
            tutorial_url: URL of the tutorial
        """
        progress = self.load()
        if "completed_tutorials" not in progress:
            progress["completed_tutorials"] = []
        if tutorial_url not in progress["completed_tutorials"]:
            progress["completed_tutorials"].append(tutorial_url)
        self.save(progress)

    def mark_tutorial_failed(self, tutorial_url: str, error: str):
        """
        Mark a tutorial as failed.

        Args:
            tutorial_url: URL of the tutorial
            error: Error message
        """
        progress = self.load()
        if "failed_tutorials" not in progress:
            progress["failed_tutorials"] = []
        failed_entry = {"url": tutorial_url, "error": error}
        if failed_entry not in progress["failed_tutorials"]:
            progress["failed_tutorials"].append(failed_entry)
        self.save(progress)

    def get_completed_urls(self) -> Set[str]:
        """
        Get set of all completed URLs.

        Returns:
            Set of completed URLs
        """
        progress = self.load()
        completed = set(progress.get("completed_guides", []))
        completed.update(progress.get("completed_tutorials", []))
        return completed
