"""
SIAM (Society for Industrial and Applied Mathematics) internship provider.
Scrapes career opportunities from SIAM careers page.
"""
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from ..extractors.common import extract_text, extract_all_links


class SIAMProvider:
    """Provider for scraping SIAM career opportunities."""
    
    BASE_URL = "https://www.siam.org/careers/career-center"
    
    def __init__(self):
        """Initialize the SIAM provider."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, url: Optional[str] = None) -> str:
        """
        Fetch the SIAM careers page.
        
        Args:
            url: Optional custom URL, defaults to BASE_URL
            
        Returns:
            HTML content of the page
        """
        target_url = url or self.BASE_URL
        response = self.session.get(target_url)
        response.raise_for_status()
        return response.text
    
    def parse_listings(self, html: str) -> List[Dict[str, str]]:
        """
        Parse career listings from SIAM page HTML.
        
        Args:
            html: HTML content of the careers page
            
        Returns:
            List of dictionaries containing career information
        """
        soup = BeautifulSoup(html, 'html.parser')
        listings = []
        
        # Find all career listing elements
        # This is a generic implementation - actual selectors may vary
        career_elements = soup.select('.career-listing, .job-posting, article.career')
        
        for element in career_elements:
            listing = {}
            
            # Extract title
            title_elem = element.select_one('h2, h3, .title, .job-title')
            if title_elem:
                listing['title'] = title_elem.get_text(strip=True)
            
            # Extract organization
            org_elem = element.select_one('.organization, .company, .employer')
            if org_elem:
                listing['organization'] = org_elem.get_text(strip=True)
            
            # Extract location
            loc_elem = element.select_one('.location, .job-location')
            if loc_elem:
                listing['location'] = loc_elem.get_text(strip=True)
            
            # Extract link
            link_elem = element.select_one('a')
            if link_elem and link_elem.get('href'):
                href = link_elem.get('href')
                # Make absolute URL if relative
                if href.startswith('/'):
                    listing['url'] = f"https://www.siam.org{href}"
                elif not href.startswith('http'):
                    listing['url'] = f"https://www.siam.org/{href}"
                else:
                    listing['url'] = href
            
            # Extract description if available
            desc_elem = element.select_one('.description, .summary, p')
            if desc_elem:
                listing['description'] = desc_elem.get_text(strip=True)
            
            # Only add if we have at least a title
            if listing.get('title'):
                listings.append(listing)
        
        return listings
    
    def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape all SIAM career listings.
        
        Returns:
            List of dictionaries containing career information
        """
        html = self.fetch_page()
        return self.parse_listings(html)
