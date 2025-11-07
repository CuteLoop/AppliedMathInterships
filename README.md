# Applied Math Internships

A web scraper and automation tool for collecting and managing applied mathematics internship opportunities from various sources.

## Features

- 🔍 **Web Scraping**: Automatically scrape internship listings from multiple providers
- 📧 **Email Generation**: Generate personalized outreach emails from templates
- ⏰ **Scheduled Updates**: Automated daily scraping via GitHub Actions
- 🌐 **GitHub Pages**: Publish scraped data to a static website
- 🧪 **Tested**: Comprehensive test suite with pytest

## Project Structure

```
applied-math-internships/
├─ scraper/                     # Main scraper package
│  ├─ __init__.py
│  ├─ main.py                   # Entry point for scraping
│  ├─ providers/                # Scraper providers for different sources
│  │  └─ siam.py                # SIAM career center provider
│  └─ extractors/               # HTML extraction utilities
│     └─ common.py              # Common extraction functions
├─ scripts/                     # Utility scripts
│  └─ format_for_outreach.py   # Generate outreach emails
├─ templates/                   # Email templates
│  └─ cold_email_template.txt  # Cold email template
├─ site/                        # Generated website files
├─ data/                        # Scraped data (JSON files)
├─ out/                         # Generated emails
├─ tests/                       # Test suite
│  ├─ fixtures/                 # Test fixtures
│  │  ├─ siam_page.html
│  │  └─ sample_career.html
│  └─ test_provider_siam.py
├─ .github/workflows/           # GitHub Actions workflows
│  ├─ scheduled.yml             # Daily scraping workflow
│  └─ pages.yml                 # GitHub Pages deployment
├─ requirements.txt             # Python dependencies
└─ README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CuteLoop/AppliedMathInterships.git
   cd AppliedMathInterships
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Scraping Internships

Run the scraper to collect internship listings:

```bash
# Scrape from all providers
python -m scraper.main --provider all --output data

# Scrape from specific provider
python -m scraper.main --provider siam --output data
```

The scraped data will be saved in the `data/` directory as JSON files.

### Generating Outreach Emails

Generate personalized emails from scraped data:

```bash
python scripts/format_for_outreach.py \
  --data data/siam_latest.json \
  --template templates/cold_email_template.txt \
  --output out
```

This will create individual email files in the `out/` directory for each internship.

### Customizing Email Templates

Edit `templates/cold_email_template.txt` to customize the email format. Use placeholders like `{{title}}`, `{{organization}}`, `{{location}}`, and `{{url}}` which will be replaced with actual data.

## Running Tests

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scraper tests/

# Run specific test file
pytest tests/test_provider_siam.py
```

## Automation

### Scheduled Scraping

The project includes a GitHub Actions workflow (`.github/workflows/scheduled.yml`) that automatically runs the scraper daily at 9 AM UTC. The workflow:

1. Runs the scraper for all providers
2. Commits the new data to the repository
3. Pushes the changes

### GitHub Pages Deployment

The `.github/workflows/pages.yml` workflow automatically deploys scraped data to GitHub Pages whenever changes are pushed to the main branch.

## Adding New Providers

To add a new internship source:

1. Create a new provider class in `scraper/providers/`:
   ```python
   class NewProvider:
       def scrape(self) -> List[Dict[str, str]]:
           # Implement scraping logic
           pass
   ```

2. Add the provider to `scraper/main.py`:
   ```python
   providers = {
       'siam': SIAMProvider,
       'new_provider': NewProvider,
   }
   ```

3. Create tests in `tests/test_provider_newprovider.py`

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - feel free to use this project for your own internship search!

## Providers

### SIAM (Society for Industrial and Applied Mathematics)

Scrapes career opportunities from the SIAM career center. SIAM is a leading organization for applied mathematics professionals.

- Website: https://www.siam.org/careers/career-center
- Focus: Applied mathematics, computational science, data science

## Disclaimer

This tool is for educational and personal use. Please respect the terms of service and robots.txt of any websites you scrape. Be mindful of rate limiting and use appropriate delays between requests.