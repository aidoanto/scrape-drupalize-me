"""
Repair script for the Drupalize.me vault.

Fixes two issues:
1. Empty titles - extracts proper titles from URLs or content
2. Missing images - downloads images still pointing to original URLs

Usage:
    uv run python repair_vault.py --vault-dir ./vault
"""

import asyncio
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin, unquote

import aiofiles
import aiohttp
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


def slug_to_title(slug: str) -> str:
    """Convert a URL slug to a readable title."""
    # Remove common suffixes
    slug = re.sub(r'free$', '', slug)
    # Replace hyphens with spaces and title case
    title = slug.replace('-', ' ').title()
    # Fix common acronyms
    replacements = {
        'Api': 'API',
        'Css': 'CSS',
        'Html': 'HTML',
        'Php': 'PHP',
        'Sql': 'SQL',
        'Ui': 'UI',
        'Url': 'URL',
        'Json': 'JSON',
        'Xml': 'XML',
        'Ddev': 'DDEV',
        'Drupal S': "Drupal's",
        'Drush': 'Drush',
        'Twig': 'Twig',
        'Oauth': 'OAuth',
        'Jsonapi': 'JSON:API',
        'Graphql': 'GraphQL',
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title


def extract_title_from_url(url: str) -> str:
    """Extract a title from a tutorial URL."""
    # Parse the URL path
    parsed = urlparse(url)
    path = parsed.path
    
    # Extract the last part of the path (the slug)
    # e.g., /tutorial/user-guide/understanding-drupal -> understanding-drupal
    parts = [p for p in path.split('/') if p and p != 'tutorial']
    if parts:
        slug = parts[-1]
        return slug_to_title(slug)
    return "Untitled"


def extract_title_from_content(content: str) -> str:
    """Try to extract title from markdown content headings."""
    # Look for first h1 or h2 that has actual text
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# ') and len(line) > 2:
            title = line[2:].strip()
            if title and title != '#':
                return title
        if line.startswith('## ') and len(line) > 3:
            title = line[3:].strip()
            if title and title not in ['Content', 'Videos', 'Goal', 'Prerequisites']:
                return title
    return ""


async def download_image(session: aiohttp.ClientSession, url: str, dest_path: Path) -> bool:
    """Download an image from URL to destination path."""
    try:
        # Handle relative URLs
        if url.startswith('/'):
            url = f"https://drupalize.me{url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://drupalize.me/',
        }
        
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=60)) as response:
            if response.status == 200:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                async with aiofiles.open(dest_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)
                return True
            else:
                console.print(f"[yellow]HTTP {response.status} for {url}[/yellow]")
    except Exception as e:
        console.print(f"[yellow]Could not download {url}: {e}[/yellow]")
    return False


def find_image_urls(content: str) -> list[tuple[str, str]]:
    """Find all image URLs in markdown content that need downloading.
    
    Returns list of (original_url, alt_text) tuples.
    """
    images = []
    
    # Match markdown images: ![alt](url)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    for match in re.finditer(pattern, content):
        alt_text = match.group(1)
        url = match.group(2)
        
        # Skip already-local images
        if url.startswith('../assets/') or url.startswith('./assets/'):
            continue
        
        # Include drupalize.me images and relative paths
        if 'drupalize.me' in url or url.startswith('/sites/') or url.startswith('/files/'):
            images.append((url, alt_text))
    
    return images


