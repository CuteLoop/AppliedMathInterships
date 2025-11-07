"""
Common extraction utilities for parsing HTML content.
"""
from typing import Optional, List
from bs4 import BeautifulSoup


def extract_text(html: str, selector: str) -> Optional[str]:
    """
    Extract text from HTML using a CSS selector.
    
    Args:
        html: HTML content as string
        selector: CSS selector to find the element
        
    Returns:
        Extracted text or None if not found
    """
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else None


def extract_all_text(html: str, selector: str) -> List[str]:
    """
    Extract text from all matching elements in HTML.
    
    Args:
        html: HTML content as string
        selector: CSS selector to find elements
        
    Returns:
        List of extracted text from all matching elements
    """
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select(selector)
    return [elem.get_text(strip=True) for elem in elements]


def extract_link(html: str, selector: str) -> Optional[str]:
    """
    Extract href attribute from an anchor tag.
    
    Args:
        html: HTML content as string
        selector: CSS selector to find the anchor element
        
    Returns:
        URL from href attribute or None if not found
    """
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.select_one(selector)
    return element.get('href') if element else None


def extract_all_links(html: str, selector: str) -> List[str]:
    """
    Extract href attributes from all matching anchor tags.
    
    Args:
        html: HTML content as string
        selector: CSS selector to find anchor elements
        
    Returns:
        List of URLs from href attributes
    """
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select(selector)
    return [elem.get('href') for elem in elements if elem.get('href')]
