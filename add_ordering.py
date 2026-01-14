"""
Add ordering information to vault tutorials.

Reads the original extraction batch files to determine tutorial order within guides,
then updates the vault files with order metadata and regenerates the index.

Usage:
    uv run python add_ordering.py --extracted-dir ./extracted --vault-dir ./vault
"""

import asyncio
import json
import re
from pathlib import Path
from collections import defaultdict

import aiofiles
import click
from rich.console import Console

console = Console()


def slugify(text: str) -> str:
    """Convert text to a valid filename slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def slug_to_title(slug: str) -> str:
    """Convert a URL slug to a readable title."""
    slug = re.sub(r'free$', '', slug)
    title = slug.replace('-', ' ').title()
    replacements = {
        'Api': 'API', 'Css': 'CSS', 'Html': 'HTML', 'Php': 'PHP',
        'Sql': 'SQL', 'Ui': 'UI', 'Url': 'URL', 'Json': 'JSON',
        'Xml': 'XML', 'Ddev': 'DDEV', 'Drupal S': "Drupal's",
        'Oauth': 'OAuth', 'Jsonapi': 'JSON:API', 'Graphql': 'GraphQL',
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title


def extract_title_from_url(url: str) -> str:
    """Extract a title from a tutorial URL."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path = parsed.path
    parts = [p for p in path.split('/') if p and p != 'tutorial']
    if parts:
        slug = parts[-1]
        return slug_to_title(slug)
    return "Untitled"


async def main(extracted_dir: Path, vault_dir: Path):
    """Add ordering to vault tutorials."""
    console.print("[bold cyan]Adding tutorial ordering...[/bold cyan]\n")
    
    tutorials_dir = vault_dir / "Tutorials"
    guides_dir = vault_dir / "Guides"
    
    # Step 1: Build order map from extracted data
    console.print("[cyan]Step 1: Reading extraction order from batch files...[/cyan]")
    
    # Map: guide_slug -> [(order, url, title), ...]
    guide_orders = defaultdict(list)
    
    batch_files = sorted(extracted_dir.glob("drupalize_content_batch_*.json"))
    
    for batch_file in batch_files:
        with open(batch_file) as f:
            data = json.load(f)
        
        for tutorial in data.get('tutorials', []):
            guide = tutorial.get('guide', 'uncategorized')
            url = tutorial.get('url', '')
            title = tutorial.get('title', '')
            
            # If title is empty, extract from URL
            if not title.strip():
                title = extract_title_from_url(url)
            
            guide_orders[guide].append({
                'url': url,
                'title': title,
                'slug': slugify(title),
            })
    
    # The order in the list IS the order from the guide
    # Add explicit order numbers
    for guide, tutorials in guide_orders.items():
        for i, t in enumerate(tutorials):
            t['order'] = i + 1
    
    console.print(f"  Found {len(guide_orders)} guides with ordering info")
    
    # Step 2: Update vault files with order in frontmatter
    console.print("\n[cyan]Step 2: Updating tutorial frontmatter with order...[/cyan]")
    
    updated_count = 0
    order_lookup = {}  # slug -> (guide, order)
    
    for guide, tutorials in guide_orders.items():
        for t in tutorials:
            order_lookup[t['slug']] = (guide, t['order'], t['title'])
    
    for md_file in tutorials_dir.glob("*.md"):
        slug = md_file.stem
        
        if slug not in order_lookup:
            continue
        
        guide, order, title = order_lookup[slug]
        
        async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        # Check if order already exists
        if 'order:' in content:
            continue
        
        # Add order to frontmatter (after the opening ---)
        lines = content.split('\n')
        new_lines = []
        in_frontmatter = False
        added_order = False
        
        for line in lines:
            new_lines.append(line)
            if line.strip() == '---' and not in_frontmatter:
                in_frontmatter = True
            elif line.strip() == '---' and in_frontmatter and not added_order:
                # Insert order before closing ---
                new_lines.insert(-1, f'order: {order}')
                added_order = True
        
        if added_order:
            async with aiofiles.open(md_file, 'w', encoding='utf-8') as f:
                await f.write('\n'.join(new_lines))
            updated_count += 1
    
    console.print(f"  Updated {updated_count} tutorial files with order")
    
    # Step 3: Regenerate guide files with ordered tutorials
    console.print("\n[cyan]Step 3: Regenerating guide index files...[/cyan]")
    
    for guide_slug, tutorials in guide_orders.items():
        guide_file = guides_dir / f"{guide_slug}.md"
        
        # Sort tutorials by their order
        sorted_tutorials = sorted(tutorials, key=lambda t: t['order'])
        
        # Try to get a nice title
        guide_title = slug_to_title(guide_slug)
        
        content_lines = [
            "---",
            f'title: "{guide_title}"',
            "type: guide",
            "---",
            "",
            f"# {guide_title}",
            "",
            "## Tutorials",
            "",
        ]
        
        for t in sorted_tutorials:
            content_lines.append(f"{t['order']}. [[Tutorials/{t['slug']}|{t['title']}]]")
        
        async with aiofiles.open(guide_file, 'w', encoding='utf-8') as f:
            await f.write('\n'.join(content_lines))
    
    console.print(f"  Regenerated {len(guide_orders)} guide files")
    
    # Step 4: Regenerate main README with ordered tutorials
    console.print("\n[cyan]Step 4: Regenerating main index...[/cyan]")
    
    content_lines = [
        "# Drupalize.me Archive",
        "",
        "*Tutorials ordered as they appear in each guide*",
        "",
        "## Guides",
        ""
    ]
    
    for guide_slug in sorted(guide_orders.keys()):
        tutorials = guide_orders[guide_slug]
        sorted_tutorials = sorted(tutorials, key=lambda t: t['order'])
        guide_title = slug_to_title(guide_slug)
        
        content_lines.append(f"### [[Guides/{guide_slug}|{guide_title}]]")
        content_lines.append("")
        
        # Show first 5 in order
        for t in sorted_tutorials[:5]:
            content_lines.append(f"{t['order']}. [[Tutorials/{t['slug']}|{t['title']}]]")
        
        if len(sorted_tutorials) > 5:
            content_lines.append(f"- ... and {len(sorted_tutorials) - 5} more")
        
        content_lines.append("")
    
    readme_file = vault_dir / "README.md"
    async with aiofiles.open(readme_file, 'w', encoding='utf-8') as f:
        await f.write('\n'.join(content_lines))
    
    console.print("\n[bold green]✅ Ordering complete![/bold green]")
    console.print(f"  - {len(guide_orders)} guides with ordered tutorials")
    console.print(f"  - {updated_count} tutorials updated with order metadata")


@click.command()
@click.option(
    '--extracted-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path('./extracted'),
    help='Directory containing extracted JSON files'
)
@click.option(
    '--vault-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path('./vault'),
    help='Path to the vault directory'
)
def cli(extracted_dir: Path, vault_dir: Path):
    """Add ordering information to vault tutorials."""
    asyncio.run(main(extracted_dir, vault_dir))


if __name__ == '__main__':
    cli()
