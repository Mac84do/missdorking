# MissDorking - Google Dorking Tool

**A comprehensive, cross-platform Google dorking application for security professionals and researchers.**

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Features

- **Cross-Platform**: Runs on Windows and Debian/Ubuntu Linux
- **Comprehensive Dork Database**: 100+ predefined Google dork queries across 10 categories
- **🎯 Hybrid Scraper Technology**: Advanced direct site analysis that finds login pages even when Google blocks traditional dorking
- **Multi-Engine Search**: Fallback support for Bing and DuckDuckGo when Google rate limits
- **User-Friendly GUI**: Clean tkinter interface with progress tracking
- **Fun Splash Screen**: Animated MissDorking character with cheeky cybersecurity humor 💋
- **🧠 Smart Analysis**: AI-powered result analysis with security relevance scoring and risk prioritization
- **Export Capabilities**: Generate professional PDF reports and CSV files
- **Rate Limiting**: Built-in delays to respect Google's terms of service
- **Configurable**: Customizable results per query and delay settings
- **Category Selection**: Choose specific dork categories to scan
- **Real-time Progress**: Live progress tracking with detailed status updates
- **Playful UI**: Fun completion messages and Easter eggs throughout

## 📋 Dork Categories

The tool includes comprehensive dork queries in the following categories:

1. **Information Disclosure** - Find exposed documents and files
2. **Login Pages** - Discover admin panels and login interfaces
3. **Configuration Files** - Locate configuration and settings files
4. **Error Messages** - Find pages with exposed error information
5. **Database Files** - Search for database backups and dumps
6. **Directory Listings** - Identify exposed directory structures
7. **Sensitive Parameters** - Find URLs with potentially vulnerable parameters
8. **Version Information** - Discover software versions and technologies
9. **Backup Files** - Locate backup and temporary files
10. **Email Addresses** - Find contact information and email addresses

## 🛠️ Installation

### Windows Installation

1. **Download and extract** the application files to your desired directory
2. **Right-click** on `install_windows.bat` and select "Run as administrator"
3. **Follow the installation prompts**

The installer will:
- Check for Python 3.7+ installation
- Create a virtual environment
- Install all required dependencies
- Create launch scripts and shortcuts

### Debian/Ubuntu Installation

1. **Download and extract** the application files to your desired directory
2. **Make the install script executable:**
   ```bash
   chmod +x install_debian.sh
   ```
3. **Run the installation script:**
   ```bash
   ./install_debian.sh
   ```

The installer will:
- Install required system packages
- Check Python installation and version
- Create a virtual environment
- Install Python dependencies
- Create desktop entry and launch scripts

## 🚀 Usage

### Windows
- Double-click `run_dorking_tool.bat`, or
- Find "Google Dorking Tool" in your Start Menu

### Linux
- Run `./run_dorking_tool.sh`, or
- Find "Google Dorking Tool" in your applications menu

### Using the Application

1. **Enter Target Domain**: Input the domain you want to scan (e.g., `example.com`)
2. **Configure Options**:
   - Set results per query (1-50)
   - Adjust delay between requests (e.g., "2-5" for random delay between 2-5 seconds)
   - Select categories to scan
3. **Start Dorking**: Click "Start Dorking" to begin the scan
4. **Monitor Progress**: Watch the real-time progress and results
5. **Export Results**: Use "Export PDF" or "Export CSV" to save your findings

## 🎯 Hybrid Scraper Technology

**NEW!** MissDorking now includes advanced hybrid scraper technology that finds login pages and admin panels even when Google blocks traditional dorking queries.

### How It Works

1. **Traditional Google Dorking** - Runs comprehensive dork queries across all selected categories
2. **Direct Site Analysis** - When Google rate limits occur, automatically switches to direct site analysis:
   - **Homepage Parsing**: Scans the target homepage for login-related links
   - **Common Path Enumeration**: Tests common login paths (`/login`, `/admin`, `/account`, etc.)
   - **Form Analysis**: Detects login forms with password/username fields
   - **Smart Detection**: Uses AI-powered analysis to identify login indicators

### Hybrid Results Example

```
=== Login & Admin Pages ===
site:example.com inurl:login: 0 results  (Google blocked)
site:example.com inurl:admin: 0 results  (Google blocked)

=== DIRECT SITE ANALYSIS ===
Direct site analysis of example.com: 4 results
  🎯 Log in - Example Corp
    https://example.com/account/login
  🎯 Admin Portal - Example Corp  
    https://example.com/admin
  🎯 Customer Login
    https://example.com/customer/signin
  🎯 Management Dashboard
    https://admin.example.com/

=== SECURITY ASSESSMENT SUMMARY ===
High Risk Findings: 4
Login Pages Found: 4
Sensitive Files: 0
```

