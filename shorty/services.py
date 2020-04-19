from flask import jsonify, request

class Tinyurl(object):
    def __init__(self, request_data):
        self.request_data = request_data

    def call_service(self):
        return jsonify({'response': 'tinyurl'})

class Bitly(object):
    def __init__(self, request_data):
        self.request_data = request_data

    def call_service(self):
        return jsonify({'response': 'bitly'})