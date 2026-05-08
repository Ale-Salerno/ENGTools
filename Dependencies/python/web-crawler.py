import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os


def get_urls_from_input():
    """
    Prompt the user to input one or more URLs (comma-separated) and return a list of clean URLs.
    """
    raw = input("Enter one or more starting URLs (comma-separated): ")
    urls = [url.strip() for url in raw.split(',') if url.strip()]
    return urls


def prompt_depth():
    """
    Ask the user for maximum crawl depth (integer >= 1).
    """
    while True:
        try:
            depth = int(input("Enter maximum crawl depth (>=1): "))
            if depth >= 1:
                return depth
            print("Depth must be at least 1.")
        except ValueError:
            print("Please enter a valid integer.")


def is_valid_link(link):
    """
    Check if the link is a valid HTTP/HTTPS URL.
    """
    parsed = urlparse(link)
    return parsed.scheme in ('http', 'https')


def crawl(start_urls, max_depth):
    """
    Crawl starting from each URL up to max_depth.
    Prints and saves visited page URLs and HTML content.
    """
    visited = set()
    to_visit = [(url, 1) for url in start_urls]

    # Create output directory
    output_dir = 'crawled_pages'
    os.makedirs(output_dir, exist_ok=True)

    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue

        print(f"Crawling ({depth}/{max_depth}): {url}")
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            visited.add(url)
            continue

        # Save HTML content
        safe_name = url.replace('://', '_').replace('/', '_')
        file_path = os.path.join(output_dir, f"{safe_name}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

        visited.add(url)

        # Parse links and enqueue
        soup = BeautifulSoup(response.text, 'html.parser')
        for link_tag in soup.find_all('a', href=True):
            link = link_tag['href']
            absolute_link = urljoin(url, link)
            if is_valid_link(absolute_link) and absolute_link not in visited:
                to_visit.append((absolute_link, depth + 1))

    print(f"\nCrawling finished. {len(visited)} pages visited. HTML saved in '{output_dir}/'")


if __name__ == '__main__':
    start_urls = get_urls_from_input()
    depth = prompt_depth()
    crawl(start_urls, depth)
