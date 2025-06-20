# Web Scraping Project - Claude Configuration

## Project Overview
This is a web scraping project designed for automated data extraction from websites, APIs, and online sources. The project emphasizes ethical scraping practices, robust error handling, and efficient data processing with respect for website terms of service and rate limits.

**Key Technologies:**
- **Requests**: HTTP library for simple web requests and API calls
- **BeautifulSoup**: HTML/XML parsing and data extraction
- **Scrapy**: High-performance web crawling framework
- **Selenium**: Browser automation for JavaScript-heavy sites
- **Playwright**: Modern browser automation with better performance
- **aiohttp**: Async HTTP client for concurrent scraping
- **pandas**: Data manipulation and analysis for scraped data
- **SQLAlchemy**: Database ORM for data storage

## Architecture & Patterns

### Directory Structure
```
project/
├── src/
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py              # Base scraper classes
│   │   ├── simple/              # Simple request-based scrapers
│   │   │   ├── __init__.py
│   │   │   ├── news_scraper.py
│   │   │   └── product_scraper.py
│   │   ├── browser/             # Browser-based scrapers
│   │   │   ├── __init__.py
│   │   │   ├── selenium_scraper.py
│   │   │   └── playwright_scraper.py
│   │   └── crawlers/            # Scrapy crawlers
│   │       ├── __init__.py
│   │       ├── spiders/
│   │       ├── items.py
│   │       ├── pipelines.py
│   │       ├── middlewares.py
│   │       └── settings.py
│   ├── extractors/              # Data extraction logic
│   │   ├── __init__.py
│   │   ├── text_extractor.py
│   │   ├── image_extractor.py
│   │   ├── link_extractor.py
│   │   └── structured_data.py
│   ├── storage/                 # Data storage handlers
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── file_storage.py
│   │   └── cloud_storage.py
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── rate_limiter.py
│   │   ├── proxy_manager.py
│   │   ├── user_agents.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── config/                  # Configuration modules
│       ├── __init__.py
│       ├── settings.py
│       └── logging_config.py
├── data/
│   ├── raw/                     # Raw scraped data
│   ├── processed/               # Cleaned and processed data
│   ├── exports/                 # Final export files
│   └── cache/                   # Cached responses
├── configs/                     # Configuration files
│   ├── scrapers/               # Scraper-specific configs
│   ├── proxies.json            # Proxy configurations
│   └── user_agents.txt         # User agent strings
├── tests/                      # Test files
│   ├── test_scrapers/
│   ├── test_extractors/
│   └── fixtures/               # Test HTML files
├── scripts/                    # Utility scripts
│   ├── run_scraper.py          # Script runner
│   └── data_processor.py       # Data processing
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

### Web Scraping Patterns
- **Respectful scraping**: Rate limiting, robots.txt compliance, terms of service respect
- **Error resilience**: Retry logic, fallback strategies, graceful degradation
- **Data validation**: Schema validation, data quality checks, duplicate detection
- **Modular design**: Separate concerns (scraping, extraction, storage, processing)
- **Configuration-driven**: External configs for URLs, selectors, and parameters
- **Monitoring**: Logging, metrics, and alerting for scraping operations
- **Anti-detection**: User agent rotation, proxy support, request timing variation

## Development Workflow

### Common Commands
```bash
# Simple scraping with requests
python -m scrapers.simple.news_scraper --config configs/news.json
python scripts/run_scraper.py --scraper product --limit 100

# Scrapy framework
scrapy startproject project_name
scrapy genspider spider_name domain.com
scrapy crawl spider_name
scrapy crawl spider_name -o output.json
scrapy crawl spider_name -s LOG_LEVEL=INFO

# Browser automation
python -m scrapers.browser.selenium_scraper --headless
python -m scrapers.browser.playwright_scraper --browser chromium

# Data processing
python scripts/data_processor.py --input data/raw/ --output data/processed/
python -m storage.database --migrate
python -m storage.database --seed

# Testing
pytest tests/
pytest tests/test_scrapers/ -v
pytest --cov=src tests/
pytest -k "test_extraction" --verbose

# Code quality
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
bandit src/                     # Security scanning

