from flask import request

from ..app import app
from .controllers import (
    list_all_macs_controller,
    create_mac_controller,
    retrieve_mac_controller,
    update_mac_controller,
    delete_mac_controller,
)


@app.route('/macs', methods=['GET', 'POST'])
def list_create_macs():
    if request.method == 'GET':
        return list_all_macs_controller()
    if request.method == 'POST':
        return create_mac_controller()
    else:
        return 'Method is Not Allowed'


@app.route('/macs/<mac_id>', methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_macs(mac_id):
    if request.method == 'GET':
        return retrieve_mac_controller(mac_id)
    if request.method == 'PUT':
        return update_mac_controller(mac_id)
    if request.method == 'DELETE':
        return delete_mac_controller(mac_id)
    else:
        return 'Method is Not Allowed'
