from flask import request, jsonify

from .. import db
from .models import Description


def list_all_descriptions_controller():
    descriptions = Description.query.all()
    response = []
    for description in descriptions:
        response.append(description.toDict())
    return jsonify(response)


def create_description_controller():
    request_form = request.form.to_dict()

    new_description = Description(
        text=request_form['text'],
        client=request_form['client'],
        hostname_id=request_form['hostname_id'],
    )

    db.session.add(new_description)
    db.session.commit()

    response = Description.query.get(new_description.id).toDict()
    return jsonify(response)


def retrieve_description_controller(description_id):
    response = Description.query.get(description_id).toDict()
    return jsonify(response)


def update_description_controller(description_id):
    request_form = request.form.to_dict()
    description = Description.query.get(description_id)

    description.text = request_form['text']
    description.client = request_form['client']
    description.hostname_id = request_form['hostname_id']

    db.session.commit()

    response = Description.query.get(description_id).toDict()
    return jsonify(response)


def delete_description_controller(description_id):
    Description.query.filter_by(id=description_id).delete()

    db.session.commit()

    return ("Description with Id '{}' deleted successfully!").format(description_id)
