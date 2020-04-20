from flask import jsonify
from urllib.error import HTTPError
from shorty.providers import *

class TestCreateShortlink:
    def shortlinks_request(self, app, data):
        client = app.test_client()
        if 'provider' not in data:
            return client.post('/shortlinks', json=dict(url=data['url']))
        else:
            return client.post('/shortlinks', json=dict(provider=data['provider'], url=data['url']))

    def mock_tinyurl(self):
        return jsonify({'link': 'link tinyurl', 'url': 'url'})

    def mock_bitly(self):
        return jsonify({'link': 'link bitly', 'url': 'url'})

    def mock_error(self):
        raise HTTPError('http://url.com', 500, 'Internal Error', {}, None)

    def test_bitly(self, app, monkeypatch):
        monkeypatch.setattr(Bitly, "call_service", self.mock_bitly)

        response = self.shortlinks_request(app, {'provider': 'bitly', 'url': 'url'})
        assert b'bitly' in response.data
        assert response.status_code == 200

    def test_tinyurl(self, app, monkeypatch):
        monkeypatch.setattr(Tinyurl, "call_service", self.mock_tinyurl)

        response = self.shortlinks_request(app, {'provider': 'tinyurl', 'url': 'url'})
        assert b'tinyurl' in response.data
        assert response.status_code == 200

    def test_invalid_provider(self, app, monkeypatch):
        monkeypatch.setattr(Bitly, "call_service", self.mock_bitly)

        response = self.shortlinks_request(app, {'provider': 'invalid_provider', 'url': 'url'})
        assert b'invalid provider' in response.data
        assert response.status_code == 400

    def test_default(self, app, monkeypatch):
        monkeypatch.setattr(Bitly, "call_service", self.mock_bitly)

        response = self.shortlinks_request(app, {'url': 'url'})
        assert b'bitly' in response.data
        assert response.status_code == 200

    def test_fallback(self, app, monkeypatch):
        monkeypatch.setattr(Tinyurl, "call_service", self.mock_error)
        monkeypatch.setattr(Bitly, "call_service", self.mock_bitly)

        response = self.shortlinks_request(app, {'provider': 'tinyurl', 'url': 'url'})
        assert b'bitly' in response.data
        assert response.status_code == 200