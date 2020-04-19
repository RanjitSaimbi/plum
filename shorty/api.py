from flask import Blueprint, request
from shorty.shortlink_controller import ShortlinkController

api = Blueprint('api', __name__)

@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    request_data = request.get_json()
    return ShortlinkController(request_data).call()



