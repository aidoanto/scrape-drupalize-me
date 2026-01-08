"""Main scraper for guides and tutorials."""

import asyncio
import re
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from scraper.browser import BrowserSession
from scraper.converter import MarkdownConverter
from scraper.downloader import MediaDownloader
from scraper.extractor import ContentExtractor, TutorialContent
from scraper.progress import ProgressTracker
from scraper.vault import VaultManager


class DrupalizeScraper:
    """Main scraper for Drupalize.me content."""

    def __init__(
        self,
        vault_root: Path,
        base_url: str = "https://drupalize.me",
        delay: float = 2.5,
        headless: bool = True,
        cookies_file: Optional[Path] = None,
        cdp_url: Optional[str] = None,
    ):
        """
        Initialize scraper.

        Args:
            vault_root: Root directory for the Obsidian vault
            base_url: Base URL of Drupalize.me
            delay: Delay between requests in seconds
            headless: Whether to run browser in headless mode
        """
        self.vault_root = Path(vault_root)
        self.base_url = base_url
        self.delay = delay
        self.headless = headless
        self.cookies_file = cookies_file
        self.cdp_url = cdp_url

        self.vault = VaultManager(self.vault_root)
        self.extractor = ContentExtractor(base_url)
        self.converter = MarkdownConverter(self.vault_root)
        self.progress = ProgressTracker(self.vault.metadata_dir)
        self.console = Console()

    async def scrape_all(self):
        """Scrape all guides and tutorials."""
        self.vault.initialize()

        async with BrowserSession(
            headless=self.headless,
            cookies_file=self.cookies_file,
            cdp_url=self.cdp_url,
        ) as browser:
            # First, get list of all guides
            guides = await self._get_guide_list(browser)

            self.console.print(f"[green]Found {len(guides)} guides[/green]")

            # Scrape each guide (skip if already completed)
            for guide_url, guide_name in guides:
                if not self.progress.is_guide_completed(guide_url):
                    await self._scrape_guide(browser, guide_url, guide_name)
                    self.progress.mark_guide_completed(guide_url)
                else:
                    self.console.print(f"[yellow]Skipping completed guide: {guide_name}[/yellow]")
                await asyncio.sleep(self.delay)

            # Also scrape standalone tutorials
            await self._scrape_standalone_tutorials(browser)

    async def _get_guide_list(self, browser: BrowserSession) -> List[tuple]:
        """
        Get list of all guides.

        Args:
            browser: Browser session

        Returns:
            List of (url, name) tuples
        """
        guides = []
        search_url = f"{self.base_url}/search?f%5B0%5D=type%3Aguide"

        try:
            await browser.navigate(search_url)
            await browser.wait_for_cloudflare()

            html = await browser.page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Find guide links
            guide_links = soup.find_all("a", href=re.compile(r"/guide/"))
            for link in guide_links:
                href = link.get("href", "")
                if href.startswith("/guide/"):
                    full_url = urljoin(self.base_url, href)
                    name = link.get_text(strip=True)
                    if name and (full_url, name) not in guides:
                        guides.append((full_url, name))

        except Exception as e:
            self.console.print(f"[red]Error fetching guide list: {e}[/red]")

        return guides

    async def _scrape_guide(self, browser: BrowserSession, guide_url: str, guide_name: str):
        """
        Scrape a single guide and all its tutorials.

        Args:
            browser: Browser session
            guide_url: URL of the guide
            guide_name: Name of the guide
        """
        self.console.print(f"[cyan]Scraping guide: {guide_name}[/cyan]")

        try:
            await browser.navigate(guide_url)
            await browser.wait_for_cloudflare()

            html = await browser.page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Extract guide overview/description
            guide_overview = self._extract_guide_overview(soup)

            # Find all tutorial links in this guide
            tutorial_links = self._extract_tutorial_links_from_guide(soup)

            self.console.print(f"  Found {len(tutorial_links)} tutorials")

            # Create guide directory
            guide_path = self.vault.get_guide_path(guide_name)
            guide_path.mkdir(parents=True, exist_ok=True)

            # Save guide overview
            overview_path = guide_path / "_overview.md"
            overview_content = f"# {guide_name}\n\n{guide_overview}\n"
            overview_path.write_text(overview_content, encoding="utf-8")

            # Scrape each tutorial (skip if already completed)
            tutorials_metadata = []
            for tutorial_url, tutorial_name, subfolder in tutorial_links:
                if not self.progress.is_tutorial_completed(tutorial_url):
                    tutorial_meta = await self._scrape_tutorial(
                        browser, tutorial_url, tutorial_name, guide_path, guide_name, subfolder
                    )
                    if tutorial_meta:
                        tutorials_metadata.append(tutorial_meta)
                        self.progress.mark_tutorial_completed(tutorial_url)
                    else:
                        self.progress.mark_tutorial_failed(tutorial_url, "Scraping failed")
                else:
                    self.console.print(f"      [yellow]Skipping completed: {tutorial_name}[/yellow]")
                await asyncio.sleep(self.delay)

            # Create guide index
            self.vault.create_guide_index(guide_path, guide_name, tutorials_metadata)

        except Exception as e:
            self.console.print(f"[red]Error scraping guide {guide_name}: {e}[/red]")

    async def _scrape_tutorial(
        self,
        browser: BrowserSession,
        tutorial_url: str,
        tutorial_name: str,
        guide_path: Path,
        guide_name: str,
        subfolder: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Scrape a single tutorial.

        Args:
            browser: Browser session
            tutorial_url: URL of the tutorial
            tutorial_name: Name of the tutorial
            guide_path: Path to guide directory
            guide_name: Name of the guide
            subfolder: Optional subfolder name

        Returns:
            Tutorial metadata dictionary or None if failed
        """
        try:
            self.console.print(f"    Scraping: {tutorial_name}")

            # Get tutorial HTML
            html = await browser.get_content(tutorial_url)
            await browser.wait_for_cloudflare()

            # Extract content
            tutorial = self.extractor.extract_tutorial(html, tutorial_url)

            # Download media
            async with MediaDownloader(
                self.vault.images_dir, self.vault.videos_dir
            ) as downloader:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    console=self.console,
                ) as progress:
                    media_paths = await downloader.download_all(
                        tutorial.images, tutorial.videos, progress
                    )

            # Convert to markdown
            markdown = self.converter.convert_tutorial(tutorial, guide_path)

            # Save tutorial file
            tutorial_path = self.vault.get_tutorial_path(guide_path, tutorial.title, subfolder)
            tutorial_path.write_text(markdown, encoding="utf-8")

            return {
                "title": tutorial.title,
                "filename": tutorial_path.name,
                "subfolder": subfolder,
                "url": tutorial_url,
            }

        except Exception as e:
            self.console.print(f"[red]Error scraping tutorial {tutorial_name}: {e}[/red]")
            return None

    async def _scrape_standalone_tutorials(self, browser: BrowserSession):
        """Scrape tutorials that aren't part of guides."""
        self.console.print("[cyan]Scraping standalone tutorials[/cyan]")

        search_url = f"{self.base_url}/search?f%5B0%5D=type%3Atutorial"

        try:
            await browser.navigate(search_url)
            await browser.wait_for_cloudflare()

            html = await browser.page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Find tutorial links
            tutorial_links = soup.find_all("a", href=re.compile(r"/tutorial/"))
            tutorials = []
            for link in tutorial_links:
                href = link.get("href", "")
                if href.startswith("/tutorial/"):
                    full_url = urljoin(self.base_url, href)
                    name = link.get_text(strip=True)
                    if name and (full_url, name) not in tutorials:
                        tutorials.append((full_url, name))

            self.console.print(f"Found {len(tutorials)} standalone tutorials")

            # Create standalone directory
            standalone_path = self.vault_root / "Tutorials"
            standalone_path.mkdir(exist_ok=True)

            # Scrape each tutorial (skip if already completed)
            for tutorial_url, tutorial_name in tutorials:
                if not self.progress.is_tutorial_completed(tutorial_url):
                    tutorial_meta = await self._scrape_tutorial(
                        browser, tutorial_url, tutorial_name, standalone_path, "Standalone Tutorials"
                    )
                    if tutorial_meta:
                        self.progress.mark_tutorial_completed(tutorial_url)
                    else:
                        self.progress.mark_tutorial_failed(tutorial_url, "Scraping failed")
                else:
                    self.console.print(f"  [yellow]Skipping completed: {tutorial_name}[/yellow]")
                await asyncio.sleep(self.delay)

        except Exception as e:
            self.console.print(f"[red]Error scraping standalone tutorials: {e}[/red]")

    def _extract_guide_overview(self, soup: BeautifulSoup) -> str:
        """Extract guide overview/description."""
        main_content = soup.find("main") or soup.find("article") or soup

        # Try to find overview section
        overview_elem = main_content.find("div", class_=re.compile(r"overview|description|intro", re.I))
        if overview_elem:
            return overview_elem.get_text(separator="\n", strip=True)

        # Fallback: get first paragraph
        first_p = main_content.find("p")
        if first_p:
            return first_p.get_text(strip=True)

        return ""

    def _extract_tutorial_links_from_guide(self, soup: BeautifulSoup) -> List[tuple]:
        """
        Extract tutorial links from a guide page.

        Returns:
            List of (url, name, subfolder) tuples
        """
        tutorials = []
        main_content = soup.find("main") or soup.find("article") or soup

        # Find all tutorial links
        tutorial_links = main_content.find_all("a", href=re.compile(r"/tutorial/"))

        for link in tutorial_links:
            href = link.get("href", "")
            if href.startswith("/tutorial/"):
                full_url = urljoin(self.base_url, href)
                name = link.get_text(strip=True)

                # Try to determine subfolder from parent structure
                subfolder = None
                parent = link.find_parent(["section", "div", "li"])
                if parent:
                    # Look for heading that might indicate a section
                    heading = parent.find_previous(["h2", "h3", "h4"])
                    if heading:
                        heading_text = heading.get_text(strip=True)
                        # Skip if it's a generic heading
                        if heading_text and heading_text.lower() not in [
                            "tutorials",
                            "lessons",
                            "content",
                        ]:
                            subfolder = heading_text

                if name and (full_url, name, subfolder) not in tutorials:
                    tutorials.append((full_url, name, subfolder))

        return tutorials
