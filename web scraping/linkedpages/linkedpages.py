import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv

def get_linked_pages(url):
    # Fetch the HTML content of the page
    response = requests.get(url)
    if response.status_code == 200:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract all anchor tags
        links = soup.find_all('a')
        linked_pages = set()
        for link in links:
            href = link.get('href')
            if href and href.startswith('http'):  # Filter out absolute URLs
                parsed_url = urlparse(href)
                if parsed_url.netloc == urlparse(url).netloc:  # Filter out external links
                    linked_pages.add(href)
            elif href:  # Relative URLs
                absolute_url = urljoin(url, href)
                linked_pages.add(absolute_url)
        return linked_pages
    else:
        print("Failed to fetch page:", response.status_code)
        return None

# Example usage:
if __name__ == "__main__":
    url = input("Enter URL: ")
    linked_pages = get_linked_pages(url)
    if linked_pages:
        output_filename = "linked_pages.csv"
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Linked Pages"])
            for page in linked_pages:
                writer.writerow([page])
        print(f"Linked pages saved to {output_filename}")