### Advantages

- **🚫 Bypasses Google Rate Limiting** - No more "0 results" due to blocks
- **🎯 Higher Accuracy** - Direct analysis often finds more login pages than Google search
- **⚡ Faster Results** - No waiting for Google retry delays
- **🔍 Comprehensive Coverage** - Combines search engine results with direct analysis
- **🧠 Smart Scoring** - AI-powered risk assessment and confidence scoring

## 📊 Sample Output

The application displays results in real-time:

```
=== Information Disclosure ===
site:example.com filetype:pdf: 15 results
  • Annual Report 2023 - Example Corp
    https://example.com/reports/annual_report_2023.pdf
  • Technical Documentation
    https://example.com/docs/tech_manual.pdf
  ... and 13 more results

=== Login Pages ===
site:example.com inurl:admin: 3 results
  • Admin Panel - Example Corp
    https://example.com/admin/login
  ...
```

## 📄 Export Formats

### PDF Report
- Professional formatted report with executive summary
- Organized by category with detailed results
- Includes metadata and generation timestamp
- Perfect for documentation and reporting

### CSV Export
- Structured data format for analysis
- Fields: Category, Query, Title, URL, Snippet, Timestamp
- Easy to import into spreadsheet applications
- Suitable for further data processing

## ⚠️ Important Notes

### Legal and Ethical Use
- **Only use this tool for authorized security testing**
- **Obtain proper permission** before scanning domains you don't own
- **Respect Google's Terms of Service** and rate limits
- **Use responsibly** for legitimate security research purposes

### Rate Limiting
- The tool includes built-in delays between requests
- Default delay is 2-5 seconds (randomized)
- Adjust delays based on your specific requirements
- Higher delays reduce the chance of being blocked

### Limitations
- Results depend on what Google has indexed
- Some queries may return fewer results due to Google's algorithms
- Rate limiting may slow down large scans
- Results may vary based on geographic location and Google's regional differences

## 🛠️ Technical Details

### Requirements
- Python 3.7 or higher
- tkinter (usually included with Python)
- Internet connection for Google searches

### Dependencies
- `requests` - HTTP library for web requests
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser
- `reportlab` - PDF generation
- `fake-useragent` - User agent rotation
- `python-dateutil` - Date/time utilities

### Architecture
The application is built with a modular design:

- `main_gui.py` - Main application and GUI
- `google_dorks.py` - Dork query database and management
- `scraper.py` - Web scraping and Google search functionality
- `export.py` - PDF and CSV export capabilities

## 🔧 Configuration

### Customizing Dork Queries
You can modify `google_dorks.py` to add your own dork queries:

```python
GOOGLE_DORKS = {
    "Custom Category": [
        'site:{domain} "custom query"',
        'site:{domain} filetype:custom',
        # Add more queries...
    ]
}
```

### Adjusting Delays
Modify the delay range in the GUI or programmatically:

```python
scraper.delay_range = (3, 8)  # 3-8 second delay range
```

## 🐛 Troubleshooting

### Common Issues

**"Python not found" error:**
- Ensure Python 3.7+ is installed and in your system PATH
- On Windows, reinstall Python with "Add to PATH" option checked

**"Failed to install requirements" error:**
- Check your internet connection
- Try running the installer as administrator (Windows)
- On Linux, ensure you have python3-dev installed

**GUI doesn't start:**
- Ensure tkinter is installed (`python -m tkinter` should open a test window)
- On Linux: `sudo apt install python3-tk`

**No search results:**
- Check if the domain exists and is indexed by Google
- Try different dork categories
- Verify your internet connection
- Consider if you've been rate-limited by Google

### Logs
The application creates `dorking_app.log` with detailed logging information for troubleshooting.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Areas for Contribution
- Additional dork query categories
- New export formats
- UI/UX improvements
- Platform support (macOS)
- Performance optimizations

## 📞 Support

For support, please:
1. Check the troubleshooting section
2. Review the application logs
3. Open an issue on the project repository

## ⚖️ Disclaimer

This tool is for educational and authorized security testing purposes only. Users are responsible for complying with applicable laws and regulations. The developers assume no liability for misuse of this software.

---

**Happy Dorking! 🎯**
