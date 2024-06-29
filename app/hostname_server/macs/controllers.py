from flask import request, jsonify

from .. import db
from .models import Mac


def list_all_macs_controller():
    macs = Mac.query.all()
    response = []
    for mac in macs:
        response.append(mac.toDict())
    return jsonify(response)


def create_mac_controller():
    request_form = request.form.to_dict()

    new_mac = Mac(
        mac_str=request_form['mac_str'],
        mac_int=request_form['mac_int'],
        hostname_id=request_form['hostname_id'],
    )

    db.session.add(new_mac)
    db.session.commit()

    response = Mac.query.get(new_mac.id).toDict()
    return jsonify(response)


def retrieve_mac_controller(mac_id):
    response = Mac.query.get(mac_id).toDict()
    return jsonify(response)


def update_mac_controller(mac_id):
    request_form = request.form.to_dict()
    mac = Mac.query.get(mac_id)

    mac.mac_str = request_form['mac_str']
    mac.mac_int = request_form['mac_int']
    mac.hostname_id = request_form['hostname_id']

    db.session.commit()

    response = Mac.query.get(mac_id).toDict()
    return jsonify(response)


def delete_mac_controller(mac_id):
    Mac.query.filter_by(id=mac_id).delete()

    db.session.commit()

    return ("Mac with Id '{}' deleted successfully!").format(mac_id)
