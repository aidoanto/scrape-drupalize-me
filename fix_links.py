"""
Fix broken links by mapping URLs to actual files.

The issue: slugs generated from URLs don't always match actual filenames.
Solution: Read actual files, extract their URLs, and build a proper mapping.

Also rebuilds guide/tutorial ordering based on `drupalize_urls.json` (URL-only data),
since extraction batch order does not match guide order.

Usage:
    uv run python fix_links.py --vault-dir ./vault --urls-file ./drupalize_urls.json
"""

import asyncio
import json
import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

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

    # Fix common acronyms using word boundaries.
    # Note: we keep this intentionally small to avoid weird transformations.
    acronyms = {
        "Api": "API",
        "Css": "CSS",
        "Html": "HTML",
        "Php": "PHP",
        "Sql": "SQL",
        "Ui": "UI",
        "Url": "URL",
        "Json": "JSON",
        "Xml": "XML",
        "Ddev": "DDEV",
        "Oauth": "OAuth",
        "Graphql": "GraphQL",
    }
    for old, new in acronyms.items():
        title = re.sub(rf"\b{re.escape(old)}\b", new, title)
    return title


def _normalize_url_to_path(url: str) -> str:
    """Normalize a URL (or relative path) to just its path."""
    if not url:
        return ""
    parsed = urlparse(url)
    return parsed.path


async def _set_tutorial_order(
    tutorials_dir: Path,
    order_by_guide_and_slug: dict[tuple[str, str], int],
):
    """Upsert `order:` in tutorial frontmatter based on (guide, slug) mapping.

    This avoids writing a single ambiguous `order` for tutorials that might appear
    in multiple guides.
    """
    updated = 0
    for md_file in tutorials_dir.glob("*.md"):
        async with aiofiles.open(md_file, "r", encoding="utf-8") as f:
            content = await f.read()

        if not content.startswith("---"):
            continue

        guide_match = re.search(r'guide:\s*"\[\[([^\]]+)\]\]"', content)
        guide_slug = guide_match.group(1) if guide_match else ""
        order = order_by_guide_and_slug.get((guide_slug, md_file.stem))
        if order is None:
            continue

        # Replace existing order if present, else insert before closing frontmatter.
        if re.search(r"(?m)^order:\s*\d+\s*$", content):
            new_content = re.sub(r"(?m)^order:\s*\d+\s*$", f"order: {order}", content)
        else:
            parts = content.split("---", 2)
            if len(parts) < 3:
                continue
            frontmatter = parts[1]
            body = parts[2]
            frontmatter = frontmatter.rstrip("\n") + f"\norder: {order}\n"
            new_content = "---" + frontmatter + "---" + body

        if new_content != content:
            async with aiofiles.open(md_file, "w", encoding="utf-8") as f:
                await f.write(new_content)
            updated += 1

    return updated


