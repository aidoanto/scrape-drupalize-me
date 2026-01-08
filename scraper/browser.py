"""Browser session management using Playwright."""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from playwright.async_api import async_playwright, Browser, BrowserContext, Page


class BrowserSession:
    """Manages Playwright browser session - can connect to your real Chrome browser."""

    def __init__(
        self,
        user_data_dir: Optional[Path] = None,
        headless: bool = True,
        cookies_file: Optional[Path] = None,
        cdp_url: Optional[str] = None,
        chrome_profile_path: Optional[Path] = None,
    ):
        """
        Initialize browser session manager.

        Args:
            user_data_dir: Directory to store browser data (only for standalone mode)
            headless: Whether to run browser in headless mode
            cookies_file: Optional path to JSON file with cookies to import
            cdp_url: Connect to existing Chrome via Chrome DevTools Protocol (e.g., "http://localhost:9222")
            chrome_profile_path: Path to your Chrome user data directory to use your real profile
        """
        self.user_data_dir = user_data_dir or Path.home() / ".drupalize_scraper"
        self.headless = headless
        self.cookies_file = cookies_file
        self.cdp_url = cdp_url
        self.chrome_profile_path = chrome_profile_path
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._owns_browser = True  # Whether we launched the browser ourselves

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def start(self):
        """Start the browser session."""
        self.playwright = await async_playwright().start()

        if self.cdp_url:
            # Connect to existing Chrome instance via CDP - best for avoiding detection
            await self._connect_to_chrome_cdp()
        elif self.chrome_profile_path:
            # Use your actual Chrome profile - good balance
            await self._launch_with_chrome_profile()
        else:
            # Fallback: Launch standalone Playwright browser
            await self._launch_standalone()

        # Import cookies if provided and we have a context
        if self.cookies_file and self.cookies_file.exists() and self.context:
            await self._import_cookies(self.cookies_file)

    async def _connect_to_chrome_cdp(self):
        """Connect to an existing Chrome browser via Chrome DevTools Protocol."""
        print(f"Connecting to Chrome at {self.cdp_url}...")
        try:
            self.browser = await self.playwright.chromium.connect_over_cdp(self.cdp_url)
            self._owns_browser = False  # We didn't launch it, don't close it
            
            # Get the default context (the browser's existing context)
            contexts = self.browser.contexts
            if contexts:
                self.context = contexts[0]
                if self.context.pages:
                    self.page = self.context.pages[0]
                else:
                    self.page = await self.context.new_page()
            else:
                self.context = await self.browser.new_context()
                self.page = await self.context.new_page()
                
            print("Connected successfully!")
        except Exception as e:
            print(f"Failed to connect to Chrome: {e}")
            print("\nMake sure Chrome is running with remote debugging enabled:")
            print('  Windows: chrome.exe --remote-debugging-port=9222')
            print('  Mac: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222')
            print('  Linux: google-chrome --remote-debugging-port=9222')
            raise

    async def _launch_with_chrome_profile(self):
        """Launch Chrome using your actual Chrome profile."""
        print(f"Launching Chrome with profile from {self.chrome_profile_path}...")
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.chrome_profile_path),
            headless=False,  # Must be visible when using real profile
            channel="chrome",  # Use installed Chrome, not Chromium
            viewport={"width": 1920, "height": 1080},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ],
        )
        
        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()

    async def _launch_standalone(self):
        """Launch a standalone Playwright browser (original method)."""
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        stealth_args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
        ]
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=self.headless,
            viewport={"width": 1920, "height": 1080},
            args=stealth_args,
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York",
        )

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()

        await self._inject_stealth_scripts()

    async def _inject_stealth_scripts(self):
        """Inject scripts to make the browser less detectable."""
        if not self.page:
            return

        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            window.chrome = { runtime: {} };
        """)

    async def _import_cookies(self, cookies_file: Path):
        """Import cookies from a JSON file."""
        try:
            with open(cookies_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)

            if isinstance(cookies, dict) and "cookies" in cookies:
                cookies = cookies["cookies"]
            elif not isinstance(cookies, list):
                cookies = [cookies]

            normalized_cookies = []
            for cookie in cookies:
                normalized = {
                    "name": cookie.get("name"),
                    "value": cookie.get("value"),
                    "domain": cookie.get("domain"),
                    "path": cookie.get("path", "/"),
                }

                if "expirationDate" in cookie and cookie["expirationDate"]:
                    normalized["expires"] = int(cookie["expirationDate"])
                if "httpOnly" in cookie:
                    normalized["httpOnly"] = bool(cookie["httpOnly"])
                if "secure" in cookie:
                    normalized["secure"] = bool(cookie["secure"])

                same_site = cookie.get("sameSite")
                if same_site is None or same_site == "null" or same_site == "":
                    normalized["sameSite"] = "None"
                elif isinstance(same_site, str):
                    same_site_lower = same_site.lower()
                    if same_site_lower == "strict":
                        normalized["sameSite"] = "Strict"
                    elif same_site_lower == "lax":
                        normalized["sameSite"] = "Lax"
                    else:
                        normalized["sameSite"] = "None"
                else:
                    normalized["sameSite"] = "None"

                normalized_cookies.append(normalized)

            if normalized_cookies:
                await self.context.add_cookies(normalized_cookies)
                print(f"Imported {len(normalized_cookies)} cookies")
        except Exception as e:
            print(f"Warning: Could not import cookies: {e}")

    async def export_cookies(self, output_file: Path) -> List[dict]:
        """Export current cookies to a JSON file."""
        if not self.context:
            return []
        cookies = await self.context.cookies()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
        return cookies

    async def close(self):
        """Close the browser session."""
        # Don't close if we connected to an existing browser
        if self._owns_browser:
            if self.context:
                await self.context.close()
        if self.playwright:
            await self.playwright.stop()

    async def navigate(self, url: str, wait_until: str = "networkidle", timeout: int = 60000) -> Page:
        """Navigate to a URL and wait for page load."""
        if not self.page:
            raise RuntimeError("Browser session not started. Call start() first.")
        await self.page.goto(url, wait_until=wait_until, timeout=timeout)
        return self.page

    async def get_content(self, url: str) -> str:
        """Get HTML content from a URL."""
        page = await self.navigate(url)
        return await page.content()

    async def wait_for_cloudflare(self, timeout: int = 30000):
        """Wait for Cloudflare verification to complete if present."""
        if not self.page:
            return
        try:
            await self.page.wait_for_selector("text=Just a moment", state="hidden", timeout=timeout)
        except Exception:
            pass
        await asyncio.sleep(2)
