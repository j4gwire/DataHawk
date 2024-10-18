import scrapy
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
import argparse
from datetime import datetime, timezone
import logging
import threading
import time
import random
from scrapy_selenium import SeleniumRequest  # Importing SeleniumRequest for dynamic content handling
from urllib.parse import urlparse  # To parse URLs

# Banner
def display_banner():
    banner = """
    DataHawk - OSINT Web Crawler
    ---------------------------------
    Automatic data scraping for sensitive information leaks

    Example usage:

    1. Crawl for emails (default query):
       python DataHawk.py

    2. Crawl for usernames:
       python DataHawk.py -q username

    3. Use a proxy for crawling:
       python DataHawk.py --proxy http://proxyserver:port

    4. Crawl with multithreading:
       python DataHawk.py --threads 4

    Use -h or --help for more options.
    """
    print(banner)

# Scrapy Spider class for the crawler
class OSINTSpider(scrapy.Spider):
    name = "datahawk_spider"
    
    def __init__(self, start_urls=None, query=None, proxy=None, verbose=False, *args, **kwargs):
        super(OSINTSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls if start_urls else ["http://example.com"]
        self.query = query if query else "email"
        self.proxy = proxy
        self.verbose = verbose

        # Create a unique output file name based on the domain of the first URL
        parsed_url = urlparse(self.start_urls[0])
        self.output_file = f"datahawk_results_{parsed_url.netloc.replace('.', '_')}.txt"  # Output file name

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0', 
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'
        ]

    def start_requests(self):
        for url in self.start_urls:
            user_agent = random.choice(self.user_agents)
            headers = {'User-Agent': user_agent}
            if self.proxy:
                yield SeleniumRequest(url=url, callback=self.parse, headers=headers, meta={"proxy": self.proxy}, errback=self.error_handler)
            else:
                yield SeleniumRequest(url=url, callback=self.parse, headers=headers, errback=self.error_handler)
            sleep_time = random.uniform(2, 5)  # Rate limiting (delay between requests)
            self.log(f"Sleeping for {sleep_time:.2f} seconds before next request.", level=logging.DEBUG)
            time.sleep(sleep_time)

    def parse(self, response):
        if response.status != 200:
            self.log(f"Error: Received {response.status} for URL {response.url}", level=logging.ERROR)
            return

        page_url = response.url
        page_content = response.text

        # Define regex patterns
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        username_pattern = r'@\w+'

        # Search for emails or custom query within the page content
        found_items = []
        if self.query == 'email':
            found_items = re.findall(email_pattern, page_content)
        elif self.query == 'username':
            found_items = re.findall(username_pattern, page_content)
        else:
            found_items = re.findall(self.query, page_content)

        if found_items:
            for item in found_items:
                self.save_finding(item, page_url)
        else:
            self.log(f"No data matching query '{self.query}' found on {page_url}", level=logging.INFO)
        
        # Follow pagination links intelligently
        next_pages = response.css('a.next::attr(href)').getall()  # Get all pagination links
        for next_page in next_pages:
            yield response.follow(next_page, self.parse)

    def save_finding(self, data, source_url):
        # Save findings to text file in readable format
        with open(self.output_file, 'a') as f:
            f.write(f"Data: {data}\nSource URL: {source_url}\nScraped At: {datetime.now(timezone.utc).isoformat()}\n{'-'*40}\n")
        self.log(f"Data saved: {data}", level=logging.INFO)

    def error_handler(self, failure):
        self.log(f"Request failed: {failure}", level=logging.ERROR)

    def log(self, message, level=logging.INFO):
        if self.verbose or level == logging.ERROR:
            super().log(message, level)

# Run crawler programmatically
def run_osint_crawler(start_urls, query, proxy=None, threads=1, verbose=False):
    process = CrawlerProcess(settings={
        "USER_AGENT": random.choice(['Mozilla/5.0', 'ScrapyBot/1.0']),
        "LOG_LEVEL": logging.INFO,  # Set log level
        "DOWNLOAD_DELAY": random.uniform(2, 5),  # Dynamic delay between requests
    })
    
    # Run with multiple threads
    def crawl_with_threads():
        process.crawl(OSINTSpider, start_urls=start_urls, query=query, proxy=proxy, verbose=verbose)
        process.start()
    
    # Run threads in parallel
    for _ in range(threads):
        thread = threading.Thread(target=crawl_with_threads)
        thread.start()
        thread.join()

# Argument parser for CLI options
def parse_arguments():
    parser = argparse.ArgumentParser(description="DataHawk Web Crawler: Scrape websites for data with optional proxy support.")
    parser.add_argument('-q', '--query', help='Custom query to search for (e.g., email, username)', default='email')
    parser.add_argument('--proxy', help='HTTP/HTTPS proxy to use (e.g., http://proxyserver:port)', default=None)
    parser.add_argument('--threads', type=int, help='Number of threads for multithreading', default=1)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    return parser.parse_args()

# Function to get URLs from user
def get_urls_from_user():
    urls = input("Please enter the URLs to crawl, separated by spaces: ")
    return urls.split()

# Main function
if __name__ == "__main__":
    # Display banner
    display_banner()
    
    # Parse arguments
    args = parse_arguments()
    
    # Get URLs from user if not provided in arguments
    urls = get_urls_from_user()
    
    # Run crawler with user-supplied arguments and multithreading
    run_osint_crawler(start_urls=urls, query=args.query, proxy=args.proxy, threads=args.threads, verbose=args.verbose)
