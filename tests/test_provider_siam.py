"""
Tests for SIAM provider.
"""
import pytest
from pathlib import Path
from scraper.providers.siam import SIAMProvider


@pytest.fixture
def siam_page_html():
    """Load sample SIAM page HTML from fixtures."""
    fixture_path = Path(__file__).parent / 'fixtures' / 'siam_page.html'
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def sample_career_html():
    """Load sample career detail HTML from fixtures."""
    fixture_path = Path(__file__).parent / 'fixtures' / 'sample_career.html'
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return f.read()


class TestSIAMProvider:
    """Test suite for SIAM provider."""
    
    def test_parse_listings(self, siam_page_html):
        """Test parsing of career listings from SIAM page."""
        provider = SIAMProvider()
        listings = provider.parse_listings(siam_page_html)
        
        # Should extract 3 listings from the fixture
        assert len(listings) == 3
        
        # Check first listing
        first_listing = listings[0]
        assert first_listing['title'] == 'Research Intern - Applied Mathematics'
        assert first_listing['organization'] == 'National Institute for Mathematical Sciences'
        assert first_listing['location'] == 'Princeton, NJ'
        assert 'computational modeling' in first_listing['description']
        assert first_listing['url'] == 'https://www.siam.org/careers/12345'
        
        # Check second listing (with external URL)
        second_listing = listings[1]
        assert second_listing['title'] == 'Data Science Internship'
        assert second_listing['organization'] == 'Tech Analytics Corp'
        assert second_listing['location'] == 'Remote'
        assert second_listing['url'] == 'https://example.com/jobs/data-science'
        
        # Check third listing
        third_listing = listings[2]
        assert third_listing['title'] == 'Computational Mathematics Intern'
        assert third_listing['organization'] == 'Scientific Computing Lab'
        assert third_listing['location'] == 'Cambridge, MA'
    
    def test_parse_listings_empty(self):
        """Test parsing with empty HTML."""
        provider = SIAMProvider()
        listings = provider.parse_listings('<html><body></body></html>')
        
        assert listings == []
    
    def test_parse_listings_partial_data(self):
        """Test parsing with partial data."""
        html = '''
        <html>
        <body>
            <article class="career">
                <h3 class="title">Test Position</h3>
                <!-- Missing organization and location -->
            </article>
        </body>
        </html>
        '''
        provider = SIAMProvider()
        listings = provider.parse_listings(html)
        
        # Should still extract the listing with available data
        assert len(listings) == 1
        assert listings[0]['title'] == 'Test Position'
        assert 'organization' not in listings[0] or listings[0].get('organization') is None
    
    def test_provider_initialization(self):
        """Test SIAM provider initialization."""
        provider = SIAMProvider()
        
        assert provider.BASE_URL == "https://www.siam.org/careers/career-center"
        assert hasattr(provider, 'session')
        assert 'User-Agent' in provider.session.headers
