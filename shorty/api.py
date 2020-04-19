from flask import Blueprint, jsonify, request
from urllib.error import HTTPError
import shorty.services as services
from shorty.services import Bitly
import importlib, inspect

api = Blueprint('api', __name__)

@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
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
        request_data = request.get_json()
        service = 'service' in request_data
        url = 'url' in request_data
        invalid_service = request_data['service'].capitalize() not in dir(services) if service else False

        if not url:
            return jsonify({'response': 'url not specified'}), 400

        if invalid_service:
            return jsonify({'response': 'invalid service specified'}), 400
        
        if service:
            service = getattr(services, request_data['service'].capitalize())
            instance = service(request_data)
            try:
                return instance.call_service()
            except HTTPError as e:
                return fallback(request_data)
        else:
            return default(request_data).call_service()
    
    return response()


