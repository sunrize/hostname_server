from flask import request, jsonify
from sqlalchemy import exc
import logging

from .. import db
from ..macs.models import Mac
from ..hostnames.models import Hostname
from ..descriptions.models import Description
from .. import namer


def get_hostname_when_macs_new(macs_int, client="", description="", postfix=None):
    generated_hostname = None
    ### Generate hostname
    prefix = namer.prefix()
    # # safe_description = description.replace("'", "''") # SQLite

    # Add new Hostname and get it's id
    new_hostname = Hostname(
        prefix=prefix,
        postfix=postfix,
        description=description,
    )
    db.session.add(new_hostname)
    db.session.commit()

    new_id = new_hostname.id
    # response = Hostname.query.get(new_hostname.id).toDict()
    generated_hostname = namer.hostname(prefix, new_id, client, postfix)

    ### Add new Mac
    for mac_int in macs_int:
        new_mac = Mac(
            mac_str=namer.int_to_mac(mac_int),
            mac_int=mac_int,
            hostname_id=new_id,
        )
        db.session.add(new_mac)
    db.session.commit()
    
    ### Add new Description
    new_description = Description(
        text=description,
        client=client,
        hostname_id=new_id,
    )

    try:
        db.session.add(new_description)
        db.session.commit()
    except exc.SQLAlchemyError as error:
        logging.error("An error occurred: %s", error)
        db.session.rollback()
        
    return generated_hostname, description

def get_hostname_when_macs_already_exist(hostname_id, client="", description=""):
    result_hostname = None
    result_description = None

    if hostname_id is not None:
        query_response_dict = Hostname.query.get(hostname_id).toDict()
        
        prefix = query_response_dict["prefix"]
        postfix = query_response_dict["postfix"] if query_response_dict["postfix"] is not None else ""
        result_description = (
            query_response_dict["description"] if query_response_dict["description"] is not None else ""
        )
        result_hostname = namer.hostname(prefix, hostname_id, client, postfix)


        # # safe_description = description.replace("'", "''") #SQLite
        ### Add new Description
        new_description = Description(
            text=description,
            client=client,
            hostname_id=hostname_id,
        )
        
        try:
            db.session.add(new_description)
            db.session.commit()
        except exc.SQLAlchemyError as error:
            logging.error("An error occurred: %s", error)
            db.session.rollback()
    else:
        pass
    return result_hostname, result_description

def post_get_hostname(request):
    """Generate a unique hostname"""
    if not request.json or not "macs" in request.json:
        abort(400)
    else:
        macs = request.json.get("macs")
        client = request.json.get("client") if request.json.get("client") != None else ""
        description = request.json.get("description") if request.json.get("description") != None else ""
        postfix = request.json.get("postfix")

    result_hostname = None
    result_description = None

    if len(macs) != 0:
        result_hostname = None
        macs_int = set(map(namer.mac_to_int, macs))

        # Query exiscting macs

        query_result = Mac.query.filter(Mac.mac_int.in_(macs_int)).first()
                
        if query_result is None:
            result_hostname, result_description = get_hostname_when_macs_new(
                macs_int, client, description, postfix
            )
        else:
            query_result_dict = query_result.toDict()
            hostname_id = query_result_dict['hostname_id']
            result_hostname, result_description = get_hostname_when_macs_already_exist(
                hostname_id, client, description
            )
    else:
        abort(400)

    if result_hostname == None or result_description == None:
        abort(400)

    return jsonify({"hostname": result_hostname, "description": result_description})


# def list_all_descriptions_controller():
#     descriptions = Description.query.all()
#     response = []
#     for description in descriptions:
#         response.append(description.toDict())
#     return jsonify(response)


# def create_description_controller():
#     request_form = request.form.to_dict()

#     new_description = Description(
#         text=request_form['text'],
#         client=request_form['client'],
#         hostname_id=request_form['hostname_id'],
#     )

#     db.session.add(new_description)
#     db.session.commit()

#     response = Description.query.get(new_description.id).toDict()
#     return jsonify(response)


# def retrieve_description_controller(description_id):
#     response = Description.query.get(description_id).toDict()
#     return jsonify(response)


# def update_description_controller(description_id):
#     request_form = request.form.to_dict()
#     description = Description.query.get(description_id)

#     description.text = request_form['text']
#     description.client = request_form['client']
#     description.hostname_id = request_form['hostname_id']

#     db.session.commit()

#     response = Description.query.get(description_id).toDict()
#     return jsonify(response)


# def delete_description_controller(description_id):
#     Description.query.filter_by(id=description_id).delete()

#     db.session.commit()

#     return ("Description with Id '{}' deleted successfully!").format(description_id)
