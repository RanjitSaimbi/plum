from flask import jsonify

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

    def test_tinyurl(self, app):
        response = self.shortlinks_request(app, {'service': 'tinyurl'})
        assert b'tinyurl' in response.data
        assert response.status_code == 200