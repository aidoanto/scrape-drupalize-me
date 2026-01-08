/**
 * Drupalize.me Content Extractor
 * 
 * Run this AFTER extract_urls.js has generated drupalize_urls.json.
 * This script fetches full content for each tutorial.
 * 
 * Usage:
 * 1. Load drupalize_urls.json first (paste it into a variable or use FileReader)
 * 2. Paste this script
 * 3. Wait for extraction (this takes a while - 1-2 seconds per tutorial)
 * 4. Results are downloaded as JSON files (batched to avoid memory issues)
 */

// Helper to load the URLs JSON file
async function loadUrlsFile() {
    return new Promise((resolve) => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = async (e) => {
            const file = e.target.files[0];
            const text = await file.text();
            resolve(JSON.parse(text));
        };
        input.click();
    });
}

(async function extractDrupalizeContent() {
    console.log('📂 Please select your drupalize_urls.json file...');
    const urlsData = await loadUrlsFile();
    
    console.log(`📚 Loaded ${urlsData.tutorials.length} tutorials to extract`);
    
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    
    const results = {
        extractedAt: new Date().toISOString(),
        tutorials: []
    };
    
    const BATCH_SIZE = 50; // Save every 50 tutorials
    let batchNum = 0;
    
    for (let i = 0; i < urlsData.tutorials.length; i++) {
        const tutorial = urlsData.tutorials[i];
        console.log(`[${i + 1}/${urlsData.tutorials.length}] ${tutorial.title}`);
        
        try {
            const response = await fetch(tutorial.url);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Extract tutorial content
            const content = {
                url: tutorial.url,
                title: tutorial.title,
                guide: tutorial.guide,
                guideUrl: tutorial.guideUrl,
                extractedHtml: '',
                videos: [],
                images: [],
                topics: [],
                drupalVersions: [],
                bodyText: ''
            };
            
            // Get main content area
            const mainContent = doc.querySelector('.tutorial-content, .node__content, article, main');
            if (mainContent) {
                content.extractedHtml = mainContent.innerHTML;
                content.bodyText = mainContent.textContent.trim();
            }
            
            // Extract video URLs (Vimeo, YouTube, or direct video)
            const videos = doc.querySelectorAll('iframe[src*="vimeo"], iframe[src*="youtube"], video source, [data-video-url], .video-embed iframe');
            videos.forEach(v => {
                const src = v.getAttribute('src') || v.getAttribute('data-video-url');
                if (src) {
                    content.videos.push(src);
                }
            });
            
            // Also check for video player data attributes
            const videoContainers = doc.querySelectorAll('[data-video-id], [data-vimeo-id]');
            videoContainers.forEach(vc => {
                const videoId = vc.getAttribute('data-video-id') || vc.getAttribute('data-vimeo-id');
                if (videoId) {
                    content.videos.push(`https://player.vimeo.com/video/${videoId}`);
                }
            });
            
            // Extract images
            const images = doc.querySelectorAll('article img, .tutorial-content img, .node__content img');
            images.forEach(img => {
                const src = img.getAttribute('src') || img.getAttribute('data-src');
                if (src && !src.includes('data:image')) {
                    const fullSrc = src.startsWith('http') ? src : `https://drupalize.me${src}`;
                    content.images.push(fullSrc);
                }
            });
            
            // Extract topics/tags
            const topics = doc.querySelectorAll('.field--name-field-topics a, .taxonomy-term a, [rel="tag"]');
            topics.forEach(t => {
                content.topics.push(t.textContent.trim());
            });
            
            // Extract Drupal versions
            const versions = doc.querySelectorAll('.field--name-field-drupal-version a, .drupal-version');
            versions.forEach(v => {
                content.drupalVersions.push(v.textContent.trim());
            });
            
            results.tutorials.push(content);
            
            // Save batch periodically
            if (results.tutorials.length >= BATCH_SIZE) {
                saveBatch(results.tutorials, batchNum);
                batchNum++;
                results.tutorials = [];
            }
            
            await delay(1000); // 1 second between requests
            
        } catch (error) {
            console.error(`Error extracting ${tutorial.url}:`, error);
            results.tutorials.push({
                url: tutorial.url,
                title: tutorial.title,
                error: error.message
            });
        }
    }
    
    // Save remaining tutorials
    if (results.tutorials.length > 0) {
        saveBatch(results.tutorials, batchNum);
    }
    
    console.log('🎉 Extraction complete!');
})();

function saveBatch(tutorials, batchNum) {
    const data = {
        batch: batchNum,
        extractedAt: new Date().toISOString(),
        tutorials: tutorials
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `drupalize_content_batch_${batchNum}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log(`💾 Saved batch ${batchNum} (${tutorials.length} tutorials)`);
}