async def main(vault_dir: Path, urls_file: Path):
    """Fix broken links in the vault."""
    console.print("[bold cyan]Fixing links + rebuilding correct guide order...[/bold cyan]\n")
    
    tutorials_dir = vault_dir / "Tutorials"
    guides_dir = vault_dir / "Guides"
    
    # Step 1: Build URL -> filename mapping from existing files
    console.print("[cyan]Step 1: Building URL to filename mapping...[/cyan]")
    
    url_to_file: dict[str, str] = {}
    path_to_files: dict[str, list[str]] = defaultdict(list)
    file_to_title = {}
    file_to_guide = {}
    
    for md_file in tutorials_dir.glob("*.md"):
        async with aiofiles.open(md_file, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        # Extract URL from frontmatter
        url_match = re.search(r'url:\s*"([^"]+)"', content)
        if url_match:
            url = url_match.group(1).strip()
            path = _normalize_url_to_path(url)
            if url:
                url_to_file[url] = md_file.stem
            if path:
                path_to_files[path].append(md_file.stem)
        
        # Extract title
        title_match = re.search(r'title:\s*"([^"]*)"', content)
        if title_match and title_match.group(1):
            file_to_title[md_file.stem] = title_match.group(1)
        else:
            file_to_title[md_file.stem] = slug_to_title(md_file.stem)

        guide_match = re.search(r'guide:\s*"\[\[([^\]]+)\]\]"', content)
        if guide_match:
            file_to_guide[md_file.stem] = guide_match.group(1)
    
    console.print(f"  Found {len(url_to_file)} files with URLs")
    
    # Step 2: Read guide ordering from drupalize_urls.json (URL-only)
    console.print("\n[cyan]Step 2: Reading guide ordering from drupalize_urls.json...[/cyan]")
    
    guide_tutorials = defaultdict(list)

    urls_data = json.loads(urls_file.read_text(encoding="utf-8"))
    guides = urls_data.get("guides", [])

    # Build guide -> list of tutorial slugs in the order shown on the guide page.
    def resolve_tutorial_slug(guide_slug: str, tutorial_url: str) -> str | None:
        """Resolve a guide tutorial URL to an actual vault file slug."""
        tutorial_url = (tutorial_url or "").strip()
        if not tutorial_url:
            return None

        # Prefer exact URL match (keeps ?p= distinctions).
        if tutorial_url in url_to_file:
            return url_to_file[tutorial_url]

        # Fallback: match by path, then disambiguate.
        t_path = _normalize_url_to_path(tutorial_url)
        candidates = path_to_files.get(t_path, [])
        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0]

        # Prefer candidate whose declared guide matches.
        guide_matched = [c for c in candidates if file_to_guide.get(c) == guide_slug]
        if len(guide_matched) == 1:
            return guide_matched[0]

        # Prefer any candidate whose stored URL contains a ?p= (more specific).
        # Build reverse map just for this path.
        for cand in candidates:
            # Find a stored URL for this candidate
            # (url_to_file is url->slug; invert on the fly for candidates only)
            for u, s in url_to_file.items():
                if s == cand and _normalize_url_to_path(u) == t_path and "?p=" in u:
                    return cand

        # Otherwise, just pick the first deterministically.
        return sorted(candidates)[0]

    for g in guides:
        guide_slug = (g.get("title") or "").strip() or slugify(g.get("url", "").split("/")[-1])
        seen_slugs = set()

        for t in g.get("tutorials", []):
            t_url = (t.get("url") or "").strip()
            actual_slug = resolve_tutorial_slug(guide_slug, t_url)
            if actual_slug is None:
                continue
            if actual_slug in seen_slugs:
                continue
            seen_slugs.add(actual_slug)

            title = file_to_title.get(actual_slug, slug_to_title(actual_slug))
            guide_tutorials[guide_slug].append({"slug": actual_slug, "title": title})

    # Add order numbers based on their position in each guide list.
    order_by_guide_and_slug: dict[tuple[str, str], int] = {}
    for guide_slug, tutorials in guide_tutorials.items():
        for i, t in enumerate(tutorials, start=1):
            t["order"] = i
            order_by_guide_and_slug[(guide_slug, t["slug"])] = i

    console.print(
        f"  Mapped {sum(len(t) for t in guide_tutorials.values())} tutorials across {len(guide_tutorials)} guides"
    )

    # Step 3: Update tutorial `order:` frontmatter to match guide ordering
    console.print("\n[cyan]Step 3: Updating tutorial frontmatter order...[/cyan]")
    updated = await _set_tutorial_order(tutorials_dir, order_by_guide_and_slug)
    console.print(f"  Updated {updated} tutorial files with order")
    
    # Step 4: Regenerate guide files with correct links + correct ordering
    console.print("\n[cyan]Step 4: Regenerating guide files with correct links...[/cyan]")
    
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
    
    # Step 5: Regenerate main README
    console.print("\n[cyan]Step 5: Regenerating main README...[/cyan]")
    
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
    
    # Step 6: Verify no broken links
    console.print("\n[cyan]Step 6: Verifying links...[/cyan]")
    
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
    '--urls-file',
    type=click.Path(exists=True, dir_okay=False, file_okay=True, path_type=Path),
    default=Path('./drupalize_urls.json'),
    help='Path to drupalize_urls.json (URL-only, guide ordering source)'
)
def cli(vault_dir: Path, urls_file: Path):
    """Fix broken links and rebuild guide ordering from drupalize_urls.json."""
    asyncio.run(main(vault_dir, urls_file))


if __name__ == '__main__':
    cli()
