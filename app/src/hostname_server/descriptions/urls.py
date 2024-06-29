from flask import request

from ..app import app
from .controllers import (
    list_all_descriptions_controller,
    create_description_controller,
    retrieve_description_controller,
    update_description_controller,
    delete_description_controller,
)


@app.route('/descriptions', methods=['GET', 'POST'])
def list_create_descriptions():
    if request.method == 'GET':
        return list_all_descriptions_controller()
    if request.method == 'POST':
        return create_description_controller()
    else:
        return 'Method is Not Allowed'


@app.route('/descriptions/<description_id>', methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_descriptions(description_id):
    if request.method == 'GET':
        return retrieve_description_controller(description_id)
    if request.method == 'PUT':
        return update_description_controller(description_id)
    if request.method == 'DELETE':
        return delete_description_controller(description_id)
    else:
        return 'Method is Not Allowed'
