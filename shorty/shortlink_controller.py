from flask import Blueprint, jsonify, request
from urllib.error import HTTPError
import shorty.providers as providers
from shorty.providers import Bitly
import importlib, inspect

class ShortlinkController(object):
    def __init__(self, request_data):
        self.request_data = request_data

    def call(self):
        default = Bitly

        def fallback(request_data):
            provider= request_data['provider'].capitalize()
            for name, cls in inspect.getmembers(importlib.import_module('shorty.providers'), inspect.isclass):
                if cls.__module__ == 'shorty.providers' and (name != provider and name != 'Response'):
                    try:
                        provider = getattr(providers, name)
                        return provider(request_data).call_service()
                    except HTTPError as e:
                        return jsonify({'response': 'all providers failed'}), 400

        def response():
            provider = 'provider' in self.request_data
            url = 'url' in self.request_data
            invalid_provider = self.request_data['provider'].capitalize() not in dir(providers) if provider else False

            if not url:
                return jsonify({'response': 'url not specified'}), 400

            if invalid_provider:
                return jsonify({'response': 'invalid provider specified'}), 400
            
            if provider:
                try:
                    provider = getattr(providers, self.request_data['provider'].capitalize())
                    instance = provider(self.request_data)
                    return instance.call_service()
                except HTTPError as e:
                    return fallback(self.request_data)
            else:
                return default(self.request_data).call_service()
        
        return response()
