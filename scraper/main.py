"""
Main scraper entry point.
"""
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from .providers.siam import SIAMProvider


def save_results(results: List[Dict], output_dir: Path, provider_name: str):
    """
    Save scraping results to JSON file.
    
    Args:
        results: List of scraped internship data
        output_dir: Directory to save results
        provider_name: Name of the provider (e.g., 'siam')
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{provider_name}_{timestamp}.json"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Also save as latest
    latest_filepath = output_dir / f"{provider_name}_latest.json"
    with open(latest_filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(results)} results to {filepath}")
    print(f"Latest results at {latest_filepath}")


def main():
    """Main entry point for the scraper."""
    parser = argparse.ArgumentParser(description='Scrape applied math internships')
    parser.add_argument(
        '--provider',
        choices=['siam', 'all'],
        default='all',
        help='Provider to scrape (default: all)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data'),
        help='Output directory for results (default: data)'
    )
    
    args = parser.parse_args()
    
    providers = {
        'siam': SIAMProvider,
    }
    
    # Determine which providers to run
    if args.provider == 'all':
        providers_to_run = providers.items()
    else:
        providers_to_run = [(args.provider, providers[args.provider])]
    
    # Run each provider
    for provider_name, provider_class in providers_to_run:
        print(f"\n{'='*60}")
        print(f"Scraping {provider_name.upper()}...")
        print(f"{'='*60}\n")
        
        try:
            provider = provider_class()
            results = provider.scrape()
            save_results(results, args.output, provider_name)
            print(f"✓ Successfully scraped {len(results)} listings from {provider_name}")
        except Exception as e:
            print(f"✗ Error scraping {provider_name}: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main()
