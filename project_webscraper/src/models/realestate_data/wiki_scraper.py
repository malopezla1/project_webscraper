from scraper_base import Scraper
from bs4 import BeautifulSoup

class WikiScraper(Scraper):
    """
    Scraper for Wikipedia pages.
    Extracts the title and main paragraphs of the content.
    """
    def __init__(self, base_url="https://en.wikipedia.org", endpoints=None) -> None:
        super().__init__(base_url=base_url, endpoints=endpoints or ["/wiki/Web_scraping"])

    def parse(self, html: str) -> dict:
        """Parses the HTML and returns the title and content of the page."""

        if not html:
            return {"title": "", "content": "", "error": "No HTML provided"}

        try:
            soup = BeautifulSoup(html, "html.parser")
            # Title: may not exist in atypical pages
            title_tag = soup.find("h1", {"id": "firstHeading"})
            title = title_tag.text.strip() if title_tag and title_tag.text else ""

            # Main content: ensure it exists before looking for paragraphs
            content = soup.find("div", {"class": "mw-parser-output"})
            if content:
                paragraphs = content.find_all("p")
                # Ignore empty paragraphs and clean text
                text = "\n".join(
                    [para.get_text().strip() for para in paragraphs if para.get_text().strip()]
                )
            else:
                text = ""

            return {"title": title, "content": text}
        except Exception as e:
            # Return consistent structure and error message for debugging
            return {"title": "", "content": "", "error": str(e)}
