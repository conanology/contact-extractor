#!/usr/bin/env python3
"""
Business Contact Info Extractor

Extracts business contact information (email, phone, address) from websites and directories.

Uses regex patterns to find emails and phone numbers in webpage text.

Usage:
    python main.py --url <target_url>
    python main.py --url "https://example.com"
"""

import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import re


def extract_emails(text):
    """Extract email addresses using regex"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return list(set(re.findall(email_pattern, text)))


def extract_phones(text):
    """Extract phone numbers using regex (US/international formats)"""
    # Matches formats: (123) 456-7890, 123-456-7890, +1-123-456-7890, etc.
    phone_patterns = [
        r'\+?\d{1,3}?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}'
    ]

    phones = []
    for pattern in phone_patterns:
        phones.extend(re.findall(pattern, text))

    # Filter out false positives (too short or too long)
    filtered = []
    for phone in phones:
        digits_only = re.sub(r'\D', '', phone)
        if 10 <= len(digits_only) <= 15:
            filtered.append(phone)

    return list(set(filtered))


def scrape_data(url):
    """
    Main scraping logic - Extracts contact info from web pages

    Args:
        url: Target URL to scrape

    Returns:
        pandas.DataFrame: Scraped data with columns: type, value, url
    """
    # Set headers to avoid bot detection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text content
    text = soup.get_text()

    # Extract contacts
    emails = extract_emails(text)
    phones = extract_phones(text)

    data = []

    # Add emails
    for email in emails:
        data.append({
            'type': 'email',
            'value': email,
            'url': url
        })

    # Add phone numbers
    for phone in phones:
        data.append({
            'type': 'phone',
            'value': phone,
            'url': url
        })

    # If no contacts found, add a note
    if not data:
        data.append({
            'type': 'note',
            'value': 'No contact information found on this page',
            'url': url
        })

    return pd.DataFrame(data)


def main():
    parser = argparse.ArgumentParser(description='Business Contact Info Extractor')
    parser.add_argument(
        '--url',
        required=True,
        help='Target URL to scrape'
    )
    parser.add_argument('--output', default='output/results.csv', help='Output file path')

    args = parser.parse_args()

    print(f"Extracting contacts from {args.url}...")
    df = scrape_data(args.url)

    # Save to CSV
    output_path = Path(args.output)
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)

    # Count by type
    if 'type' in df.columns:
        email_count = len(df[df['type'] == 'email'])
        phone_count = len(df[df['type'] == 'phone'])
        print(f"[OK] Found {email_count} emails, {phone_count} phone numbers")
    else:
        print(f"[OK] Extracted {len(df)} items")

    print(f"[OK] Saved to {output_path}")

    # Display results
    if len(df) > 0:
        print(f"\n[DATA] Results:")
        print(df.to_string(index=False))


if __name__ == '__main__':
    main()
