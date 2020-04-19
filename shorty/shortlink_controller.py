from flask import Blueprint, jsonify, request
from urllib.error import HTTPError
import shorty.services as services
from shorty.services import Bitly
import importlib, inspect

class ShortlinkController(object):
    def __init__(self, request_data):
        self.request_data = request_data

    def call(self):
        default = Bitly

        def fallback(request_data):
            service = request_data['service'].capitalize()
            for name, cls in inspect.getmembers(importlib.import_module('shorty.services'), inspect.isclass):
                if cls.__module__ == 'shorty.services' and name != service:
                    try:
                        service = getattr(services, name)
                        return service(request_data).call_service()
                    except HTTPError as e:
                        return jsonify({'response': 'services failed'}), 400

        def response():
            service = 'service' in self.request_data
            url = 'url' in self.request_data
            invalid_service = self.request_data['service'].capitalize() not in dir(services) if service else False

            if not url:
                return jsonify({'response': 'url not specified'}), 400

            if invalid_service:
                return jsonify({'response': 'invalid service specified'}), 400
            
            if service:
                service = getattr(services, self.request_data['service'].capitalize())
                instance = service(self.request_data)
                try:
                    return instance.call_service()
                except HTTPError as e:
                    return fallback(self.request_data)
            else:
                return default(self.request_data).call_service()
        
        return response()