# Monitoring and debugging
python -m utils.rate_limiter --test
python -m utils.proxy_manager --check
tail -f logs/scraper.log
```

### Development Process
1. **Target analysis** - Study website structure, robots.txt, and terms of service
2. **Strategy selection** - Choose appropriate scraping method (requests, browser, Scrapy)
3. **Data modeling** - Define data structures and validation schemas
4. **Scraper implementation** - Build extraction logic with error handling
5. **Rate limiting setup** - Implement respectful request timing
6. **Data pipeline** - Build storage and processing workflows
7. **Testing** - Unit tests and integration tests with mock data
8. **Monitoring setup** - Logging, metrics, and alerting
9. **Deployment** - Scheduling and production monitoring

### Git Workflow
- **Feature branches**: `feature/add-ecommerce-scraper`
- **Scraper organization**: Separate commits for different website scrapers
- **Configuration management**: Version control for scraper configs
- **Data exclusion**: Never commit scraped data, only sample/test data
- **Security**: Never commit API keys, credentials, or sensitive configs

## Code Quality & Standards

### Python Code Style
- **Follow PEP 8** with Black formatting
- **Type hints**: Use for all function parameters and returns
- **Docstrings**: Google style with examples for scraper functions
- **Error handling**: Comprehensive exception handling with logging
- **Async patterns**: Use async/await for concurrent scraping when possible

### Web Scraping Ethics
- **Respect robots.txt**: Always check and follow robots.txt rules
- **Rate limiting**: Implement appropriate delays between requests
- **Terms of service**: Review and comply with website terms
- **Data usage**: Use scraped data responsibly and legally
- **Attribution**: Provide proper attribution when required
- **Privacy**: Respect user privacy and data protection laws

### Code Organization Standards
- **Modular scrapers**: One scraper per website or data source
- **Reusable components**: Extract common functionality to base classes
- **Configuration-driven**: Use external configs for URLs and selectors
- **Error isolation**: Isolate failures to prevent cascade issues
- **Data validation**: Validate all extracted data before storage
- **Logging**: Comprehensive logging for debugging and monitoring

## Testing Strategy

### Test Types
```python
# Unit tests for extraction logic
def test_text_extraction():
    html = "<div class='content'>Test content</div>"
    soup = BeautifulSoup(html, 'html.parser')
    extractor = TextExtractor()
    result = extractor.extract(soup, '.content')
    assert result == "Test content"

# Integration tests with mock responses
@responses.activate
def test_scraper_with_mock():
    responses.add(
        responses.GET,
        'https://example.com/data',
        body=load_fixture('sample_page.html'),
        status=200
    )
    
    scraper = NewsScraper()
    results = scraper.scrape('https://example.com/data')
    assert len(results) > 0
    assert 'title' in results[0]

# Browser automation tests
def test_selenium_scraper(webdriver):
    scraper = SeleniumScraper(webdriver)
    results = scraper.scrape_dynamic_content('https://example.com')
    assert results is not None
    assert len(results) > 0
```

### Test Data Management
- **Fixtures**: Save sample HTML files for consistent testing
- **Mock responses**: Use responses library for HTTP request mocking
- **Browser testing**: Use headless browsers for automated testing
- **Data validation**: Test data schemas and validation rules
- **Error scenarios**: Test network failures, malformed HTML, and rate limits

## Environment Variables

### Scraping Configuration
```bash
# Request settings
SCRAPER_USER_AGENT=Mozilla/5.0 (compatible; Scraper/1.0)
SCRAPER_TIMEOUT=30
SCRAPER_MAX_RETRIES=3
SCRAPER_RETRY_DELAY=5
SCRAPER_RATE_LIMIT=1.0

# Proxy settings
PROXY_ENABLED=false
PROXY_HTTP=http://proxy.example.com:8080
PROXY_HTTPS=https://proxy.example.com:8080
PROXY_ROTATION=true

# Browser automation
SELENIUM_BROWSER=chrome
SELENIUM_HEADLESS=true
SELENIUM_WINDOW_SIZE=1920x1080
PLAYWRIGHT_BROWSER=chromium
PLAYWRIGHT_HEADLESS=true

