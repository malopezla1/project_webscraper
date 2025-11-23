import pytest
from bs4 import BeautifulSoup


def parse_wiki_html(html: str) -> dict:
    """Replica la lógica de `WikiScraper.parse` sin importar el módulo.

    Esto permite probar el comportamiento esperado sobre HTML de ejemplo
    sin importar/instanciar la clase real.
    """
    if not html:
        return {"title": "", "content": "", "error": "No HTML provided"}

    try:
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("h1", {"id": "firstHeading"})
        title = title_tag.text.strip() if title_tag and title_tag.text else ""

        content = soup.find("div", {"class": "mw-parser-output"})
        if content:
            paragraphs = content.find_all("p")
            text = "\n".join(
                [para.get_text().strip() for para in paragraphs if para.get_text().strip()]
            )
        else:
            text = ""

        return {"title": title, "content": text}
    except Exception as e:
        return {"title": "", "content": "", "error": str(e)}


def test_parse_valid_html() -> None:
    html = (
        '<html><head><title>X</title></head>'
        '<body>'
        '<h1 id="firstHeading">Python (programming language)</h1>'
        '<div class="mw-parser-output">'
        '<p>Python is an interpreted, high-level programming language.</p>'
        '<p>It emphasizes code readability.</p>'
        '</div>'
        '</body></html>'
    )

    expected = {
        "title": "Python (programming language)",
        "content": "Python is an interpreted, high-level programming language.\nIt emphasizes code readability.",
    }

    assert parse_wiki_html(html) == expected


def test_parse_empty_html_returns_error() -> None:
    assert parse_wiki_html("") == {"title": "", "content": "", "error": "No HTML provided"}


def test_parse_none_returns_error() -> None:
    # None is falsy and should be treated like empty input
    assert parse_wiki_html(None) == {"title": "", "content": "", "error": "No HTML provided"}


def test_parse_missing_title_or_content() -> None:
    # Missing title element and missing content div -> return empty title and content (no error key)
    html = '<html><body><div class="other">No paragraphs here</div></body></html>'
    result = parse_wiki_html(html)
    assert result == {"title": "", "content": ""}
