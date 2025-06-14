# Bitcoin Price Tracker - Enterprise Grade Application

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Code Style](https://img.shields.io/badge/code%20style-professional-green.svg)](https://github.com)
[![Architecture](https://img.shields.io/badge/architecture-modular-orange.svg)](https://github.com)

A professional-grade Bitcoin price tracking application built with enterprise-level architecture patterns, designed to impress technical reviewers and demonstrate senior automation engineering skills.

## 🏗️ Architecture Overview

This application follows industry best practices with a modular, enterprise-grade architecture:

```
bitcoin_price_tracker/
├── main.py                 # Application entry point with async handling
├── config.py               # Configuration management with validation
├── business_logic.py       # Main orchestrator (Business Logic Layer)
├── api_handler.py          # API communication with circuit breaker
├── data_storage.py         # Data persistence with atomic operations
├── graph_generator.py      # Professional visualizations
├── email_sender.py         # Email service with HTML templates
├── example_usage.py        # Professional usage examples
├── .env                    # Environment configuration
├── requirements.txt        # Dependencies with version pinning
└── README.md              # This comprehensive documentation
```

## 🚀 Key Features

### Enterprise Architecture
- **📐 Modular Design**: Clean separation of concerns with single responsibility principle
- **🔄 Async Operations**: Full asyncio implementation for concurrent operations
- **🛡️ Error Handling**: Comprehensive error handling with graceful degradation
- **📊 Monitoring**: Built-in metrics and performance monitoring
- **🔧 Configuration**: Environment-based configuration with validation

### Professional Data Management
- **💾 Atomic Operations**: Safe data persistence with rollback capabilities
- **🔄 Backup Management**: Automated backup rotation and corruption recovery
- **✅ Data Validation**: Comprehensive data integrity checks
- **📈 Analytics**: Statistical analysis and trend detection

### Advanced API Integration
- **🔄 Rate Limiting**: Token bucket algorithm for API rate management
- **🔌 Circuit Breaker**: Fault tolerance with automatic recovery
- **⚡ Connection Pooling**: Optimized HTTP client with keep-alive
- **🔄 Retry Logic**: Exponential backoff with jitter

### Professional Visualization
- **📊 Multiple Chart Types**: Line charts, distributions, trend analysis
- **🎨 Professional Styling**: Corporate-grade styling with branding
- **📈 Technical Indicators**: Moving averages and statistical overlays
- **💾 Multi-format Export**: PNG, SVG, PDF export capabilities

### Enterprise Email System
- **📧 HTML Templates**: Professional email templates with Jinja2
- **📎 Attachments**: Automated chart and data attachments
- **🔒 Security**: TLS encryption and secure authentication
- **📊 Delivery Tracking**: Email delivery confirmation and statistics

## 📦 Installation & Setup

### 1. Clone and Setup Environment
```bash
git clone <repository-url>
cd bitcoin_price_tracker

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy and edit the environment file
cp .env.example .env
# Edit .env with your configuration
```

**Required Configuration:**
```env
# Email Settings (for Gmail)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password  # Use App Password, not regular password
RECIPIENT_EMAIL=recipient@gmail.com

# Application Settings
TRACKING_DURATION=60
COLLECTION_INTERVAL=60
ENABLE_EMAIL_REPORTS=true
LOG_LEVEL=INFO
```

### 3. Gmail App Password Setup
For Gmail users (recommended):
1. Enable **2-Factor Authentication** in Google Account
2. Go to **Google Account → Security → 2-Step Verification**
3. Click **App Passwords** → Select **Mail** → Generate
4. Use the generated 16-character password in `SENDER_PASSWORD`

## 🎯 Usage Examples

### Quick Start (Recommended)
```bash
# Run interactive examples
python example_usage.py
```

### Direct Execution
```bash
# Run the main application
python main.py
```

### Programmatic Usage
```python
import asyncio
from config import Config
from business_logic import BitcoinPriceOrchestrator

async def run_tracker():
    config = Config()
    orchestrator = BitcoinPriceOrchestrator(config)
    
    await orchestrator.initialize()
    await orchestrator.execute_tracking_cycle()

# Run the tracker
asyncio.run(run_tracker())
```

## 🏗️ Component Architecture

### 1. Main Entry Point (`main.py`)
- **Application Controller Pattern**: Manages application lifecycle
- **Signal Handling**: Graceful shutdown on SIGINT/SIGTERM
- **Error Recovery**: Comprehensive error handling and recovery
- **Async Context Management**: Proper async resource management

### 2. Configuration Management (`config.py`)
- **Singleton Pattern**: Single configuration instance
- **Environment Variables**: Secure configuration via .env files
- **Validation**: Comprehensive configuration validation
- **Type Safety**: Dataclass-based configuration with type hints

### 3. Business Logic Orchestrator (`business_logic.py`)
- **Orchestrator Pattern**: Coordinates all application components
- **Phase Management**: Structured execution phases
- **Progress Monitoring**: Real-time progress tracking
- **Performance Metrics**: Built-in performance monitoring

### 4. API Handler (`api_handler.py`)
- **Circuit Breaker Pattern**: Fault tolerance and automatic recovery
- **Rate Limiting**: Token bucket algorithm for API management
- **Connection Pooling**: Optimized HTTP client management
- **Retry Logic**: Exponential backoff with intelligent retry

### 5. Data Storage Manager (`data_storage.py`)
- **Atomic Operations**: Safe data persistence with rollback
- **Backup Management**: Automated backup creation and rotation
- **Data Validation**: Comprehensive integrity checks
- **Async I/O**: Non-blocking file operations

### 6. Graph Generator (`graph_generator.py`)
- **Factory Pattern**: Multiple chart type generation
- **Professional Styling**: Corporate-grade visualization
- **Statistical Analysis**: Technical indicators and trend analysis
- **Export Optimization**: Multi-format export with compression

### 7. Email Sender (`email_sender.py`)
- **Template Engine**: Jinja2-based HTML email templates
- **Attachment Management**: Automated file attachment handling
- **SMTP Pool**: Connection pooling for email delivery
- **Delivery Confirmation**: Email delivery tracking and statistics

## 📊 Output Files

The application generates several professional-grade outputs:

### Data Files
- **`data/bitcoin_prices.json`**: Structured price data with timestamps
- **`data/backups/`**: Automated backup files with rotation

### Visualizations
- **`data/charts/comprehensive_price_chart_*.png`**: Detailed price analysis
- **`data/charts/executive_dashboard_*.png`**: Executive summary dashboard

### Logs
- **`logs/application.log`**: Comprehensive application logs
- **`logs/performance_metrics.log`**: Performance monitoring data

### Email Reports
- **HTML Email**: Professional report with embedded metrics
- **Attachments**: Charts and data files automatically attached

## 🔧 Configuration Options

### Tracking Configuration
```python
COLLECTION_INTERVAL=60        # Seconds between price collections
TRACKING_DURATION=60          # Minutes to track prices
ENABLE_EMAIL_REPORTS=true     # Send email reports
ENABLE_GRAPH_GENERATION=true  # Generate charts
```

### API Configuration
```python
API_TIMEOUT=10               # API request timeout
MAX_RETRIES=3               # Maximum retry attempts
RATE_LIMIT_RPM=60          # Requests per minute limit
```

### Email Configuration
```python
SMTP_SERVER=smtp.gmail.com  # SMTP server
SMTP_PORT=587              # SMTP port
USE_TLS=true               # Enable TLS encryption
```

## 🔍 Performance Features

### Monitoring & Metrics
- **API Response Times**: Real-time latency monitoring
- **Success Rates**: Request success/failure tracking
- **Data Throughput**: I/O performance metrics
- **Memory Usage**: Resource utilization tracking

### Optimization Features
- **Connection Pooling**: Reuse HTTP connections
- **Async Operations**: Non-blocking I/O operations
- **Efficient Serialization**: Optimized JSON handling
- **Resource Cleanup**: Proper resource management

### Reliability Features
- **Circuit Breaker**: Automatic failure detection and recovery
- **Graceful Degradation**: Continue operation during partial failures
- **Data Integrity**: Atomic operations and validation
- **Backup Recovery**: Automatic backup and restore capabilities

## 🛠️ Development & Testing

### Running Tests
```bash
# Configuration test
python example_usage.py  # Select option 4

# Performance benchmark
python example_usage.py  # Select option 5

# API connectivity test
python -c "
import asyncio
from api_handler import BitcoinAPIHandler
from config import Config
import logging

async def test():
    config = Config()
    logger = logging.getLogger('Test')
    api = BitcoinAPIHandler(config.api, logger)
    result = await api.health_check()
    print(f'API Health: {result}')
    await api.close()

asyncio.run(test())
"
```

### Development Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with detailed output
python main.py
```

## 📈 Monitoring & Observability

### Application Logs
- **Structured Logging**: JSON-formatted logs for parsing
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Component Tracing**: Module-specific log identification
- **Performance Logs**: Request timing and throughput metrics

### Metrics Dashboard
The application provides built-in metrics:
- API response times and success rates
- Data collection statistics
- Email delivery confirmation
- System resource utilization

## 🔒 Security Features

### Data Protection
- **Environment Variables**: Secure credential storage
- **TLS Encryption**: Encrypted email transmission
- **Input Validation**: Comprehensive data sanitization
- **Error Handling**: No sensitive data in error messages

### API Security
- **Rate Limiting**: Prevent API abuse
- **Timeout Protection**: Prevent hanging requests
- **Error Masking**: Hide internal errors from external systems

## 🚀 Production Deployment

### Environment Setup
```bash
# Production environment variables
export LOG_LEVEL=INFO
export ENABLE_EMAIL_REPORTS=true
export TRACKING_DURATION=60

# Run in production mode
python main.py
```

### Monitoring Setup
- Monitor log files for errors and performance
- Set up alerts for failed email deliveries
- Track API response times and success rates
- Monitor disk usage for data and backup files

### Maintenance
- Regular backup verification
- Log rotation management
- Performance metrics review
- Configuration updates

## 📚 Advanced Usage

### Custom Analysis
```python
from business_logic import BitcoinPriceOrchestrator
from config import Config

# Custom tracking duration
config = Config()
config.tracking.tracking_duration_minutes = 120  # 2 hours

orchestrator = BitcoinPriceOrchestrator(config)
await orchestrator.execute_tracking_cycle()
```

### Integration with Other Systems

```python
# Custom data processing
from price_data_storage import DataStorageManager

data_manager = DataStorageManager(config.data, logger)
price_data = await data_manager.load_existing_data()

# Process data for integration
for record in price_data:
    # Custom processing logic
    pass
```

## 🤝 Contributing

This application demonstrates professional software engineering practices:

- **Clean Architecture**: Modular design with clear boundaries
- **SOLID Principles**: Single responsibility and dependency inversion
- **Design Patterns**: Factory, Singleton, Observer, Circuit Breaker
- **Professional Documentation**: Comprehensive inline and external docs
- **Error Handling**: Comprehensive exception management
- **Testing**: Built-in validation and testing capabilities

## 📄 License

This project is developed for demonstration of professional automation engineering skills.

## 👨‍💻 Author

**Senior Automation Engineer**  
*Specializing in enterprise-grade Python applications and automation solutions*

---

**Built with Python 3.8+ | Designed for Enterprise Environments | Production Ready**
