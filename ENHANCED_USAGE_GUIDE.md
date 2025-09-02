# 💋 MissDorking™ Enhanced Usage Guide 🍒

## ✨ What's New in Enhanced Edition

Your MissDorking tool now includes fabulous new features:

### 🎯 **Smart File Naming**
- All exports now include domain name and timestamp
- Format: `MissDorking_{domain}_{YYYYMMDD_HHMMSS}.{extension}`
- Bulk scans: `MissDorking_BULK_scan_{YYYYMMDD_HHMMSS}.{extension}`

### 📋 **Bulk Domain Processing**
- Scan multiple domains in one operation
- Load domains from files or enter manually
- Flexible report generation (individual, combined, or both)

### 💻 **Powerful Command Line Interface**
- Full CLI support with extensive options
- Direct scripting capabilities
- Batch processing for automation

### 🎪 **Enhanced Visual Experience**
- Fun ASCII art and colorful output
- Sass-filled completion messages
- Interactive menus with personality

---

## 🚀 Available Tools

### 1. **Enhanced GUI** (`main_gui_enhanced.py`)
**Features:**
- Tabbed interface with Single Domain and Bulk Domains tabs
- Smart filename generation with domain and timestamp
- Multiple report format options
- Load domains from files
- Real-time progress tracking

**Usage:**
```bash
python main_gui_enhanced.py
```

### 2. **Enhanced CLI Tool** (`run_dorking_cli.py`)
**Features:**
- Complete command-line interface
- Single domain and bulk domain scanning
- Multiple export formats (PDF, CSV, JSON)
- Hybrid scraper support
- Flexible report generation

**Examples:**
```bash
# Single domain scan
python run_dorking_cli.py -d example.com

# Bulk domain scan from file
python run_dorking_cli.py -b example_domains.txt --report-format both

# Fast hybrid scan with specific categories
python run_dorking_cli.py -d target.com --hybrid --categories "File Extensions" "Login Pages"

# Custom settings bulk scan
python run_dorking_cli.py -b "domain1.com,domain2.com" --max-results 20 --delay 1-3
```

### 3. **Enhanced Windows Launcher** (`run_dorking_enhanced.bat`)
**Features:**
- Colorful interactive menu
- All modes in one script
- Environment validation
- Smart option handling

**Usage:**
```cmd
run_dorking_enhanced.bat
```

### 4. **Enhanced Unix/Linux Launcher** (`run_dorking_enhanced.sh`)
**Features:**
- Full Unix/Linux compatibility
- Interactive and direct CLI modes
- Colorful terminal output
- Comprehensive error handling

**Usage:**
```bash
# Interactive menu
./run_dorking_enhanced.sh

# Direct CLI usage
./run_dorking_enhanced.sh -d example.com --export pdf csv json
```

---

## 📋 CLI Command Reference

### Basic Usage
```bash
python run_dorking_cli.py [OPTIONS]
```

### Required Arguments (choose one)
- `-d, --domain DOMAIN` - Single domain to scan
- `-b, --bulk BULK` - Bulk domains (comma-separated or file path)

### Scan Options
- `--categories CATEGORIES [CATEGORIES ...]` - Categories to scan (default: all)
- `--max-results MAX_RESULTS` - Maximum results per query (default: 10)
- `--delay DELAY` - Delay between requests in seconds (default: 2-4)
- `--hybrid` - Use hybrid scraper for better results

### Output Options
- `--output-format {console,verbose,quiet}` - Output verbosity level
- `--export {pdf,csv,json} [{pdf,csv,json} ...]` - Export formats (default: pdf)
- `--report-format {individual,combined,both}` - Bulk report format

### Advanced Options
- `--log-level {DEBUG,INFO,WARNING,ERROR}` - Logging level
- `--no-banner` - Suppress banner display

---

## 🎯 Usage Examples

### Single Domain Scanning

#### GUI Mode
1. Launch `main_gui_enhanced.py`
2. Use "Single Domain" tab
3. Enter domain and configure options
4. Click "🚀 Start Dorking"
5. Export with smart filename

#### CLI Mode
```bash
# Basic scan
python run_dorking_cli.py -d example.com

# Advanced scan with options
python run_dorking_cli.py -d target.com \
  --max-results 15 \
  --delay 1-3 \
  --hybrid \
  --categories "Login Pages" "File Extensions" \
  --export pdf csv json
```