# Storage settings
DATABASE_URL=sqlite:///scraped_data.db
DATA_DIR=./data
CACHE_DIR=./data/cache
CACHE_ENABLED=true
CACHE_TTL=3600

# External services
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=scraped-data-bucket

# Monitoring
LOG_LEVEL=INFO
LOG_FILE=logs/scraper.log
METRICS_ENABLED=true
SENTRY_DSN=https://your-sentry-dsn
```

### Anti-Detection Settings
```bash
# User agent rotation
USER_AGENT_ROTATION=true
USER_AGENT_LIST_FILE=configs/user_agents.txt

# Request timing
REQUEST_DELAY_MIN=1
REQUEST_DELAY_MAX=3
REQUEST_JITTER=0.5

# Session management
SESSION_ROTATION=true
SESSION_REQUESTS_LIMIT=100
COOKIE_PERSISTENCE=true
```

## Scrapy Framework Integration

### Scrapy Settings
```python
# settings.py
BOT_NAME = 'web_scraper'
SPIDER_MODULES = ['src.scrapers.crawlers.spiders']
NEWSPIDER_MODULE = 'src.scrapers.crawlers.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure delays
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = 0.5 * DOWNLOAD_DELAY

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# User agent
USER_AGENT = 'web_scraper (+http://www.yourdomain.com)'

# Item pipelines
ITEM_PIPELINES = {
    'src.scrapers.crawlers.pipelines.ValidationPipeline': 300,
    'src.scrapers.crawlers.pipelines.DuplicatesPipeline': 400,
    'src.scrapers.crawlers.pipelines.DatabasePipeline': 500,
}

