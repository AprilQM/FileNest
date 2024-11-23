from flask import Blueprint, jsonify, request, send_from_directory, abort
from werkzeug.utils import safe_join
import os

from app.api import api

@api.route('/get_ui_creator/<device>/<ui_name>', methods=['GET'])
def status(device, ui_name):
    base_path = os.path.abspath(f'app/static/js/UIcreator/{device}/')
    if os.path.exists(safe_join(base_path, ui_name)):
        return send_from_directory(base_path, ui_name)
    else:
        return abort(404)
            
# @main.route('/api/UIcreator', methods=['POST'])