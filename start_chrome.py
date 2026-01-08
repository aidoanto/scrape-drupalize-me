#!/usr/bin/env python3
"""
Helper script to start Chrome with remote debugging enabled.

This allows the scraper to connect to your real Chrome browser where you're 
already logged into Drupalize.me, bypassing Cloudflare detection.

Usage:
    1. Run this script: python start_chrome.py
    2. In the Chrome window that opens, go to drupalize.me and log in
    3. Keep Chrome open, then run the scraper in another terminal:
       uv run python main.py --cdp-url http://localhost:9222 --vault-dir ./vault
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def get_chrome_paths():
    """Get possible Chrome executable paths for the current platform."""
    system = platform.system()
    
    if system == "Windows":
        return [
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
        ]
    elif system == "Darwin":  # macOS
        return [
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    else:  # Linux / WSL
        # Check if we're in WSL
        is_wsl = "microsoft" in platform.uname().release.lower() or "wsl" in platform.uname().release.lower()
        
        paths = [
            Path("/usr/bin/google-chrome"),
            Path("/usr/bin/google-chrome-stable"),
            Path("/usr/bin/chromium"),
            Path("/usr/bin/chromium-browser"),
        ]
        
        if is_wsl:
            # Add Windows Chrome paths accessible from WSL
            paths.extend([
                Path("/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"),
                Path("/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
            ])
            # Try to find user-specific Chrome installation
            try:
                username = subprocess.check_output(["cmd.exe", "/c", "echo", "%USERNAME%"], text=True, stderr=subprocess.DEVNULL).strip()
                paths.append(Path(f"/mnt/c/Users/{username}/AppData/Local/Google/Chrome/Application/chrome.exe"))
            except Exception:
                pass
        
        return paths


def find_chrome():
    """Find the Chrome executable."""
    for path in get_chrome_paths():
        if path.exists():
            return path
    return None


def start_chrome_with_debugging(port: int = 9222):
    """Start Chrome with remote debugging enabled."""
    chrome_path = find_chrome()
    
    if not chrome_path:
        console.print("[red]Could not find Chrome installation![/red]")
        console.print("\nPlease install Chrome or specify the path manually.")
        console.print("\nAlternatively, start Chrome manually with:")
        console.print(f'  chrome --remote-debugging-port={port}')
        return None
    
    console.print(f"[green]Found Chrome at:[/green] {chrome_path}")
    
    # Check if we're in WSL and need to use Windows Chrome
    is_wsl = "microsoft" in platform.uname().release.lower() or "wsl" in platform.uname().release.lower()
    is_windows_chrome = "/mnt/c" in str(chrome_path)
    
    args = [
        str(chrome_path),
        f"--remote-debugging-port={port}",
        "--no-first-run",
        "--no-default-browser-check",
        "https://drupalize.me",  # Start at the login page
    ]
    
    console.print(f"\n[cyan]Starting Chrome with remote debugging on port {port}...[/cyan]")
    
    try:
        if is_wsl and is_windows_chrome:
            # For Windows Chrome from WSL, we need to use a different approach
            # Convert to Windows path format
            chrome_win_path = str(chrome_path).replace("/mnt/c", "C:").replace("/", "\\")
            cmd = f'"{chrome_win_path}" --remote-debugging-port={port} --no-first-run --no-default-browser-check https://drupalize.me'
            subprocess.Popen(["cmd.exe", "/c", "start", "", chrome_win_path, f"--remote-debugging-port={port}", "--no-first-run", "https://drupalize.me"])
        else:
            subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return port
    except Exception as e:
        console.print(f"[red]Failed to start Chrome: {e}[/red]")
        return None


def main():
    console.print(Panel.fit(
        "[bold cyan]Chrome Remote Debugging Launcher[/bold cyan]\n\n"
        "This starts Chrome with remote debugging so the scraper can\n"
        "connect to your real browser and bypass Cloudflare.",
        border_style="cyan"
    ))
    
    port = 9222
    
    result = start_chrome_with_debugging(port)
    
    if result:
        console.print("\n" + "="*60)
        console.print(Panel(
            f"[bold green]Chrome started successfully![/bold green]\n\n"
            f"[yellow]Next steps:[/yellow]\n"
            f"1. Log into [cyan]drupalize.me[/cyan] in the Chrome window\n"
            f"2. Keep Chrome open\n"
            f"3. In a [bold]new terminal[/bold], run:\n\n"
            f"   [bold white]uv run python main.py --cdp-url http://localhost:{port} --vault-dir ./vault[/bold white]\n\n"
            f"The scraper will connect to your logged-in Chrome session.",
            title="Success",
            border_style="green"
        ))
    else:
        console.print("\n[yellow]Manual alternative:[/yellow]")
        console.print("Start Chrome yourself with remote debugging:\n")
        console.print("  Windows (PowerShell):")
        console.print(f'    & "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port={port}')
        console.print("\n  Windows (CMD):")
        console.print(f'    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port={port}')
        console.print(f"\nThen run: uv run python main.py --cdp-url http://localhost:{port} --vault-dir ./vault")


if __name__ == "__main__":
    main()
