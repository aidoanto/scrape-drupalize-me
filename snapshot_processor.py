"""
Process Cursor browser snapshots into Obsidian markdown.

This script reads the accessibility tree snapshots created by the Cursor browser
and extracts tutorial content into markdown files.

Usage:
    uv run python snapshot_processor.py --snapshot-dir /mnt/c/Users/<user>/.cursor/browser-logs --vault-dir ./vault
"""

import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

import click
from rich.console import Console
from rich.progress import Progress

console = Console()


def parse_snapshot_yaml(content: str) -> Dict[str, Any]:
    """Parse the YAML-like accessibility tree snapshot."""
    try:
        # The snapshot is valid YAML
        return yaml.safe_load(content)
    except yaml.YAMLError:
        # Fallback to line-by-line parsing
        return {"raw": content}


def extract_text_from_node(node: Any, depth: int = 0) -> List[str]:
    """Recursively extract text content from accessibility tree nodes."""
    texts = []
    
    if isinstance(node, dict):
        # Get the name/text of this node
        name = node.get('name', '')
        role = node.get('role', '')
        
        # Skip navigation, footer, and other non-content elements
        skip_roles = {'navigation', 'banner', 'contentinfo', 'button', 'textbox', 'radio', 'form'}
        skip_names = {'Main navigation', 'Footer menu', 'Toggle menu', 'Toggle Chat', 'Search', 'Skip to main content'}
        
        if role in skip_roles or name in skip_names:
            return texts
        
        if name and len(name) > 2:
            # Clean up the text (remove extra spaces)
            name = ' '.join(name.split())
            
            # Format based on role
            if role == 'heading':
                level = 2  # Default heading level
                texts.append(f"\n{'#' * level} {name}\n")
            elif role == 'listitem':
                texts.append(f"- {name}")
            elif role == 'link' and depth > 3:  # Only include deep links as inline
                texts.append(f"[{name}]")
            elif role == 'generic' or role == '':
                texts.append(name)
        
        # Process children
        children = node.get('children', [])
        for child in children:
            texts.extend(extract_text_from_node(child, depth + 1))
    
    elif isinstance(node, list):
        for item in node:
            texts.extend(extract_text_from_node(item, depth))
    
    return texts


def extract_metadata_from_snapshot(content: str) -> Dict[str, str]:
    """Extract page URL and title from snapshot patterns."""
    metadata = {
        'url': '',
        'title': '',
        'drupal_versions': []
    }
    
    # Look for URL patterns in the raw content
    url_match = re.search(r'name:\s*"?(https://drupalize\.me/[^"\s]+)"?', content)
    if url_match:
        metadata['url'] = url_match.group(1)
    
    # Look for Drupal version mentions
    for version in ['Drupal 11', 'Drupal 10', 'Drupal 9', 'Drupal 8', 'Drupal 7']:
        if version in content:
            metadata['drupal_versions'].append(version)
    
    return metadata


