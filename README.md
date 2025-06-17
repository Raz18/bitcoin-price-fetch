# Bitcoin Price Tracker 📈

A robust, production-ready Bitcoin price tracking application built with Python that monitors BTC prices, generates visualizations, and sends automated email reports. Features asynchronous programming, comprehensive logging, and professional-grade error handling.

## 🚀 Features

### Core Functionality
- **Real-time Bitcoin Price Monitoring**: Fetches current BTC prices from Coinbase API every minute
- **Automated Data Collection**: Configurable tracking duration with persistent JSON storage
- **Professional Visualizations**: Generates detailed price trend graphs with matplotlib
- **Email Reporting**: Automated email delivery with price summaries and chart attachments
- **Maximum Price Detection**: Tracks and reports peak prices during monitoring periods

### Technical Highlights
- **Asynchronous Architecture**: Built with `asyncio` and `aiohttp` for optimal performance
- **Object-Oriented Design**: Clean separation of concerns with dedicated classes
- **Comprehensive Logging**: Detailed logging with both console and file output
- **Robust Error Handling**: Graceful handling of network, API, and system errors
- **Environment-Based Configuration**: Secure credential management with `.env` support
- **Production-Ready Testing**: Complete API test suite with mocking and async test support

## 🏗️ Architecture

```
bitcoin-tracker/
├── api_handler.py           # API communication and data fetching
├── business_logic.py        # Core application orchestration
├── email_sender.py         # SMTP email functionality
├── graph_generator.py      # Chart generation and visualization
├── price_data_storage.py   # Data persistence and management
├── main.py                 # Application entry point
├── config/
│   ├── __init__.py
│   └── app_config.py       # Configuration management
├── utils/
│   ├── __init__.py
│   └── logger.py           # Centralized logging setup
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures and mocking
│   └── test_api_fetch.py   # API handler test suite
├── temp/
│   └── test_runs/          # Log file storage
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Modern Python with async/await support
- **aiohttp**: Asynchronous HTTP client for API requests
- **asyncio**: Built-in async programming framework
- **matplotlib**: Professional chart generation
- **smtplib**: Email delivery functionality

### Development & Testing
- **pytest**: Comprehensive testing framework
- **pytest-asyncio**: Async test support
- **unittest.mock**: Advanced mocking capabilities
- **python-dotenv**: Environment variable management

### Data & Visualization
- **JSON**: Lightweight data persistence
- **matplotlib with seaborn styling**: Professional visualizations
- **Pathlib**: Modern file system operations

## 📋 Pre-requisites

- Python 3.8 or higher
- Gmail account or SMTP server access
- Internet connection for API access
- 50MB free disk space (for logs and outputs)

## 🚀 Quick Start

### 1. Extract and Setup

```bash
# extract the code zip file
tar -xf file.zip

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your configuration
# Use your preferred text editor
notepad .env        # Windows
nano .env          # Linux/macOS
code .env          # VS Code
```

### 3. Configure Email Settings

For Gmail users:
1. Enable 2-Factor Authentication
2. Generate an App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Use the App Password (not your regular password) in `.env`

### 4. Run the Application

```bash
# Run with default settings (60 minutes tracking)
python main.py

# The application will:
# 1. Start fetching Bitcoin prices every minute
# 2. Log all activities to console and file
# 3. Generate a graph after completion
# 4. Send email report with maximum price and chart
```

## ⚙️ Configuration

### Environment Variables (.env)

Create a `.env` file in the project root with the following configuration:

```bash
# API Configuration
API_URL=https://api.coinbase.com/v2/prices/BTC-USD/spot

# Tracking Settings
TRACKING_DURATION=60                    # Duration in minutes (default: 60)

# File Paths
JSON_FILEPATH=data/bitcoin_prices.json  # Price data storage
GRAPH_FILEPATH=output/bitcoin_graph.png # Generated chart location

# Email Configuration
RECIPIENT_EMAIL=your-email@example.com  # Where to send reports
SENDER_EMAIL=sender@gmail.com           # Your Gmail address
SENDER_PASSWORD=your-app-password       # Gmail App Password (not regular password)
SMTP_SERVER=smtp.gmail.com              # Gmail SMTP server
SMTP_PORT=587                           # Gmail SMTP port

