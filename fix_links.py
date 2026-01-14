"""
Fix broken links by mapping URLs to actual files.

The issue: slugs generated from URLs don't always match actual filenames.
Solution: Read actual files, extract their URLs, and build a proper mapping.

Usage:
    uv run python fix_links.py --vault-dir ./vault --extracted-dir ./extracted
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
        'Xml': 'XML', 'Ddev': 'DDEV', "Drupal'S": "Drupal's",
        'Oauth': 'OAuth', 'Jsonapi': 'JSON:API', 'Graphql': 'GraphQL',
        "Drupal'Site": "Drupal Site", "Drupal'Sites": "Drupal Sites",
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title


async def main(vault_dir: Path, extracted_dir: Path):
    """Fix broken links in the vault."""
    console.print("[bold cyan]Fixing broken links...[/bold cyan]\n")
    
    tutorials_dir = vault_dir / "Tutorials"
    guides_dir = vault_dir / "Guides"
    
    # Step 1: Build URL -> actual filename mapping from existing files
    console.print("[cyan]Step 1: Building URL to filename mapping...[/cyan]")
    
    url_to_file = {}
    file_to_title = {}
    
    for md_file in tutorials_dir.glob("*.md"):
        async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        # Extract URL from frontmatter
        url_match = re.search(r'url:\s*"([^"]+)"', content)
        if url_match:
            url = url_match.group(1)
            url_to_file[url] = md_file.stem
        
        # Extract title
        title_match = re.search(r'title:\s*"([^"]*)"', content)
        if title_match and title_match.group(1):
            file_to_title[md_file.stem] = title_match.group(1)
        else:
            file_to_title[md_file.stem] = slug_to_title(md_file.stem)
    
    console.print(f"  Found {len(url_to_file)} files with URLs")
    
    # Step 2: Build guide -> ordered tutorials mapping from batch files
    console.print("\n[cyan]Step 2: Reading tutorial order from batch files...[/cyan]")
    
    guide_tutorials = defaultdict(list)
    
    batch_files = sorted(extracted_dir.glob("drupalize_content_batch_*.json"))
    
    for batch_file in batch_files:
        with open(batch_file) as f:
            data = json.load(f)
        
        for tutorial in data.get('tutorials', []):
            guide = tutorial.get('guide', 'uncategorized')
            url = tutorial.get('url', '')
            
            # Find actual filename for this URL
            actual_slug = url_to_file.get(url)
            
            if actual_slug:
                title = file_to_title.get(actual_slug, slug_to_title(actual_slug))
                guide_tutorials[guide].append({
                    'slug': actual_slug,
                    'title': title,
                    'url': url,
                })
    
    # Add order numbers
    for guide, tutorials in guide_tutorials.items():
        for i, t in enumerate(tutorials):
            t['order'] = i + 1
    
    console.print(f"  Mapped {sum(len(t) for t in guide_tutorials.values())} tutorials across {len(guide_tutorials)} guides")
    
    # Step 3: Regenerate guide files with correct links
    console.print("\n[cyan]Step 3: Regenerating guide files with correct links...[/cyan]")
    
    for guide_slug, tutorials in guide_tutorials.items():
        guide_file = guides_dir / f"{guide_slug}.md"
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
        
        for t in tutorials:
            content_lines.append(f"{t['order']}. [[Tutorials/{t['slug']}|{t['title']}]]")
        
        async with aiofiles.open(guide_file, 'w', encoding='utf-8') as f:
            await f.write('\n'.join(content_lines))
    
    console.print(f"  Regenerated {len(guide_tutorials)} guide files")
    
    # Step 4: Regenerate main README
    console.print("\n[cyan]Step 4: Regenerating main README...[/cyan]")
    
    content_lines = [
        "# Drupalize.me Archive",
        "",
        "*Tutorials in learning order with working links*",
        "",
        "## Guides",
        ""
    ]
    
    for guide_slug in sorted(guide_tutorials.keys()):
        tutorials = guide_tutorials[guide_slug]
        guide_title = slug_to_title(guide_slug)
        
        content_lines.append(f"### [[Guides/{guide_slug}|{guide_title}]]")
        content_lines.append("")
        
        for t in tutorials[:5]:
            content_lines.append(f"{t['order']}. [[Tutorials/{t['slug']}|{t['title']}]]")
        
        if len(tutorials) > 5:
            content_lines.append(f"- ... and {len(tutorials) - 5} more")
        
        content_lines.append("")
    
    readme_file = vault_dir / "README.md"
    async with aiofiles.open(readme_file, 'w', encoding='utf-8') as f:
        await f.write('\n'.join(content_lines))
    
    # Step 5: Verify no broken links
    console.print("\n[cyan]Step 5: Verifying links...[/cyan]")
    
    actual_files = {f.stem for f in tutorials_dir.glob('*.md')}
    broken = 0
    
    for guide_file in guides_dir.glob('*.md'):
        async with aiofiles.open(guide_file, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        for match in re.finditer(r'\[\[Tutorials/([^\]|]+)', content):
            slug = match.group(1)
            if slug not in actual_files:
                broken += 1
    
    if broken == 0:
        console.print("  [green]✓ All links verified![/green]")
    else:
        console.print(f"  [yellow]Warning: {broken} broken links remain[/yellow]")
    
    console.print("\n[bold green]✅ Links fixed![/bold green]")


@click.command()
@click.option(
    '--vault-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path('./vault'),
    help='Path to the vault directory'
)
@click.option(
    '--extracted-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path('./extracted'),
    help='Directory containing extracted JSON files'
)
def cli(vault_dir: Path, extracted_dir: Path):
    """Fix broken links in vault by mapping URLs to actual files."""
    asyncio.run(main(vault_dir, extracted_dir))


if __name__ == '__main__':
    cli()