# Middlewares
DOWNLOADER_MIDDLEWARES = {
    'src.scrapers.crawlers.middlewares.ProxyMiddleware': 350,
    'src.scrapers.crawlers.middlewares.UserAgentMiddleware': 400,
}
```

### Scrapy Spider Example
```python
import scrapy
from src.scrapers.crawlers.items import ArticleItem

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['example-news.com']
    start_urls = ['https://example-news.com/articles']
    
    def parse(self, response):
        # Extract article links
        article_links = response.css('.article-link::attr(href)').getall()
        
        for link in article_links:
            yield response.follow(link, self.parse_article)
        
        # Follow pagination
        next_page = response.css('.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_article(self, response):
        item = ArticleItem()
        item['title'] = response.css('h1::text').get()
        item['content'] = response.css('.article-content::text').getall()
        item['author'] = response.css('.author::text').get()
        item['published_date'] = response.css('.date::text').get()
        item['url'] = response.url
        
        yield item
```

## Browser Automation Patterns

### Selenium Integration
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumScraper:
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def scrape_dynamic_content(self, url):
        self.driver.get(url)
        
        # Wait for dynamic content to load
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dynamic-content'))
        )
        
        # Extract data
        elements = self.driver.find_elements(By.CSS_SELECTOR, '.data-item')
        data = []
        
        for element in elements:
            item = {
                'title': element.find_element(By.CSS_SELECTOR, '.title').text,
                'description': element.find_element(By.CSS_SELECTOR, '.desc').text
            }
            data.append(item)
        
        return data
    
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
```

### Playwright Integration
```python
from playwright.async_api import async_playwright

class PlaywrightScraper:
    async def scrape_spa_content(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set user agent and viewport
            await page.set_user_agent('Mozilla/5.0 (compatible; Scraper/1.0)')
            await page.set_viewport_size({'width': 1920, 'height': 1080})
            
            await page.goto(url)
            
            # Wait for content to load
            await page.wait_for_selector('.content-loaded')
            
            # Extract data
            data = await page.evaluate('''
                () => {
                    const items = document.querySelectorAll('.data-item');
                    return Array.from(items).map(item => ({
                        title: item.querySelector('.title')?.textContent,
                        description: item.querySelector('.desc')?.textContent
                    }));
                }
            ''')
            
            await browser.close()
            return data
```

## Critical Rules

### Legal & Ethical Requirements
- ⚠️ **ALWAYS** read and comply with robots.txt files
- ⚠️ **ALWAYS** review website terms of service before scraping
- ⚠️ **NEVER** scrape personal or sensitive information without permission
- ⚠️ **ALWAYS** implement appropriate rate limiting and delays
- ⚠️ **NEVER** overwhelm servers with excessive requests
- ⚠️ **ALWAYS** respect copyright and intellectual property rights
- ⚠️ **NEVER** use scraped data for malicious purposes

### Technical Requirements
- ⚠️ **ALWAYS** handle HTTP errors and network failures gracefully
- ⚠️ **ALWAYS** implement retry logic with exponential backoff
- ⚠️ **NEVER** hardcode URLs or selectors without configuration
- ⚠️ **ALWAYS** validate and sanitize extracted data
- ⚠️ **ALWAYS** log all scraping activities for debugging and monitoring
- ⚠️ **NEVER** ignore SSL certificate errors in production
- ⚠️ **ALWAYS** use appropriate user agents and headers

### Data Handling Requirements
- ⚠️ **NEVER** commit scraped data to version control
- ⚠️ **ALWAYS** implement data deduplication mechanisms
- ⚠️ **ALWAYS** validate data schemas before storage
- ⚠️ **NEVER** store sensitive data without encryption
- ⚠️ **ALWAYS** implement data retention and cleanup policies
- ⚠️ **NEVER** mix scraped data with different schemas

### Security Requirements
- ⚠️ **NEVER** commit API keys or credentials to version control
- ⚠️ **ALWAYS** use environment variables for sensitive configuration
- ⚠️ **ALWAYS** sanitize all user inputs and extracted data
- ⚠️ **NEVER** execute arbitrary code from scraped content
- ⚠️ **ALWAYS** use secure connections (HTTPS) when possible
- ⚠️ **NEVER** trust external content without validation

## Common Commands Reference

### Daily Development
```bash
# Run simple scraper
python -m scrapers.simple.news_scraper --config configs/news.json

# Run Scrapy spider
scrapy crawl news_spider -o data/raw/news.json

# Process scraped data
python scripts/data_processor.py --input data/raw/ --output data/processed/

# Check proxy status
python -m utils.proxy_manager --check-all

# Monitor scraping logs
tail -f logs/scraper.log | grep ERROR
```

### Testing and Debugging
```bash
# Run tests with coverage
pytest --cov=src tests/ --cov-report=html

# Test specific scraper
pytest tests/test_scrapers/test_news_scraper.py -v

# Debug with verbose logging
python -m scrapers.simple.news_scraper --config configs/debug.json --log-level DEBUG

# Validate robots.txt compliance
python -m utils.validators --check-robots https://example.com
```

### Data Management
```bash
# Clean and deduplicate data
python scripts/data_processor.py --deduplicate --input data/raw/

# Export to different formats
python scripts/data_processor.py --export csv --input data/processed/
python scripts/data_processor.py --export json --input data/processed/

# Database operations
python -m storage.database --create-tables
python -m storage.database --import data/processed/
```

## Claude-Specific Instructions

### Code Generation Preferences
- **Always** include robots.txt checking and rate limiting
- **Always** implement comprehensive error handling and retries
- **Include** proper data validation and schema checking
- **Add** logging for all scraping operations and errors
- **Use** appropriate scraping libraries (requests, BeautifulSoup, Scrapy)
- **Include** user agent rotation and anti-detection measures
- **Add** configuration files for URLs, selectors, and parameters

### Scraper Implementation
- **Start** with robots.txt compliance checking
- **Include** rate limiting and respectful request timing
- **Add** data extraction with CSS selectors or XPath
- **Use** proper session management and cookie handling
- **Include** data validation and cleaning logic
- **Add** storage mechanisms (database, file, cloud)
- **Implement** monitoring and alerting capabilities

### Ethical Considerations
- **Always** emphasize legal and ethical scraping practices
- **Include** terms of service compliance checking
- **Add** data usage guidelines and attribution requirements
- **Use** appropriate rate limiting to avoid server overload
- **Include** privacy considerations and data protection
- **Add** guidelines for responsible data usage and sharing

### Error Handling Focus
- **Include** network error handling and retry logic
- **Add** HTML parsing error recovery
- **Use** graceful degradation for missing elements
- **Include** data validation and schema enforcement
- **Add** logging for debugging and monitoring
- **Implement** alerting for critical failures and issues