def slugify(text: str) -> str:
    """Convert text to a valid filename slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


class VaultRepairer:
    """Repairs issues in an existing vault."""
    
    def __init__(self, vault_dir: Path):
        self.vault_dir = vault_dir
        self.tutorials_dir = vault_dir / "Tutorials"
        self.guides_dir = vault_dir / "Guides"
        self.images_dir = vault_dir / "assets" / "images"
        self.repairs_made = {
            'titles_fixed': 0,
            'images_downloaded': 0,
            'files_renamed': 0,
            'links_updated': 0,
        }
        
    async def repair_all(self):
        """Run all repairs."""
        console.print("[bold cyan]Starting vault repair...[/bold cyan]\n")
        
        # Step 1: Fix empty titles and rename files
        await self.fix_empty_titles()
        
        # Step 2: Download missing images and update links
        await self.fix_missing_images()
        
        # Step 3: Regenerate the index
        await self.regenerate_index()
        
        # Summary
        console.print("\n[bold green]✅ Repair complete![/bold green]")
        console.print(f"  - Titles fixed: {self.repairs_made['titles_fixed']}")
        console.print(f"  - Files renamed: {self.repairs_made['files_renamed']}")
        console.print(f"  - Images downloaded: {self.repairs_made['images_downloaded']}")
        console.print(f"  - Image links updated: {self.repairs_made['links_updated']}")
    
    async def fix_empty_titles(self):
        """Find and fix tutorials with empty titles."""
        console.print("[cyan]Step 1: Fixing empty titles...[/cyan]")
        
        # Check for the problematic .md file (empty filename)
        empty_file = self.tutorials_dir / ".md"
        files_to_process = []
        
        if empty_file.exists():
            files_to_process.append(empty_file)
        
        # Also check all files for empty titles in frontmatter
        for md_file in self.tutorials_dir.glob("*.md"):
            async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Check if title is empty in frontmatter
            if 'title: ""' in content or 'title: \'\'' in content:
                files_to_process.append(md_file)
        
        # Remove duplicates
        files_to_process = list(set(files_to_process))
        
        console.print(f"  Found {len(files_to_process)} files needing title repair")
        
        for md_file in files_to_process:
            await self.repair_title(md_file)
    
    async def repair_title(self, md_file: Path):
        """Repair the title for a single file."""
        async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        # Extract URL from frontmatter
        url_match = re.search(r'url:\s*"([^"]+)"', content)
        if not url_match:
            console.print(f"  [yellow]No URL found in {md_file.name}, skipping[/yellow]")
            return
        
        url = url_match.group(1)
        
        # Get new title from URL
        new_title = extract_title_from_url(url)
        
        # If still no good title, try content
        if new_title == "Untitled":
            content_title = extract_title_from_content(content)
            if content_title:
                new_title = content_title
        
        new_slug = slugify(new_title)
        new_filename = f"{new_slug}.md"
        new_file = self.tutorials_dir / new_filename
        
        # Update the content with new title
        # Fix frontmatter title
        content = re.sub(r'title:\s*""', f'title: "{new_title}"', content)
        content = re.sub(r"title:\s*''", f'title: "{new_title}"', content)
        
        # Fix the h1 heading if empty
        content = re.sub(r'^# \s*$', f'# {new_title}', content, flags=re.MULTILINE)
        
        # Check if target file already exists
        if new_file.exists() and new_file != md_file:
            # Merge or skip - for now, append a number
            counter = 1
            while new_file.exists():
                new_filename = f"{new_slug}-{counter}.md"
                new_file = self.tutorials_dir / new_filename
                counter += 1
        
        # Write the updated content
        async with aiofiles.open(new_file, 'w', encoding='utf-8') as f:
            await f.write(content)
        
        # Remove old file if different
        if md_file != new_file and md_file.exists():
            md_file.unlink()
            self.repairs_made['files_renamed'] += 1
        
        self.repairs_made['titles_fixed'] += 1
        console.print(f"  ✓ Fixed: {new_title}")
    
    async def fix_missing_images(self):
        """Download missing images and update markdown links."""
        console.print("\n[cyan]Step 2: Fixing missing images...[/cyan]")
        
        # Collect all images that need downloading
        all_images = {}  # url -> list of (file, alt_text)
        
        for md_file in self.tutorials_dir.glob("*.md"):
            async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            images = find_image_urls(content)
            for url, alt_text in images:
                if url not in all_images:
                    all_images[url] = []
                all_images[url].append((md_file, alt_text))
        
        console.print(f"  Found {len(all_images)} unique images to download")
        
        if not all_images:
            return
        
        # Download images
        async with aiohttp.ClientSession() as session:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                task = progress.add_task("Downloading images...", total=len(all_images))
                
                # Map of original URL -> local path
                url_to_local = {}
                
                for url in all_images:
                    # Generate local filename
                    parsed = urlparse(url if url.startswith('http') else f"https://drupalize.me{url}")
                    original_name = Path(unquote(parsed.path)).name
                    # Remove query string artifacts
                    original_name = re.sub(r'\?.*$', '', original_name)
                    
                    # Create unique filename
                    base_name = Path(original_name).stem
                    ext = Path(original_name).suffix or '.png'
                    
                    # Sanitize filename
                    base_name = re.sub(r'[^\w\-]', '-', base_name)
                    local_filename = f"{base_name}{ext}"
                    local_path = self.images_dir / local_filename
                    
                    # Handle duplicates
                    counter = 1
                    while local_path.exists():
                        local_filename = f"{base_name}-{counter}{ext}"
                        local_path = self.images_dir / local_filename
                        counter += 1
                    
                    # Download
                    success = await download_image(session, url, local_path)
                    
                    if success:
                        url_to_local[url] = f"../assets/images/{local_filename}"
                        self.repairs_made['images_downloaded'] += 1
                    
                    progress.advance(task)
                
                # Update all markdown files
                console.print("  Updating markdown files with local image paths...")
                
                files_updated = set()
                for url, local_path in url_to_local.items():
                    for md_file, _ in all_images[url]:
                        files_updated.add(md_file)
                
                for md_file in files_updated:
                    async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
                        content = await f.read()
                    
                    updated = False
                    for url, local_path in url_to_local.items():
                        if url in content:
                            content = content.replace(url, local_path)
                            updated = True
                            self.repairs_made['links_updated'] += 1
                    
                    if updated:
                        async with aiofiles.open(md_file, 'w', encoding='utf-8') as f:
                            await f.write(content)
    
    async def regenerate_index(self):
        """Regenerate the vault README with correct links."""
        console.print("\n[cyan]Step 3: Regenerating index...[/cyan]")
        
        # Collect all tutorials grouped by guide
        guides = {}
        
        for md_file in self.tutorials_dir.glob("*.md"):
            if md_file.name == '.md':
                continue  # Skip any remaining empty-named files
                
            async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Extract title
            title_match = re.search(r'title:\s*"([^"]*)"', content)
            title = title_match.group(1) if title_match else md_file.stem
            
            # Extract guide
            guide_match = re.search(r'guide:\s*"\[\[([^\]]+)\]\]"', content)
            guide = guide_match.group(1) if guide_match else "Uncategorized"
            
            if guide not in guides:
                guides[guide] = []
            
            guides[guide].append({
                'title': title,
                'slug': md_file.stem,
            })
        
        # Build the index content
        content_lines = [
            "# Drupalize.me Archive",
            "",
            "*Repaired vault with local images*",
            "",
            "## Guides",
            ""
        ]
        
        for guide_name in sorted(guides.keys()):
            guide_tutorials = guides[guide_name]
            guide_slug = slugify(guide_name)
            
            content_lines.append(f"### [[Guides/{guide_slug}|{guide_name}]]")
            content_lines.append("")
            
            # Sort tutorials by title
            guide_tutorials.sort(key=lambda t: t['title'].lower())
            
            for t in guide_tutorials[:5]:
                content_lines.append(f"- [[Tutorials/{t['slug']}|{t['title']}]]")
            
            if len(guide_tutorials) > 5:
                content_lines.append(f"- ... and {len(guide_tutorials) - 5} more")
            
            content_lines.append("")
        
        # Write the index
        index_file = self.vault_dir / "README.md"
        async with aiofiles.open(index_file, 'w', encoding='utf-8') as f:
            await f.write('\n'.join(content_lines))
        
        console.print(f"  ✓ Index regenerated with {sum(len(t) for t in guides.values())} tutorials in {len(guides)} guides")


@click.command()
@click.option(
    '--vault-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path('./vault'),
    help='Path to the vault directory (default: ./vault)'
)
def main(vault_dir: Path):
    """
    Repair issues in the Drupalize.me vault.
    
    Fixes empty titles and downloads missing images.
    """
    repairer = VaultRepairer(vault_dir)
    asyncio.run(repairer.repair_all())


if __name__ == '__main__':
    main()
