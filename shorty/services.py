from flask import Blueprint, jsonify, request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import urllib
import urllib.request
import json
import ssl
import os

class Response(object):
    def format_response(self, long_url, link):
        return jsonify(
            {
                'url': long_url,
                'link': link
                }
            ), 200

class Tinyurl(Response):
    def __init__(self, request_data):
        self.TINY_URL = "http://tinyurl.com/api-create.php?url="
        self.request_data = request_data
        self.long_url = self.request_data['url']
        self.URL = self.TINY_URL + self.long_url

    def call_service(self):
        response = urllib.request.urlopen(self.URL)
        link = str(BeautifulSoup(response, 'html.parser'))
        return self.format_response(self.long_url, link)
    

class Bitly(Response):
    auth_token = os.environ.get('TOKEN')
    BITLY_URL = "https://api-ssl.bitly.com/v4/shorten"

    def __init__(self, request_data):
        self.request_data = request_data
        self.long_url = self.request_data['url']
        self.data = {
            "domain": "bit.ly",
            "long_url": self.long_url
        }

    def add_headers(self, request, jsondataasbytes):
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header('Authorization', self.auth_token)
        request.add_header('Content-Length', len(jsondataasbytes))

    def convert_data(self, data):
        jsondata = json.dumps(data)
        return jsondata.encode('utf-8')

    def call_service(self):
        request = urllib.request.Request(self.BITLY_URL)
        jsondataasbytes = self.convert_data(self.data)
        self.add_headers(request, jsondataasbytes)
        response = urllib.request.urlopen(request, jsondataasbytes, context=ssl.SSLContext())
        link = json.loads(str(BeautifulSoup(response, 'html.parser')))['link']
        return self.format_response(self.long_url, link)