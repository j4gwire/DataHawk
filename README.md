# DataHawk - OSINT Web Crawler

**DataHawk** is a OSINT web crawler designed to automate the extraction of sensitive information from websites. This tool can scrape email addresses, usernames, and other specified queries, making it invaluable for researchers, cybersecurity professionals, and data analysts.

## Features

- **Customizable Queries**: Specify the type of data to search for (default is email).
- **Dynamic Content Handling**: Scrapes websites that use JavaScript to render content.
- **Intelligent Pagination Support**: Follows pagination links to gather data from multiple pages.
- **User-Agent Management**: Uses random user agents to avoid detection.
- **Rate Limiting**: Implements dynamic delays to mimic human behavior.
- **Multi-threading**: Supports concurrent requests for faster crawling.
- **Error Handling & Logging**: Robust logging for easier troubleshooting.

## Installation

To use **DataHawk**, clone the repository and install the required dependencies:

```
git clone https://github.com/ScribeAegis/DataHawk.git
```
## Install Requirements
```
pip install -r requirements.txt
```
## Usage
```
python DataHawk.py [options]
```

## Options

-q, --query: Custom query to search for (e.g., email, username). Default is 'email'.
--proxy: HTTP/HTTPS proxy to use (e.g., http://proxyserver:port).
--threads: Number of threads for multithreading (default is 1).

## Crawl for emails (default query):
```
python DataHawk.py
```
## Crawl for usernames:
```
python DataHawk.py -q username
```
## Use a proxy for crawling:
```
python DataHawk.py --proxy http://proxyserver:port
```
## Crawl with multithreading:
```
python DataHawk.py --threads 4
```
## Getting Started
To get started, run the crawler and follow the prompts to enter the URLs you wish to crawl. The results will be saved in datahawk_results.txt.

## Disclaimer
**DataHawk** is intended for educational purposes, research, and ethical testing only. Do not use this tool against websites without proper authorization. Misuse of this tool may be illegal and is solely the responsibility of the user.

## Contributing
If you would like to contribute to DataHawk, please fork the repository and submit a pull request with your changes. For any issues, feel free to open an issue in the GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
