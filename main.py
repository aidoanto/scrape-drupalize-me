"""Main entry point for Drupalize.me scraper."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from scraper.scraper import DrupalizeScraper


@click.command()
@click.option(
    "--vault-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=Path("vault"),
    help="Directory for the Obsidian vault (default: ./vault)",
)
@click.option(
    "--headless/--no-headless",
    default=True,
    help="Run browser in headless mode (default: True)",
)
@click.option(
    "--delay",
    type=float,
    default=2.5,
    help="Delay between requests in seconds (default: 2.5)",
)
@click.option(
    "--base-url",
    default="https://drupalize.me",
    help="Base URL of Drupalize.me (default: https://drupalize.me)",
)
@click.option(
    "--cookies-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    default=None,
    help="Path to JSON file with cookies to import (export from your browser)",
)
@click.option(
    "--cdp-url",
    default=None,
    help="Connect to existing Chrome via CDP (e.g., http://localhost:9222). Start Chrome first with --remote-debugging-port=9222",
)
def main(vault_dir: Path, headless: bool, delay: float, base_url: str, cookies_file: Optional[Path], cdp_url: Optional[str]):
    """
    Scrape Drupalize.me content into an Obsidian vault.

    This scraper will:
    - Extract all guides and tutorials
    - Download images and videos locally
    - Convert content to Obsidian-compatible Markdown
    - Track progress to allow resuming if interrupted

    Make sure you're logged into Drupalize.me in your browser before running.
    The scraper will use your existing browser session.
    """
    console = Console()

    console.print("[bold cyan]Drupalize.me Scraper[/bold cyan]")
    console.print(f"Vault directory: {vault_dir.absolute()}")
    console.print(f"Headless mode: {headless}")
    console.print(f"Delay: {delay}s")
    console.print("")

    # Check if vault directory exists and warn if it has content
    if vault_dir.exists() and any(vault_dir.iterdir()):
        console.print(
            "[yellow]Warning: Vault directory already exists and contains files.[/yellow]"
        )
        console.print(
            "[yellow]Existing files will be preserved, but new files may overwrite existing ones.[/yellow]"
        )
        if not click.confirm("Continue?"):
            console.print("[red]Aborted.[/red]")
            sys.exit(1)

    try:
        scraper = DrupalizeScraper(
            vault_root=vault_dir,
            base_url=base_url,
            delay=delay,
            headless=headless,
            cookies_file=cookies_file,
            cdp_url=cdp_url,
        )

        console.print("[green]Starting scraper...[/green]")
        console.print("")

        # Run the scraper
        asyncio.run(scraper.scrape_all())

        console.print("")
        console.print("[bold green]Scraping completed![/bold green]")
        console.print(f"Vault created at: {vault_dir.absolute()}")

    except KeyboardInterrupt:
        console.print("")
        console.print("[yellow]Scraping interrupted by user.[/yellow]")
        console.print("[yellow]Progress has been saved. Run again to resume.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print("")
        console.print(f"[red]Error: {e}[/red]")
        import traceback

        console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
