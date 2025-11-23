import json
import requests
import pytest

from scraper_base import Scraper


class MockResponse:
    def __init__(self, text='', status_code=200, raise_for_status_exc=None) -> None:
        self.text = text
        self.status_code = status_code
        self._raise_exc = raise_for_status_exc

    def raise_for_status(self):
        if self._raise_exc:
            raise self._raise_exc


class MockSession:
    def __init__(self, response=None, exc=None) -> None:
        self._response = response
        self._exc = exc

    def get(self, url, timeout=10):
        if self._exc:
            raise self._exc
        return self._response


def test_parse_raises_not_implemented() -> None:
    s = Scraper()
    with pytest.raises(NotImplementedError):
        # Scraper.parse should raise NotImplementedError by contract
        s.parse('<html></html>')


def test_fetch_html_success() -> None:
    s = Scraper(base_url='http://example.com')
    s.session = MockSession(response=MockResponse(text='OK'))
    html = s.fetch_html('/path')
    assert html == 'OK'


def test_fetch_html_request_exception() -> None:
    s = Scraper(base_url='http://example.com')
    s.session = MockSession(exc=requests.exceptions.RequestException('fail'))
    html = s.fetch_html('/path')
    assert html == ''

def test_save_data_writes_file(tmp_path) -> None:
    s = Scraper()
    s.data = [{'a': 1, 'b': 'x'}]
    filename = 'out.json'
    s.save_data(filename, folder=str(tmp_path))
    path = tmp_path / filename
    assert path.exists()
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    assert content == s.data


def test_run_calls_parse_and_collects_data(capsys) -> None:
    # Make a subclass that does not make network requests
    class DummyScraper(Scraper):
        def __init__(self):
            super().__init__(base_url='', endpoints=['/a', '/b'])

        def fetch_html(self, endpoint):
            return '<html></html>'

        def parse(self, html):
            return {'ok': True}

    ds = DummyScraper()
    ds.run()
    # Should have added two items (one for each endpoint)
    assert len(ds.data) == 2
    for item in ds.data:
        assert item == {'ok': True}
