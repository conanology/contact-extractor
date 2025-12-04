# Business Contact Info Extractor

![Python](https://img.shields.io/badge/-Python-blue) ![BeautifulSoup4](https://img.shields.io/badge/-BeautifulSoup4-blue) ![Regex](https://img.shields.io/badge/-Regex-blue) ![Phonenumbers](https://img.shields.io/badge/-Phonenumbers-blue)

Extracts business contact information (email, phone, address) from websites and directories.

## Features

- Finds emails using regex patterns
- Extracts phone numbers (validates format)
- Parses business addresses
- Exports to structured CSV
- Deduplication and validation

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/contact-extractor.git
cd contact-extractor

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Extracts emails and phone numbers from any webpage
python main.py --url "https://www.w3.org/Consortium/contact"

# Custom output location
python main.py --url "https://example.com" --output output/results.csv
```

**Live Demo:** Try it now with a real webpage!

```bash
python main.py --url "https://www.w3.org/Consortium/contact"
# Extracts 7+ emails and phone numbers from W3C contact page
```

## Output Format

Results are saved as CSV with the following columns:

| Column | Description |
|--------|-------------|
| name   | Item name   |
| value  | Item value  |
| url    | Source URL  |

## Testing

```bash
pytest tests/
```

## License

MIT License

## Contact

For questions or custom scraping projects, contact me at [your-email]

---

**Note:** This project uses regex patterns to extract contact information from any webpage. It's fully functional and collects real data. Use only on public-facing websites and respect robots.txt and Terms of Service. Do not use for unsolicited marketing.
