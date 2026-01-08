"""Filter out legacy and O'Reilly content from drupalize_urls.json"""

import json
from pathlib import Path

def filter_urls(input_file: Path, output_file: Path):
    """Filter out legacy and O'Reilly guides and their tutorials."""
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Keywords to filter out (case-insensitive)
    filter_keywords = ['legacy', 'oreilly']
    
    def should_keep(url: str) -> bool:
        url_lower = url.lower()
        return not any(keyword in url_lower for keyword in filter_keywords)
    
    # Filter guides
    original_guides = len(data['guides'])
    data['guides'] = [g for g in data['guides'] if should_keep(g['url'])]
    filtered_guides = original_guides - len(data['guides'])
    
    # Filter tutorials
    original_tutorials = len(data['tutorials'])
    data['tutorials'] = [t for t in data['tutorials'] if should_keep(t.get('guideUrl', '')) and should_keep(t.get('url', ''))]
    filtered_tutorials = original_tutorials - len(data['tutorials'])
    
    # Save filtered data
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Filtered out {filtered_guides} guides ({original_guides} → {len(data['guides'])})")
    print(f"Filtered out {filtered_tutorials} tutorials ({original_tutorials} → {len(data['tutorials'])})")
    print(f"Saved to: {output_file}")

if __name__ == '__main__':
    input_file = Path('drupalize_urls.json')
    output_file = Path('drupalize_urls_filtered.json')
    filter_urls(input_file, output_file)
