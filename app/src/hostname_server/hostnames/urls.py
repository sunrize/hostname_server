from flask import request

from ..app import app
from .controllers import (
    list_all_hostnames_controller,
    create_hostname_controller,
    retrieve_hostname_controller,
    update_hostname_controller,
    delete_hostname_controller,
)


@app.route('/hostnames', methods=['GET', 'POST'])
def list_create_hostnames():
    if request.method == 'GET':
        return list_all_hostnames_controller()
    if request.method == 'POST':
        return create_hostname_controller()
    else:
        return 'Method is Not Allowed'


@app.route('/hostnames/<hostname_id>', methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_hostnames(hostname_id):
    if request.method == 'GET':
        return retrieve_hostname_controller(hostname_id)
    if request.method == 'PUT':
        return update_hostname_controller(hostname_id)
    if request.method == 'DELETE':
        return delete_hostname_controller(hostname_id)
    else:
        return 'Method is Not Allowed'
