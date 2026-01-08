# Drupalize.me Scraper

Archive Drupalize.me tutorials into an Obsidian-compatible vault for offline learning.

## The Problem

Cloudflare blocks automated browsers (Playwright, Selenium, etc.) from accessing Drupalize.me. Even with cookies and stealth techniques, the automated browser gets stuck in an infinite "verify you're human" loop.

## The Solution

We use a **two-step approach** that leverages your already-authenticated browser:

1. **JavaScript Extraction** - Run extraction scripts directly in your browser console
2. **Python Processing** - Convert the extracted data into a beautiful Obsidian vault

This works because JavaScript running in your real browser is indistinguishable from a real user.

---

## Quick Start

### Step 1: Install Dependencies

```bash
uv sync
```

### Step 2: Extract URLs (in your browser)

1. Open Chrome/Firefox and log into [drupalize.me](https://drupalize.me)
2. Open Developer Tools (F12 or Ctrl+Shift+I)
3. Go to the **Console** tab
4. Copy the entire contents of `extract_urls.js` and paste it into the console
5. Press Enter and wait (takes ~1 minute)
6. A file `drupalize_urls.json` will download automatically

### Step 3: Extract Content (in your browser)

1. In the same browser console, paste the contents of `extract_content.js`
2. Press Enter
3. When prompted, select the `drupalize_urls.json` file from Step 2
4. Wait for extraction (takes 1-2 hours for all tutorials)
5. Multiple `drupalize_content_batch_X.json` files will download

**Tip:** You can leave this running in a background tab while you do other things!

### Step 4: Build the Vault

```bash
# Put all the JSON files in a folder called 'extracted'
mkdir extracted
mv ~/Downloads/drupalize_*.json extracted/

# Run the processor
uv run python process_extracted.py --content-dir ./extracted --vault-dir ./vault
```

### Step 5: Open in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select the `vault` directory
4. Enjoy your offline Drupal learning archive! 🎉

---

## What Gets Extracted

- ✅ All guides and their structure
- ✅ All tutorial content (text, code examples)
- ✅ All images (downloaded locally)
- ✅ Video URLs (linked, with .url shortcut files for easy access)
- ✅ Topics and tags
- ✅ Drupal version compatibility info
- ✅ Cross-linked Obsidian-style wiki links

## Vault Structure

```
vault/
├── README.md           # Index of all content
├── Guides/             # One file per guide with links to tutorials
│   ├── introduction-to-drupal.md
│   ├── theming-cheat-sheet.md
│   └── ...
├── Tutorials/          # One file per tutorial
│   ├── what-is-drupal.md
│   ├── installing-drupal.md
│   └── ...
└── assets/
    ├── images/         # Downloaded images
    └── videos/         # Video URL shortcuts
```

---

## Alternative: Automated Scraping (if Cloudflare allows)

If you want to try the fully automated approach (which may work if Cloudflare isn't blocking):

```bash
# Using cookies exported from your browser
uv run python main.py --cookies-file cookies.json --no-headless

# Or connect to your existing Chrome with remote debugging
# First, start Chrome with: chrome --remote-debugging-port=9222
uv run python main.py --cdp-url http://localhost:9222
```

## Exporting Cookies

To export cookies from your browser:

1. Install a cookie export extension:

   - Firefox: [Cookie Quick Manager](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/)
   - Chrome: [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)

2. Go to drupalize.me while logged in
3. Export cookies as JSON
4. Save as `cookies.json` in this directory

---

## Troubleshooting

### "Cloudflare keeps blocking me"

This is why we recommend the JavaScript extraction approach - it runs in your real browser which Cloudflare trusts.

### "The extraction is taking forever"

The content extraction script waits 1 second between requests to avoid being rate-limited. For ~500 tutorials, expect ~10 minutes for URL extraction and ~1-2 hours for full content.

### "Some videos aren't downloading"

Vimeo videos require special handling. The script saves `.url` shortcut files that you can double-click to open the video in your browser.

### "I'm getting JSON parse errors"

Make sure all the JSON files are complete. If the extraction was interrupted, delete the incomplete files and re-run from where it stopped.

---

## Files

| File                   | Purpose                                               |
| ---------------------- | ----------------------------------------------------- |
| `extract_urls.js`      | Browser script to get all guide/tutorial URLs         |
| `extract_content.js`   | Browser script to get full tutorial content           |
| `process_extracted.py` | Python script to build Obsidian vault                 |
| `main.py`              | Alternative automated scraper (blocked by Cloudflare) |
| `cookies.json`         | Your browser cookies (if using automated approach)    |

---

## Why This Architecture?

1. **Cloudflare Protection**: Drupalize.me uses Cloudflare which aggressively blocks automated browsers
2. **Authenticated Content**: Tutorials are behind a paywall, requiring your login session
3. **Browser Trust**: Your real browser has established trust with Cloudflare over time
4. **JavaScript Approach**: Running extraction scripts in your browser is indistinguishable from normal usage

This approach may seem more manual, but it's **guaranteed to work** because you're using your own authenticated, trusted browser session.

---

## License

For personal educational use only. Respect Drupalize.me's terms of service.
