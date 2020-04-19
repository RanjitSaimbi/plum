from flask import jsonify
from shorty.tiny_url import TinyUrl

class TestCreateShortlink:
    def shortlinks_request(self, app, data):
        client = app.test_client()
        return client.post('/shortlinks', json=dict(service=data['service']))

    def mock_tinyurl(self):
        return jsonify({'service': 'tinyurl'})

    def mock_bitly(self):
        return jsonify({'service': 'bitly'})

    def test_bitly(self, app):
        response = self.shortlinks_request(app, {'service': 'bitly'})
        assert b'bitly' in response.data
        assert response.status_code == 200

    def test_tinyurl(self, app, monkeypatch):
        monkeypatch.setattr(TinyUrl, "call_service", self.mock_tinyurl)

        response = self.shortlinks_request(app, {'service': 'tinyurl'})
        assert b'tinyurl' in response.data
        assert response.status_code == 200

    def test_default(self, app):
        response = self.shortlinks_request(app, {'service': 'invalid_service'})
        assert b'bitly' in response.data
        assert response.status_code == 200