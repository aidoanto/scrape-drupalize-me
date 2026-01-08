"""Helper script to export cookies from your browser for use with the scraper.

This script helps you extract cookies from your browser where you're already logged in.
"""

import json
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def print_instructions():
    """Print instructions for exporting cookies."""
    instructions = """
[bold cyan]How to Export Cookies from Your Browser[/bold cyan]

[bold]Option 1: Using Browser Extension (Easiest)[/bold]

1. Install a cookie export extension:
   - Chrome/Edge: "Get cookies.txt LOCALLY" or "Cookie-Editor"
   - Firefox: "cookies.txt" extension

2. Go to https://drupalize.me and make sure you're logged in

3. Click the extension icon and export cookies

4. Save as JSON format (not Netscape format)

5. Use the exported file with: --cookies-file path/to/cookies.json

[bold]Option 2: Manual Export from Browser DevTools[/bold]

1. Open https://drupalize.me and log in

2. Open DevTools (F12)

3. Go to Application/Storage tab → Cookies → https://drupalize.me

4. Copy cookie values manually (tedious, not recommended)

[bold]Option 3: Use Playwright Browser (Recommended)[/bold]

1. Run the scraper with --no-headless
2. Log in manually in the Playwright browser window
3. Cookies will be saved automatically in ~/.drupalize_scraper
4. Future runs will use the saved session

[bold]After Exporting:[/bold]

Run the scraper with:
  uv run python main.py --cookies-file path/to/cookies.json
"""
    console.print(Panel(instructions, title="Cookie Export Instructions", border_style="cyan"))


def validate_cookies_file(cookies_file: Path) -> bool:
    """Validate that a cookies file is in the correct format."""
    if not cookies_file.exists():
        console.print(f"[red]Error: Cookies file not found: {cookies_file}[/red]")
        return False

    try:
        with open(cookies_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check if it's a list of cookies or a dict with cookies key
        if isinstance(data, list):
            cookies = data
        elif isinstance(data, dict) and "cookies" in data:
            cookies = data["cookies"]
        else:
            cookies = [data]

        # Validate cookie structure
        required_fields = ["name", "value", "domain"]
        for cookie in cookies:
            if not all(field in cookie for field in required_fields):
                console.print("[red]Error: Invalid cookie format. Each cookie must have 'name', 'value', and 'domain'[/red]")
                return False

        console.print(f"[green]✓ Valid cookies file with {len(cookies)} cookies[/green]")
        return True

    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON file: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return False


if __name__ == "__main__":
    console.print("[bold cyan]Drupalize.me Cookie Export Helper[/bold cyan]\n")

    if len(sys.argv) > 1:
        cookies_file = Path(sys.argv[1])
        validate_cookies_file(cookies_file)
    else:
        print_instructions()
