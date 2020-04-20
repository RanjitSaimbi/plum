from flask import jsonify
from shorty.providers import *
from unittest import mock

class TestCreateShortlink:
    def test_format_response(self):
        response = Response().format_response('long url', 'link')
        data, status_code = response
        assert b'long url' in data.data
        assert b'link' in data.data
        assert status_code == 200
    