# Optional: Custom SMTP Settings
# SMTP_SERVER=your-smtp-server.com
# SMTP_PORT=465                         # Use 465 for SSL, 587 for STARTTLS
```

### Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_URL` | Coinbase API endpoint | coinbase.com/v2/prices/BTC-USD/spot | ✅ |
| `TRACKING_DURATION` | Monitoring duration (minutes) | 60 | ✅ |
| `JSON_FILEPATH` | Price data file path | Required | ✅ |
| `GRAPH_FILEPATH` | Chart output path | Required | ✅ |
| `RECIPIENT_EMAIL` | Report recipient | Required | ✅ |
| `SENDER_EMAIL` | Sender email address | Required | ✅ |
| `SENDER_PASSWORD` | Email password/app password | Required | ✅ |
| `SMTP_SERVER` | SMTP server address | smtp.gmail.com | ✅ |
| `SMTP_PORT` | SMTP server port | 587 | ✅ |

## 📁 Dependencies (requirements.txt)

```txt
# Core Dependencies
aiohttp>=3.8.0
asyncio-compat>=0.1.2
python-dotenv>=0.19.0

# Data Visualization
matplotlib>=3.5.0
seaborn>=0.11.0

# Development and Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.10.0

# Utilities
pathlib2>=2.3.7; python_version < "3.4"
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api_fetch.py

# Run with coverage report
pytest --cov=. --cov-report=html

# Run async tests only
pytest -k "async"
```

### Test Structure

The application includes comprehensive tests covering:

- **API Handler Tests**: Network requests, error handling, response parsing
- **Mock Implementation**: Complete aiohttp session mocking
- **Async Testing**: Proper async/await test patterns
- **Error Scenarios**: Connection timeouts, invalid responses, parsing errors
- **Parametrized Tests**: Multiple test cases with different inputs

### Test Configuration

Tests use advanced mocking strategies:
- **Session-level fixtures**: Shared mock configurations
- **Parametrized responses**: Testing multiple API response scenarios
- **Async context managers**: Proper async resource management
- **Error injection**: Simulating various failure conditions

## 📊 Output Files

### JSON Data File
```json
[
    {
        "timestamp": "2024-01-15T10:30:00.123456",
        "price": 42350.75
    },
    {
        "timestamp": "2024-01-15T10:31:00.234567",
        "price": 42375.25
    }
]
```
### bitcoin_price_graph.png: An image file of the generated price chart.

### An email sent to your configured recipient address, containing the maximum price and the graph as an attachment.

### Log Files
- **Location**: `temp/test_runs/test_run_DD-MM-YYYY_HH-MM-SS.log`
- **Format**: Timestamped entries with module names and log levels
- **Content**: API requests, price updates, errors, and system events

### Graph Output
- **Format**: PNG image with professional styling
- **Features**: Time-series line chart with price statistics
- **Styling**: Seaborn whitegrid theme with custom formatting
- **Details**: Timestamps, price formatting, and trend visualization



#### Email Authentication Errors
```bash
# Error: Authentication failed
# Solution: Use Gmail App Password instead of regular password
```

#### API Connection Issues
```bash
# Error: Connection timeout
# Solution: Check internet connection and API endpoint
```

#### File Permission Errors
```bash
# Error: Cannot create output directories
# Solution: Ensure write permissions or create directories manually
mkdir -p data output temp/test_runs
```

#### Module Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### Debug Mode

For detailed debugging, modify the logger level in `utils/logger.py`:

``` python
# Change from INFO to DEBUG
logger.setLevel(logging.DEBUG)
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)
```

## 🚀 Advanced Usage

### Custom Tracking Duration

```bash
# Set custom duration in .env
TRACKING_DURATION=30  # 30 minutes instead of default 60
```

### Multiple Recipients

```bash
# Modify email_sender.py to support multiple recipients
RECIPIENT_EMAIL=email1@example.com,email2@example.com
```

## 🙏 Acknowledgments

- [Coinbase API](https://developers.coinbase.com/) for reliable Bitcoin price data
- [aiohttp](https://docs.aiohttp.org/) for excellent async HTTP functionality
- [matplotlib](https://matplotlib.org/) for powerful visualization capabilities
