"""
Browser-based scraper that works with the Cursor browser tool.

This script parses the browser snapshot log files created by the Cursor browser
tool to extract content from Drupalize.me.

Usage:
1. Use the Cursor browser tool to navigate to pages
2. Snapshots are saved to C:\Users\<user>\.cursor\browser-logs\
3. This script reads those snapshots from /mnt/c/Users/<user>/.cursor/browser-logs/
4. Run: uv run python browser_scraper.py --snapshot-dir /mnt/c/Users/aidanmolins/.cursor/browser-logs
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

import click
from rich.console import Console

console = Console()


def parse_snapshot_yaml(content: str) -> dict:
    """Parse the YAML-like snapshot format into a more usable structure."""
    lines = content.strip().split('\n')
    
    # Extract text content from the snapshot
    text_content = []
    links = []
    
    for line in lines:
        # Extract names (visible text)
        if 'name:' in line:
            match = re.search(r'name:\s*(.+)$', line)
            if match:
                name = match.group(1).strip()
                # Clean up the name (remove quotes if present)
                if name.startswith('"') and name.endswith('"'):
                    name = name[1:-1]
                if name and len(name) > 1:
                    text_content.append(name)
        
        # Extract link references
        if 'role: link' in line:
            links.append(True)
    
    return {
        'text_content': text_content,
        'has_links': len(links) > 0,
    }


def extract_guide_names_from_snapshot(snapshot_path: Path) -> list:
    """Extract guide names from a snapshot file."""
    content = snapshot_path.read_text(encoding='utf-8')
    
    guides = []
    
    # Look for heading patterns followed by link patterns with guide names
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if 'role: heading' in line:
            # Look for the name in the next few lines
            for j in range(i, min(i + 5, len(lines))):
                if 'name:' in lines[j]:
                    match = re.search(r'name:\s*(.+)$', lines[j])
                    if match:
                        name = match.group(1).strip()
                        if name and len(name) > 3 and name not in ['Main navigation', 'Footer menu', 'Guide', 'Search']:
                            guides.append(name)
                    break
    
    return list(set(guides))  # Remove duplicates


def extract_tutorial_content_from_snapshot(snapshot_path: Path) -> dict:
    """Extract tutorial content from a snapshot file."""
    content = snapshot_path.read_text(encoding='utf-8')
    
    # Extract all text content
    text_parts = []
    current_section = None
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if 'name:' in line:
            match = re.search(r'name:\s*(.+)$', line)
            if match:
                name = match.group(1).strip()
                if name.startswith('"') and name.endswith('"'):
                    name = name[1:-1]
                if name and len(name) > 1:
                    text_parts.append(name)
    
    return {
        'content': '\n'.join(text_parts),
        'raw_lines': lines,
    }


@click.command()
@click.option(
    '--snapshot-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path('/mnt/c/Users/aidanmolins/.cursor/browser-logs'),
    help='Directory containing browser snapshot log files',
)
@click.option(
    '--output-dir',
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=Path('./vault'),
    help='Output directory for scraped content',
)
def main(snapshot_dir: Path, output_dir: Path):
    """Process browser snapshots to extract Drupalize.me content."""
    
    console.print(f"[cyan]Snapshot directory:[/cyan] {snapshot_dir}")
    console.print(f"[cyan]Output directory:[/cyan] {output_dir}")
    
    # Find all snapshot files
    snapshot_files = sorted(snapshot_dir.glob('snapshot-*.log'), key=lambda p: p.stat().st_mtime, reverse=True)
    
    if not snapshot_files:
        console.print("[red]No snapshot files found![/red]")
        return
    
    console.print(f"\n[green]Found {len(snapshot_files)} snapshot files[/green]")
    
    # Process the most recent snapshot
    latest = snapshot_files[0]
    console.print(f"\n[yellow]Processing latest snapshot:[/yellow] {latest.name}")
    
    # Try to extract guide names
    guides = extract_guide_names_from_snapshot(latest)
    
    if guides:
        console.print(f"\n[green]Found guides/content:[/green]")
        for guide in guides:
            console.print(f"  - {guide}")
    
    # Extract general content
    content = extract_tutorial_content_from_snapshot(latest)
    
    # Save to output
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    output_file.write_text(content['content'], encoding='utf-8')
    
    console.print(f"\n[green]Saved content to:[/green] {output_file}")


if __name__ == '__main__':
    main()
