"""
Format internship data for outreach emails.
Reads scraped data and generates personalized outreach emails.
"""
import json
import argparse
from pathlib import Path
from typing import Dict, List


def load_template(template_path: Path) -> str:
    """
    Load email template from file.
    
    Args:
        template_path: Path to template file
        
    Returns:
        Template content as string
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_internships(data_path: Path) -> List[Dict]:
    """
    Load internship data from JSON file.
    
    Args:
        data_path: Path to JSON data file
        
    Returns:
        List of internship dictionaries
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_email(template: str, internship: Dict) -> str:
    """
    Format an email using template and internship data.
    
    Args:
        template: Email template with placeholders
        internship: Internship data dictionary
        
    Returns:
        Formatted email text
    """
    # Replace placeholders with actual data
    email = template
    for key, value in internship.items():
        placeholder = f"{{{{{key}}}}}"
        email = email.replace(placeholder, str(value))
    
    return email


def main():
    """Main entry point for formatting outreach emails."""
    parser = argparse.ArgumentParser(
        description='Format internship data for outreach emails'
    )
    parser.add_argument(
        '--data',
        type=Path,
        required=True,
        help='Path to internship data JSON file'
    )
    parser.add_argument(
        '--template',
        type=Path,
        default=Path('templates/cold_email_template.txt'),
        help='Path to email template file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('out'),
        help='Output directory for formatted emails'
    )
    
    args = parser.parse_args()
    
    # Load template and data
    template = load_template(args.template)
    internships = load_internships(args.data)
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Generate emails
    print(f"Generating emails for {len(internships)} internships...")
    
    for i, internship in enumerate(internships):
        email = format_email(template, internship)
        
        # Create filename from title or index
        title = internship.get('title', f'internship_{i}')
        # Sanitize filename
        filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
        filename = filename.strip().replace(' ', '_')[:50]  # Limit length
        
        output_path = args.output / f"{filename}_{i}.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(email)
        
        print(f"  ✓ Generated: {output_path.name}")
    
    print(f"\nSuccessfully generated {len(internships)} emails in {args.output}")


if __name__ == '__main__':
    main()
