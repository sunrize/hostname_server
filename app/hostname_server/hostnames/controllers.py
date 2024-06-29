from flask import request, jsonify

from .. import db
from .models import Hostname


def list_all_hostnames_controller():
    hostnames = Hostname.query.all()
    response = []
    for hostname in hostnames:
        response.append(hostname.toDict())
    return jsonify(response)


def create_hostname_controller():
    request_form = request.form.to_dict()

    new_hostname = Hostname(
        prefix=request_form['prefix'],
        postfix=request_form['postfix'],
        description=request_form['description'],
    )

    db.session.add(new_hostname)
    db.session.commit()

    response = Hostname.query.get(new_hostname.id).toDict()
    return jsonify(response)


def retrieve_hostname_controller(hostname_id):
    response = Hostname.query.get(hostname_id).toDict()
    return jsonify(response)


def update_hostname_controller(hostname_id):
    request_form = request.form.to_dict()
    hostname = Hostname.query.get(hostname_id)

    hostname.prefix = request_form['prefix']
    hostname.postfix = request_form['postfix']
    hostname.description = request_form['description']

    db.session.commit()

    response = Hostname.query.get(hostname_id).toDict()
    return jsonify(response)


def delete_hostname_controller(hostname_id):
    Hostname.query.filter_by(id=hostname_id).delete()

    db.session.commit()

    return ("Hostname with Id '{}' deleted successfully!").format(hostname_id)