def slugify(text: str) -> str:
    """Convert text to a valid filename slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:100]


def snapshot_to_markdown(snapshot_path: Path) -> Optional[Dict[str, str]]:
    """Convert a snapshot file to markdown content."""
    content = snapshot_path.read_text(encoding='utf-8')
    
    # Parse the YAML
    try:
        tree = yaml.safe_load(content)
    except yaml.YAMLError as e:
        console.print(f"[yellow]Warning: Could not parse {snapshot_path.name}: {e}[/yellow]")
        return None
    
    # Extract text content
    texts = extract_text_from_node(tree)
    
    if not texts:
        return None
    
    # Get metadata
    metadata = extract_metadata_from_snapshot(content)
    
    # Find the title (first substantial heading)
    title = "Untitled"
    for text in texts[:10]:
        if text.startswith('#'):
            title = text.strip('#').strip()
            break
        elif len(text) > 10 and not text.startswith('-') and not text.startswith('['):
            title = text[:100]
            break
    
    # Build markdown
    md_parts = [
        "---",
        f'title: "{title}"',
        f'url: "{metadata["url"]}"',
        f'extracted: "{datetime.now().isoformat()}"',
    ]
    
    if metadata['drupal_versions']:
        md_parts.append("drupal_versions:")
        for v in metadata['drupal_versions']:
            md_parts.append(f'  - "{v}"')
    
    md_parts.extend([
        "---",
        "",
        f"# {title}",
        ""
    ])
    
    # Add content, avoiding duplicates
    seen = set()
    for text in texts:
        if text not in seen and len(text) > 2:
            seen.add(text)
            md_parts.append(text)
    
    return {
        'title': title,
        'slug': slugify(title),
        'content': '\n'.join(md_parts),
        'url': metadata['url']
    }


def identify_page_type(content: str) -> str:
    """Identify if a snapshot is a guide, tutorial, or search page."""
    if '/guide/' in content and '/tutorial/' not in content:
        return 'guide'
    elif '/tutorial/' in content:
        return 'tutorial'
    elif '/search' in content:
        return 'search'
    else:
        return 'other'


@click.command()
@click.option(
    '--snapshot-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=True,
    help='Directory containing browser snapshot files (e.g., /mnt/c/Users/<user>/.cursor/browser-logs)',
)
@click.option(
    '--vault-dir',
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=Path('./vault'),
    help='Output directory for Obsidian vault (default: ./vault)',
)
@click.option(
    '--process-all/--latest-only',
    default=False,
    help='Process all snapshots or just the most recent ones (default: latest only)',
)
def main(snapshot_dir: Path, vault_dir: Path, process_all: bool):
    """
    Process Cursor browser snapshots into an Obsidian vault.
    
    Use the Cursor browser to navigate Drupalize.me pages, then run this
    script to convert the snapshots into markdown files.
    """
    console.print("[bold cyan]Drupalize.me Snapshot Processor[/bold cyan]")
    console.print(f"Snapshot directory: {snapshot_dir}")
    console.print(f"Vault directory: {vault_dir}")
    console.print(f"Mode: {'All snapshots' if process_all else 'Latest snapshots only'}")
    console.print("")
    
    # Create vault structure
    guides_dir = vault_dir / "Guides"
    tutorials_dir = vault_dir / "Tutorials"
    guides_dir.mkdir(parents=True, exist_ok=True)
    tutorials_dir.mkdir(parents=True, exist_ok=True)
    
    # Find snapshot files
    snapshot_files = sorted(
        snapshot_dir.glob('snapshot-*.log'),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    if not snapshot_files:
        console.print("[red]No snapshot files found![/red]")
        console.print("Use the Cursor browser to navigate Drupalize.me pages first.")
        return
    
    console.print(f"[green]Found {len(snapshot_files)} snapshot files[/green]")
    
    if not process_all:
        # Keep only unique URLs (most recent for each)
        seen_urls = set()
        unique_snapshots = []
        for sf in snapshot_files:
            content = sf.read_text(encoding='utf-8')
            url_match = re.search(r'drupalize\.me/(tutorial|guide)/[^\s"]+', content)
            if url_match:
                url = url_match.group(0)
                if url not in seen_urls:
                    seen_urls.add(url)
                    unique_snapshots.append(sf)
        snapshot_files = unique_snapshots
        console.print(f"[green]Processing {len(snapshot_files)} unique pages[/green]")
    
    # Process snapshots
    processed = {'guides': 0, 'tutorials': 0, 'skipped': 0}
    
    with Progress(console=console) as progress:
        task = progress.add_task("Processing snapshots...", total=len(snapshot_files))
        
        for snapshot_path in snapshot_files:
            content = snapshot_path.read_text(encoding='utf-8')
            page_type = identify_page_type(content)
            
            if page_type == 'search':
                progress.advance(task)
                processed['skipped'] += 1
                continue
            
            result = snapshot_to_markdown(snapshot_path)
            
            if result:
                if page_type == 'guide':
                    output_path = guides_dir / f"{result['slug']}.md"
                    processed['guides'] += 1
                else:
                    output_path = tutorials_dir / f"{result['slug']}.md"
                    processed['tutorials'] += 1
                
                output_path.write_text(result['content'], encoding='utf-8')
            else:
                processed['skipped'] += 1
            
            progress.advance(task)
    
    console.print("")
    console.print(f"[bold green]✅ Processing complete![/bold green]")
    console.print(f"   Guides: {processed['guides']}")
    console.print(f"   Tutorials: {processed['tutorials']}")
    console.print(f"   Skipped: {processed['skipped']}")
    console.print(f"   Vault: {vault_dir.absolute()}")


if __name__ == '__main__':
    main()
