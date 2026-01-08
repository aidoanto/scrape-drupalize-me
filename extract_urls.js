/**
 * Drupalize.me URL Extractor
 * 
 * Run this script in your browser console while logged into Drupalize.me.
 * It will extract all guide and tutorial URLs, then download them as JSON.
 * 
 * Usage:
 * 1. Log into drupalize.me
 * 2. Open browser console (F12 -> Console)
 * 3. Paste this entire script
 * 4. Wait for it to complete
 * 5. A JSON file will be downloaded automatically
 */

(async function extractDrupalizeUrls() {
    const results = {
        extractedAt: new Date().toISOString(),
        guides: [],
        tutorials: [],
        errors: []
    };

    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    
    console.log('🚀 Starting Drupalize.me extraction...');
    
    // Step 1: Get all guide URLs from the search page
    console.log('📚 Fetching guide list...');
    
    let page = 0;
    let hasMorePages = true;
    
    while (hasMorePages) {
        try {
            const url = `https://drupalize.me/search?f[0]=type:guide&page=${page}`;
            console.log(`  Fetching page ${page + 1}: ${url}`);
            
            const response = await fetch(url);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Find guide links
            const guideLinks = doc.querySelectorAll('a[href*="/guide/"]');
            const uniqueGuides = new Set();
            
            guideLinks.forEach(link => {
                const href = link.getAttribute('href');
                if (href && href.startsWith('/guide/') && !href.includes('/tutorial/')) {
                    const fullUrl = `https://drupalize.me${href}`;
                    if (!uniqueGuides.has(fullUrl)) {
                        uniqueGuides.add(fullUrl);
                        results.guides.push({
                            url: fullUrl,
                            title: link.textContent.trim() || href.split('/').pop()
                        });
                    }
                }
            });
            
            // Check for next page
            const nextLink = doc.querySelector('a[rel="next"], .pager__item--next a');
            hasMorePages = nextLink !== null;
            page++;
            
            await delay(500); // Be nice to the server
            
        } catch (error) {
            console.error(`Error on page ${page}:`, error);
            results.errors.push({ type: 'guide_list', page, error: error.message });
            hasMorePages = false;
        }
    }
    
    console.log(`✅ Found ${results.guides.length} guides`);
    
    // Step 2: For each guide, get all tutorial URLs
    console.log('📖 Fetching tutorials from each guide...');
    
    for (let i = 0; i < results.guides.length; i++) {
        const guide = results.guides[i];
        console.log(`  [${i + 1}/${results.guides.length}] ${guide.title}`);
        
        try {
            const response = await fetch(guide.url);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Find all tutorial links within the guide
            // Note: URLs use /tutorial/ (singular), not /tutorials/
            const tutorialLinks = doc.querySelectorAll('a[href*="/tutorial/"]');
            guide.tutorials = [];
            
            tutorialLinks.forEach(link => {
                const href = link.getAttribute('href');
                if (href && href.includes('/tutorial/')) {
                    const fullUrl = href.startsWith('http') ? href : `https://drupalize.me${href}`;
                    const title = link.textContent.trim();
                    
                    // Avoid duplicates
                    if (!guide.tutorials.some(t => t.url === fullUrl)) {
                        guide.tutorials.push({
                            url: fullUrl,
                            title: title || href.split('/').pop()
                        });
                        
                        // Also add to flat tutorials list if not already there
                        if (!results.tutorials.some(t => t.url === fullUrl)) {
                            results.tutorials.push({
                                url: fullUrl,
                                title: title,
                                guide: guide.title,
                                guideUrl: guide.url
                            });
                        }
                    }
                }
            });
            
            console.log(`    Found ${guide.tutorials.length} tutorials`);
            await delay(500);
            
        } catch (error) {
            console.error(`Error fetching guide ${guide.url}:`, error);
            results.errors.push({ type: 'guide_fetch', url: guide.url, error: error.message });
        }
    }
    
    console.log(`✅ Total tutorials found: ${results.tutorials.length}`);
    
    // Step 3: Download as JSON
    console.log('💾 Downloading results...');
    
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'drupalize_urls.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log('🎉 Done! Check your downloads folder for drupalize_urls.json');
    console.log(`   Guides: ${results.guides.length}`);
    console.log(`   Tutorials: ${results.tutorials.length}`);
    if (results.errors.length > 0) {
        console.log(`   Errors: ${results.errors.length}`);
    }
    
    return results;
})();
