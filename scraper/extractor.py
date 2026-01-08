"""HTML content extraction from Drupalize.me pages."""

import re
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


@dataclass
class TutorialContent:
    """Extracted tutorial content."""

    title: str
    url: str
    topics: List[str]
    drupal_versions: List[str]
    goal: Optional[str] = None
    prerequisites: List[str] = field(default_factory=list)
    content: str = ""
    recap: Optional[str] = None
    further_understanding: Optional[str] = None
    additional_resources: Optional[List[dict]] = None  # List of {"text": str, "url": str}
    images: List[str] = field(default_factory=list)  # List of image URLs
    videos: List[str] = field(default_factory=list)  # List of video URLs


class ContentExtractor:
    """Extracts content from Drupalize.me HTML pages."""

    def __init__(self, base_url: str = "https://drupalize.me"):
        """
        Initialize content extractor.

        Args:
            base_url: Base URL for resolving relative links
        """
        self.base_url = base_url

    def extract_tutorial(self, html: str, url: str) -> TutorialContent:
        """
        Extract tutorial content from HTML.

        Args:
            html: HTML content of the tutorial page
            url: URL of the tutorial page

        Returns:
            TutorialContent object with extracted data
        """
        soup = BeautifulSoup(html, "html.parser")

        # Extract title
        title = self._extract_title(soup)

        # Extract topics/tags
        topics = self._extract_topics(soup)

        # Extract Drupal versions
        drupal_versions = self._extract_drupal_versions(soup)

        # Extract main content sections
        main_content = soup.find("main") or soup.find("article") or soup

        # Extract goal
        goal = self._extract_section(main_content, "Goal")

        # Extract prerequisites
        prerequisites = self._extract_prerequisites(main_content)

        # Extract main content
        content = self._extract_main_content(main_content)

        # Extract recap
        recap = self._extract_section(main_content, "Recap")

        # Extract further understanding
        further_understanding = self._extract_section(main_content, "Further your understanding")

        # Extract additional resources
        additional_resources = self._extract_additional_resources(main_content)

        # Extract media
        images = self._extract_images(soup, url)
        videos = self._extract_videos(soup, url)

        return TutorialContent(
            title=title,
            url=url,
            topics=topics,
            drupal_versions=drupal_versions,
            goal=goal,
            prerequisites=prerequisites,
            content=content,
            recap=recap,
            further_understanding=further_understanding,
            additional_resources=additional_resources or [],
            images=images,
            videos=videos,
        )

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract tutorial title."""
        # Try multiple selectors for title
        title_selectors = [
            "h1",
            "article h1",
            "main h1",
            '[role="article"] h1',
            ".field--name-title",
        ]

        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                if title:
                    return title

        # Fallback to page title
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Remove "| Drupalize.Me" suffix if present
            title = re.sub(r"\s*\|\s*Drupalize\.Me.*$", "", title, flags=re.IGNORECASE)
            return title

        return "Untitled Tutorial"

    def _extract_topics(self, soup: BeautifulSoup) -> List[str]:
        """Extract topic tags."""
        topics = []
        main_content = soup.find("main") or soup.find("article") or soup

        # Look for topic links
        topic_links = main_content.find_all("a", href=re.compile(r"/topic/|/tag/"))
        for link in topic_links:
            topic = link.get_text(strip=True)
            if topic and topic not in topics:
                topics.append(topic)

        # Also check for topic metadata
        topic_meta = soup.find_all("meta", {"property": re.compile(r"topic|tag", re.I)})
        for meta in topic_meta:
            content = meta.get("content", "").strip()
            if content and content not in topics:
                topics.append(content)

        return topics

    def _extract_drupal_versions(self, soup: BeautifulSoup) -> List[str]:
        """Extract Drupal version tags."""
        versions = []
        main_content = soup.find("main") or soup.find("article") or soup

        # Look for version links (e.g., "11.0.x", "Drupal 11")
        version_pattern = re.compile(r"(?:Drupal\s+)?(\d+\.\d+\.x|\d+\.\d+)", re.I)
        version_links = main_content.find_all("a", href=re.compile(r"/version/|/drupal-\d+"))
        for link in version_links:
            text = link.get_text(strip=True)
            match = version_pattern.search(text)
            if match:
                version = match.group(1)
                if version not in versions:
                    versions.append(version)

        # Also check text content for version mentions
        text_content = main_content.get_text()
        matches = version_pattern.findall(text_content)
        for match in matches:
            if match not in versions:
                versions.append(match)

        return versions

    def _extract_section(self, soup: BeautifulSoup, section_name: str) -> Optional[str]:
        """Extract a specific section by heading."""
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        for heading in headings:
            text = heading.get_text(strip=True)
            if section_name.lower() in text.lower():
                # Get content after this heading until next heading
                content_parts = []
                current = heading.find_next_sibling()
                while current:
                    if current.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                        break
                    if current.name:
                        content_parts.append(str(current))
                    current = current.find_next_sibling()

                if content_parts:
                    section_soup = BeautifulSoup("".join(content_parts), "html.parser")
                    return section_soup.get_text(separator="\n", strip=True)

        return None

    def _extract_prerequisites(self, soup: BeautifulSoup) -> List[str]:
        """Extract prerequisite tutorials."""
        prerequisites = []
        prereq_section = self._extract_section(soup, "Prerequisite")
        if prereq_section:
            # Look for links in the prerequisites section
            prereq_elem = None
            for heading in soup.find_all(["h2", "h3"]):
                if "prerequisite" in heading.get_text(strip=True).lower():
                    prereq_elem = heading.find_next_sibling("ul")
                    break

            if prereq_elem:
                for li in prereq_elem.find_all("li", recursive=False):
                    link = li.find("a")
                    if link:
                        prereq_text = link.get_text(strip=True)
                        if prereq_text:
                            prerequisites.append(prereq_text)

        return prerequisites

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main tutorial content."""
        main_content = soup.find("main") or soup.find("article") or soup

        # Remove unwanted sections
        for unwanted in main_content.find_all(["nav", "header", "footer", "aside"]):
            unwanted.decompose()

        # Remove sections we've already extracted separately
        for heading in main_content.find_all(["h1", "h2", "h3"]):
            text = heading.get_text(strip=True).lower()
            if any(
                keyword in text
                for keyword in ["goal", "prerequisite", "recap", "further", "additional resource"]
            ):
                # Remove this section and its content
                current = heading
                while current:
                    next_sibling = current.find_next_sibling()
                    if current.name in ["h1", "h2", "h3"] and current != heading:
                        break
                    current.decompose()
                    current = next_sibling
                    if current and current.name in ["h1", "h2", "h3"]:
                        break

        # Get remaining content
        content_html = str(main_content)
        return content_html

    def _extract_additional_resources(self, soup: BeautifulSoup) -> List[dict]:
        """Extract additional resources links."""
        resources = []
        resources_section = self._extract_section(soup, "Additional resource")
        if resources_section:
            # Find the resources list
            for heading in soup.find_all(["h2", "h3"]):
                if "additional resource" in heading.get_text(strip=True).lower():
                    list_elem = heading.find_next_sibling("ul")
                    if list_elem:
                        for li in list_elem.find_all("li", recursive=False):
                            link = li.find("a")
                            if link:
                                resources.append(
                                    {
                                        "text": link.get_text(strip=True),
                                        "url": urljoin(self.base_url, link.get("href", "")),
                                    }
                                )

        return resources

    def _extract_images(self, soup: BeautifulSoup, page_url: str) -> List[str]:
        """Extract image URLs from the page."""
        images = []
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if src:
                # Resolve relative URLs
                full_url = urljoin(page_url, src)
                if full_url not in images:
                    images.append(full_url)

        return images

    def _extract_videos(self, soup: BeautifulSoup, page_url: str) -> List[str]:
        """Extract video URLs from the page."""
        videos = []

        # Look for video tags
        for video in soup.find_all("video"):
            src = video.get("src")
            if src:
                full_url = urljoin(page_url, src)
                if full_url not in videos:
                    videos.append(full_url)

            # Check source tags
            for source in video.find_all("source"):
                src = source.get("src")
                if src:
                    full_url = urljoin(page_url, src)
                    if full_url not in videos:
                        videos.append(full_url)

        # Look for iframe embeds (YouTube, Vimeo, etc.)
        for iframe in soup.find_all("iframe"):
            src = iframe.get("src", "")
            if any(domain in src for domain in ["youtube", "vimeo", "dailymotion", "video"]):
                if src not in videos:
                    videos.append(src)

        # Look for video links
        for link in soup.find_all("a", href=re.compile(r"\.(mp4|webm|ogg|mov|avi)$", re.I)):
            href = link.get("href", "")
            full_url = urljoin(page_url, href)
            if full_url not in videos:
                videos.append(full_url)

        return videos
