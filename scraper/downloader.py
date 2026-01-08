"""Async media file downloader."""

import asyncio
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import aiofiles
import aiohttp
from rich.progress import Progress, TaskID


class MediaDownloader:
    """Downloads images and videos asynchronously."""

    def __init__(
        self,
        images_dir: Path,
        videos_dir: Path,
        session: Optional[aiohttp.ClientSession] = None,
        max_concurrent: int = 5,
    ):
        """
        Initialize media downloader.

        Args:
            images_dir: Directory to save images
            videos_dir: Directory to save videos
            session: Optional aiohttp session (will create one if not provided)
            max_concurrent: Maximum concurrent downloads
        """
        self.images_dir = Path(images_dir)
        self.videos_dir = Path(videos_dir)
        self.session = session
        self.max_concurrent = max_concurrent
        self._own_session = session is None

        # Create directories
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)

    async def __aenter__(self):
        """Async context manager entry."""
        if self._own_session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=300),  # 5 minute timeout for videos
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._own_session and self.session:
            await self.session.close()

    def _get_filename(self, url: str, media_type: str = "image") -> str:
        """
        Generate filename from URL.

        Args:
            url: Media URL
            media_type: Type of media ('image' or 'video')

        Returns:
            Filename with appropriate extension
        """
        parsed = urlparse(url)
        path = Path(parsed.path)
        filename = path.name

        # If no filename in URL, generate one from URL hash
        if not filename or "." not in filename:
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            if media_type == "video":
                filename = f"{url_hash}.mp4"
            else:
                filename = f"{url_hash}.jpg"

        # Sanitize filename
        filename = filename.replace(" ", "_")
        # Remove query string from filename if present
        filename = filename.split("?")[0]

        return filename

    async def download_file(
        self, url: str, filepath: Path, progress: Optional[Progress] = None, task_id: Optional[TaskID] = None
    ) -> bool:
        """
        Download a single file.

        Args:
            url: URL to download
            filepath: Path to save the file
            progress: Optional Rich progress bar
            task_id: Optional task ID for progress tracking

        Returns:
            True if successful, False otherwise
        """
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return False

                # Get file size if available
                total_size = int(response.headers.get("Content-Length", 0))

                if progress and task_id:
                    progress.update(task_id, total=total_size)

                # Download in chunks
                async with aiofiles.open(filepath, "wb") as f:
                    downloaded = 0
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)
                        downloaded += len(chunk)
                        if progress and task_id:
                            progress.update(task_id, advance=len(chunk))

                return True

        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False

    async def download_images(
        self, image_urls: List[str], progress: Optional[Progress] = None
    ) -> Dict[str, str]:
        """
        Download multiple images.

        Args:
            image_urls: List of image URLs
            progress: Optional Rich progress bar

        Returns:
            Dictionary mapping original URLs to local file paths
        """
        if not image_urls:
            return {}

        semaphore = asyncio.Semaphore(self.max_concurrent)
        results = {}

        async def download_one(url: str):
            async with semaphore:
                filename = self._get_filename(url, "image")
                filepath = self.images_dir / filename

                # Skip if already exists
                if filepath.exists():
                    results[url] = str(filepath)
                    return

                task_id = None
                if progress:
                    task_id = progress.add_task(f"Downloading {filename}", total=None)

                success = await self.download_file(url, filepath, progress, task_id)
                if success:
                    results[url] = str(filepath)
                elif task_id:
                    progress.remove_task(task_id)

        tasks = [download_one(url) for url in image_urls]
        await asyncio.gather(*tasks)

        return results

    async def download_videos(
        self, video_urls: List[str], progress: Optional[Progress] = None
    ) -> Dict[str, str]:
        """
        Download multiple videos.

        Args:
            video_urls: List of video URLs
            progress: Optional Rich progress bar

        Returns:
            Dictionary mapping original URLs to local file paths
        """
        if not video_urls:
            return {}

        semaphore = asyncio.Semaphore(self.max_concurrent)
        results = {}

        async def download_one(url: str):
            async with semaphore:
                filename = self._get_filename(url, "video")
                filepath = self.videos_dir / filename

                # Skip if already exists
                if filepath.exists():
                    results[url] = str(filepath)
                    return

                task_id = None
                if progress:
                    task_id = progress.add_task(f"Downloading {filename}", total=None)

                success = await self.download_file(url, filepath, progress, task_id)
                if success:
                    results[url] = str(filepath)
                elif task_id:
                    progress.remove_task(task_id)

        tasks = [download_one(url) for url in video_urls]
        await asyncio.gather(*tasks)

        return results

    async def download_all(
        self, images: List[str], videos: List[str], progress: Optional[Progress] = None
    ) -> Dict[str, Dict[str, str]]:
        """
        Download all media files.

        Args:
            images: List of image URLs
            videos: List of video URLs
            progress: Optional Rich progress bar

        Returns:
            Dictionary with 'images' and 'videos' keys mapping URLs to file paths
        """
        image_results = await self.download_images(images, progress)
        video_results = await self.download_videos(videos, progress)

        return {"images": image_results, "videos": video_results}
