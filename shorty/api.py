from flask import Blueprint, jsonify, request


api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    shortlink_services = {}
    service = lambda f: shortlink_services.setdefault(f.__name__, f)

    @service
    def tinyurl():
        return jsonify({'response': 'tinyurl'})

    @service
    def bitly():
        return jsonify({'response': 'bitly'})

    def default():
        return bitly()

    def my_main():
        request_data = request.get_json()

        return shortlink_services[request_data['service']]()

    return my_main()