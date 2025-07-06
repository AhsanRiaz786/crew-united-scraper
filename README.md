# Crew United Scraper

A web scraper built with Python and Playwright that extracts company and freelancer information from [Crew United](https://www.crew-united.com), a professional networking platform for the film and television industry.

## 🚀 Features

- **Automated Authentication**: Handles login and session persistence using cookies
- **Multi-target Scraping**: Supports scraping both companies and freelancers
- **Data Extraction**: Extracts name, location, and email information
- **Pagination Support**: Automatically navigates through multiple pages
- **CSV Export**: Saves scraped data to timestamped CSV files
- **Error Handling**: Robust error handling with retry logic
- **Headless Operation**: Runs in headless mode for efficient scraping
- **Rate Limiting**: Built-in delays to prevent overwhelming the target server

## 📋 Prerequisites

- Python 3.7 or higher
- A valid Crew United account
- Internet connection

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd crew-united-scraper
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with your Crew United credentials:
   ```env
   CREW_UNITED_USERNAME=your_username
   CREW_UNITED_PASSWORD=your_password
   ```

## 🚀 Usage

### Basic Usage

Run the scraper with the default configuration:

```bash
python main.py
```

The scraper is currently configured to scrape **German film production companies** by default.

### Configuration

To modify the scraping target, edit the `target_url` variable in the `main()` function:

```python
# For companies (current default)
target_url = "https://www.crew-united.com/en/companies/..."

# For freelancers
target_url = "https://www.crew-united.com/en/freelancers/..."
```

### Output

The scraper creates CSV files with the following naming convention:
```
crew_united_{type}_{timestamp}.csv
```

Example: `crew_united_companies_20231215-143022.csv`

### CSV Structure

| Column | Description |
|--------|-------------|
| name | Company/freelancer name |
| location1 | Primary location |
| location2 | Secondary location (if available) |
| email | Contact email address |

## 🔧 Technical Details

### Architecture

The scraper consists of several key components:

1. **Cookie Management**: 
   - `load_cookies()`: Loads saved session cookies
   - `save_cookies()`: Saves current session cookies

2. **Authentication**:
   - `check_login_status()`: Verifies if user is logged in
   - `perform_login()`: Handles the login process

3. **Main Scraping Logic**:
   - `main()`: Orchestrates the entire scraping process

### Browser Configuration

The scraper uses Chromium with the following optimizations:
- Headless mode for efficiency
- Realistic user agent and viewport
- Additional headers to mimic real browser behavior
- Disabled GPU and sandbox for better compatibility

### Error Handling

- **Network Timeouts**: Configurable timeouts for page loads
- **Login Failures**: Multiple retry attempts with fallback
- **Pagination Errors**: Graceful handling of navigation issues
- **Data Extraction**: Individual item failures don't stop the process

### Rate Limiting

Built-in delays prevent overwhelming the server:
- 2-second wait between pages
- 0.1-second wait between items
- 3-second wait after navigation
- 10-second wait after login attempts

## 📁 Project Structure

```
crew-united-scraper/
├── main.py              # Main scraper script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── cookies.json         # Session cookies (auto-generated)
└── README.md           # This documentation
```

## 🔒 Security & Ethics

### Security Considerations

- **Credentials**: Store login credentials in `.env` file (never commit to version control)
- **Rate Limiting**: Built-in delays respect server resources
- **Session Management**: Secure cookie handling for authentication

### Ethical Guidelines

- **Terms of Service**: Ensure compliance with Crew United's terms of service
- **Rate Limiting**: Don't overwhelm the server with requests
- **Data Usage**: Use scraped data responsibly and in accordance with applicable laws
- **Privacy**: Respect user privacy and data protection regulations

## ⚠️ Important Notes

1. **Account Requirement**: You need a valid Crew United account to use this scraper
2. **Terms Compliance**: Ensure your usage complies with Crew United's terms of service
3. **Rate Limits**: The scraper includes built-in delays; avoid modifying these unless necessary
4. **Data Accuracy**: Scraped data is dependent on the current website structure
5. **Legal Compliance**: Ensure compliance with data protection laws in your jurisdiction

## 🐛 Troubleshooting

### Common Issues

**Login Failures**:
- Verify credentials in `.env` file
- Check if account is not locked/suspended
- Ensure stable internet connection

**No Data Extracted**:
- Website structure may have changed
- Check if target URL is correct
- Verify CSS selectors are still valid

**Browser Launch Errors**:
- Ensure Playwright browsers are installed: `playwright install chromium`
- Check system compatibility

**Permission Errors**:
- Ensure write permissions in the project directory
- Check if antivirus is blocking the script

### Debug Mode

To enable verbose output, modify the browser launch options:
```python
browser = p.chromium.launch(headless=False)  # Run with GUI for debugging
```

## 📝 Changelog

### Version 1.0.0
- Initial release
- Support for companies and freelancers scraping
- Cookie-based session management
- CSV export functionality
- Comprehensive error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add appropriate tests
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please ensure compliance with applicable terms of service and local laws.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments for technical details
3. Create an issue in the repository

---

**Disclaimer**: This tool is provided as-is for educational purposes. Users are responsible for ensuring their usage complies with all applicable terms of service and laws. 