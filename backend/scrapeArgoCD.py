import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def scrape_argo_docs(base_url):
    docs = []
    visited_links = set()  # To track visited links and avoid duplicates

    # Fetch the main page content
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to fetch URL: {base_url}")
        return docs

    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape all links to documentation pages
    # Adjust link filtering to account for relative paths
    links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True) if a['href'].startswith('/en/stable/')]

    links = list(set(links))  # Remove duplicates

    # Fetch content from each documentation link
    for link in links:
        if link in visited_links:
            continue  # Skip already visited links

        page_response = requests.get(link)
        if page_response.status_code != 200:
            print(f"Failed to fetch URL: {link}")
            continue

        page_soup = BeautifulSoup(page_response.content, "html.parser")

        # Extract the title and content
        title = page_soup.find("h1").get_text(strip=True) if page_soup.find("h1") else "Untitled"
        content = "\n".join([p.get_text(strip=True) for p in page_soup.find_all("p")])

        if content:  # Only include pages with content
            docs.append({"title": title, "content": content})

        visited_links.add(link)

    return docs

# Example usage
base_url = "https://argo-cd.readthedocs.io/en/stable/#what-is-argo-cd"
argo_docs = scrape_argo_docs(base_url)

# Save the scraped documentation to a file
with open("argo_docs.json", "w") as f:
    json.dump(argo_docs, f, indent=4)

print(f"Scraped {len(argo_docs)} pages of documentation.")