### Bulk Domain Scanning

#### GUI Mode
1. Launch `main_gui_enhanced.py`
2. Use "Bulk Domains" tab
3. Enter domains or load from file
4. Choose report format
5. Click "🚀 Start Bulk Dorking"

#### CLI Mode with File
```bash
# Create domains file
echo -e "example.com\ngoogle.com\ngithub.com" > domains.txt

# Scan all domains
python run_dorking_cli.py -b domains.txt --report-format both
```

#### CLI Mode with Direct Input
```bash
python run_dorking_cli.py -b "domain1.com,domain2.com,domain3.com" \
  --report-format individual \
  --export pdf csv
```

### Interactive Launcher Usage

#### Windows
```cmd
run_dorking_enhanced.bat
```
Then choose from the menu:
- [1] GUI Mode
- [2] Enhanced GUI  
- [3] Super Fast GUI
- [4] CLI Mode
- [5] CLI Bulk Mode
- etc.

#### Unix/Linux
```bash
./run_dorking_enhanced.sh
```
Same interactive menu as Windows version.

---

## 📊 Report Formats

### Individual Reports
- One report per domain
- Filename includes domain name and timestamp
- Best for focused analysis per domain

### Combined Reports  
- Single report containing all domains
- Queries prefixed with domain name
- Best for comparative analysis

### Both Reports
- Generates both individual and combined
- Maximum flexibility for different use cases

---

## 🎪 Fun Features

### Smart Filename Examples
```
MissDorking_example.com_20231215_143022.pdf
MissDorking_github.com_20231215_143155.csv
MissDorking_BULK_scan_20231215_143300.pdf
```

### Fabulous Completion Messages
- "💄 Scan complete! Found X fabulous results! 💋"
- "👠 All done dorking! X targets acquired with style! ✨"
- "🔥 Mission accomplished! X results ready for viewing! 💅"

### Colorful Terminal Output
- Pink headers and banners
- Cyan options and menus
- Green success messages
- Red error messages
- Yellow prompts

---

## 🔧 Advanced Configuration

### Custom Categories
Available categories include:
- "File Extensions"
- "Directory Listing"
- "Configuration Files"
- "Database Files"
- "Log Files"
- "Backup Files"
- "Login Pages"
- "SQL Errors"
- "Publicly Exposed Documents"
- "Network Infrastructure"

### Delay Configuration
- Single value: `--delay 3`
- Range: `--delay 2-5`
- Fast scanning: `--delay 0.5-1.5`

### Hybrid Scraper Benefits
- Better success rate against anti-bot measures
- Fallback mechanisms for blocked requests
- Improved result quality

---

## 📁 File Organization

After scanning, you'll find:
- **Individual PDFs**: One per domain with smart naming
- **Combined PDFs**: All domains in single report
- **CSV Files**: Structured data for analysis
- **JSON Files**: Machine-readable format
- **Log Files**: Detailed operation logs

---

## 🚨 Tips & Best Practices

### Performance Optimization
- Use hybrid scraper for better results
- Adjust delay range based on target responsiveness
- Use specific categories to reduce scan time

### Bulk Scanning
- Test with small domain lists first
- Use appropriate report format for your needs
- Monitor logs for failed domains

### Automation
- Use CLI mode for scripting
- Save domain lists in text files
- Use JSON export for data processing

### Troubleshooting
- Check virtual environment activation
- Verify domain file format (one per line)
- Review log files for detailed error information

---

## 🎉 Getting Started

### Quick Start - Single Domain
```bash
# Windows
run_dorking_enhanced.bat

# Unix/Linux  
./run_dorking_enhanced.sh
```
Choose option [4] for CLI Mode, enter a domain, and watch the magic happen!

### Quick Start - Bulk Domains
```bash
python run_dorking_cli.py -b example_domains.txt
```

### Quick Start - GUI
```bash
python main_gui_enhanced.py
```

---

## 💋 Support

For issues, questions, or to show appreciation for the fabulous enhancements:
- Check log files for detailed error information
- Verify all dependencies are installed
- Ensure virtual environment is properly activated

**Stay fabulous and happy dorking! 🍒💅**
