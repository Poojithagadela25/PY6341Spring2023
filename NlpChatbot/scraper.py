import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.content, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
            tag.decompose()

        if "wikipedia.org" in url:
            content = soup.find("div", {"id": "mw-content-text"})
            if content:
                text = "\n".join(p.get_text(strip=True) for p in content.find_all("p"))
            else:
                return ""
        else:
            content = soup.find("main") or soup.find("article") or soup.body
            text = content.get_text(separator="\n", strip=True) if content else ""

        clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        if len(clean_text.split()) < 50:
            return ""
        return clean_text
    except Exception as e:
        print(f"[SCRAPER EXCEPTION] {e}")
        return ""
