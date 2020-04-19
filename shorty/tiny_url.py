from flask import jsonify, request

class TinyUrl(object):
    def __init__(self, request_data):
        self.request_data = request_data

    def call_service(self):
        return jsonify({'response': 'tinyurl'})