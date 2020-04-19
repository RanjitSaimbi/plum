from flask import Blueprint, jsonify, request
from shorty.tiny_url import TinyUrl
from shorty.bitly import Bitly
from urllib.error import HTTPError

api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    shortlink_services = {}
    service = lambda f: shortlink_services.setdefault(f.__name__, f)

    @service
    def tinyurl():
        request_data = request.get_json()
        return TinyUrl(request_data).call_service()

    @service
    def bitly():
        request_data = request.get_json()
        return Bitly(request_data).call_service()

    def default():
        return bitly()

    def call_fallback(service):
        del shortlink_services[service]

        for service in shortlink_services.keys():
            try:
                return shortlink_services[service]()
            except HTTPError as e:
                return jsonify({'response': 'services failed'}), 400

    def my_main():
        request_data = request.get_json()
        missing_service = 'service' not in request_data
        # Prelim decision to fallback to default if invalid service provided
        invalid_service = request_data['service'] not in shortlink_services.keys() if not missing_service else None

        if missing_service or invalid_service:
            return default()
        try:
            return shortlink_services[request_data['service']]()
        except HTTPError as e:
            return call_fallback(request_data['service'])

    return my_main()