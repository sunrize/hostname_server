#!/bin/python
#
# Script for returning hostnames
#

import random
import string
import re
import unicodedata
import os
import os.path
import sys
import sqlite3
import namer
from sqlalchemy import create_engine

from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import abort
from flask import g

# Environment settings overwrite the defaults
DATA_DIRECTORY = (
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    if "HOSTNAME_SERVER_DATA_DIRECTORY" not in os.environ
    else os.path.join(os.environ["HOSTNAME_SERVER_DATA_DIRECTORY"], "", "")
)
# HOSTNAME_DIGITS = (
#     4 if "HOSTNAME_SERVER_DIGITS" not in os.environ else int(os.environ["HOSTNAME_SERVER_DIGITS"])
# )
# HOSTNAME_START = (
#     1 if "HOSTNAME_SERVER_START" not in os.environ else int(os.environ["HOSTNAME_SERVER_START"])
# )
# HOSTNAME_PATTERN = (
#     "host%i" if "HOSTNAME_SERVER_PATTERN" not in os.environ else os.environ["HOSTNAME_SERVER_PATTERN"]
# )
# HOSTNAME_RANDOM_LENGTH = (
#     8
#     if "HOSTNAME_SERVER_RANDOM_LENGTH" not in os.environ
#     else int(os.environ["HOSTNAME_SERVER_RANDOM_LENGTH"])
# )
LISTEN_IP = (
    "0.0.0.0"
    if "HOSTNAME_SERVER_LISTEN_IP" not in os.environ
    else os.environ["HOSTNAME_SERVER_LISTEN_IP"]
)
LISTEN_PORT = (
    5000
    if "HOSTNAME_SERVER_LISTEN_PORT" not in os.environ
    else int(os.environ["HOSTNAME_SERVER_LISTEN_PORT"])
)

db_file = os.path.join(DATA_DIRECTORY, "hostname.db") # SQLite
schema_file = os.path.join("./", "schema.sql")

# con = sqlite3.connect(db_file)
# cur = con.cursor()
# con.close()

app = Flask(__name__)

import hostname_server.views

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(db_file)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(schema_file, mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def query_db_lastrowid(query, args=()):
    cur = get_db().execute(query, args)
    rv = cur.lastrowid
    cur.close()
    return rv


def queryscript_db(query):
    cur = get_db().executescript(query)
    rv = cur.fetchall()
    cur.close()
    return rv


def mac_to_int(mac):
    res = re.match("^((?:(?:[0-9a-f]{2})[:-]){5}[0-9a-f]{2})$", mac.lower())
    if res is None:
        raise ValueError("invalid mac address")
    return int(res.group(0).replace(":", ""), 16)


def int_to_mac(macint):
    if type(macint) != int:
        raise ValueError("invalid integer")
    return ":".join(
        ["{}{}".format(a, b) for a, b in zip(*[iter("{:012x}".format(macint))] * 2)]
    )


if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)
if not os.path.exists(db_file):  # and os.path.exists(schema_file):
    # print("CREATE DB FILE")
    init_db()
# else:
#     print("DB FILE EXISTS")


# # Generate a filename from a string
# # normalized, lowercase and without whitespaces, please
# def create_csv_filename(input_string):
#     """Create a filename based on a given string."""
#     valid_filename = re.sub(r"\%i", "_0", input_string) + ".csv"
#     #    input_string = unicodedata.normalize('NFKD', input_string).encode('ascii', 'ignore')
#     #    input_string = unicode(re.sub(r'[^\w\s-]', '', input_string).strip().lower())
#     #    filename = unicode(re.sub(r'[-\s]+', '-', input_string)) + '.csv'
#     return str(valid_filename)


# # Write the hostname to a file
# def write_hostname_to_file(filename, input_string):
#     """Write a string to a given filename, append only."""
#     file_object = open(filename, "a")
#     file_object.write(input_string + "\n")
#     file_object.close()


# # Search for a string in a file.
# # Return true if found, or false if not found
# def find_string_in_file(filename, search_string):
#     """Check if a given file contains a string"""
#     # If the file does not exist, the string canno be found, ergo false
#     if not os.path.exists(filename):
#         return False
#     else:
#         if search_string in open(filename).read():
#             return True
#         else:
#             return False


# # Search a file for the highest integer in a line
# # and return the value
# def get_max_value_from_file(filename):
#     """Search a file for the highest integer value and return it"""
#     values = []
#     hostname_file = open(filename)
#     for line in hostname_file:
#         values.append(int(re.findall("\d+", line)[0]))
#     hostname_file.close()
#     return max(values)


# @app.route("/hostname_server/api/v1.0/generate", methods=["GET"])
# def get_generate():
#     """generate a hostname based on the default settings"""
#     pattern = HOSTNAME_PATTERN
#     hostname = pattern.replace("%i", str(HOSTNAME_START).zfill(HOSTNAME_DIGITS))
#     filename_for_hostname = create_csv_filename(pattern)
#     hostname_exists = find_string_in_file(
#         DATA_DIRECTORY + filename_for_hostname, hostname
#     )
#     if hostname_exists is True:
#         new_hostnumber = (
#             get_max_value_from_file(DATA_DIRECTORY + filename_for_hostname) + 1
#         )
#         hostname = pattern.replace("%i", str(new_hostnumber).zfill(HOSTNAME_DIGITS))

#     hostname = str(hostname)
#     write_hostname_to_file(DATA_DIRECTORY + filename_for_hostname, hostname)
#     return jsonify({"hostname": hostname})


# # Generate a hostname with the API and POST settings
# @app.route("/hostname_server/api/v1.0/generate", methods=["POST"])
# def post_generate():
#     """Generate a uniq hostname"""
#     if not request.json or not "pattern" in request.json:
#         abort(400)
#     else:
#         pattern = request.json.get("pattern")

#     # Set the number of digits
#     if "digits" in request.json:
#         digits = request.json.get("digits")
#     else:
#         digits = 4

#     # Set the start decimal
#     if "start" in request.json:
#         start_number = str(request.json.get("start")).zfill(digits)
#     else:
#         start_number = str(1).zfill(digits)

#     # Build the initial hostname
#     hostname = pattern.replace("%i", str(start_number))
#     filename_for_hostname = create_csv_filename(pattern)
#     hostname_exists = find_string_in_file(
#         DATA_DIRECTORY + filename_for_hostname, hostname
#     )
#     if (
#         hostname_exists
#     ):  # Find the highest one and add one. Replace the hostname pattern then.
#         new_hostnumber = (
#             get_max_value_from_file(DATA_DIRECTORY + filename_for_hostname) + 1
#         )
#         hostname = pattern.replace("%i", str(new_hostnumber).zfill(digits))

#     hostname = str(hostname)
#     write_hostname_to_file(DATA_DIRECTORY + filename_for_hostname, hostname)
#     return jsonify({"hostname": hostname})


### completely new macs
def get_hostname_when_new(macs_int, client="", description="", postx=""):
    hostname = None
    ### fetch hostname
    px = namer.prefix()
    safe_description = description.replace("'", "''")
    query = "insert into hostname (prefix,description) values ('{0}','{1}')".format(
        px, safe_description
    )
    id = query_db_lastrowid(query)
    hostname = namer.hostname(px, id, client, postx)
    ### insert
    query_arg = ",".join(
        ['("{0}",{1},{2})'.format(int_to_mac(mi), mi, id) for mi in macs_int]
    )
    query = "insert into macs (mac_str, mac_int, hostname_id) values {0}".format(
        query_arg
    )
    query_res = queryscript_db(query)

    query = "insert or ignore into description (text, client, hostname_id) values ('{0}','{1}',{2})".format(
        safe_description, client, id
    )
    query_res = queryscript_db(query)
    return hostname, description


def get_hostname_when_exists(query_res, client="", description=""):
    res_hostname = None
    id = query_res[0]["hostname_id"]
    if id is not None:
        query = "select * from hostname where id is {0}".format(id)
        query_res = query_db(query, one=True)
        prex = query_res["prefix"]
        postx = query_res["postfix"] if query_res["postfix"] is not None else ""
        res_description = (
            query_res["description"] if query_res["description"] is not None else ""
        )
        res_hostname = namer.hostname(prex, id, client, postx)

        safe_description = description.replace("'", "''")
        query = "insert or ignore into description (text, client, hostname_id) values ('{0}','{1}',{2})".format(
            safe_description, client, id
        )
        query_res = queryscript_db(query)
    else:
        pass
    return res_hostname, res_description


# Generate a hostname with the API and POST settings
@app.route("/hostname_server/api/v1.1/generate", methods=["POST"])
def post_generate_macs():
    """Generate a uniq hostname"""
    if not request.json or not "macs" in request.json:
        abort(400)
    else:
        macs = request.json.get("macs")
        client = request.json.get("client")
        description = request.json.get("description")
        # print(macs)

    res_hostname = None
    res_description = None

    if len(macs) != 0:
        res_hostname = None

        macs_int = set(map(mac_to_int, macs))
        query_arg = ",".join(map(str, macs_int))
        query = "select * from macs where mac_int in ({0})".format(query_arg)
        query_res = query_db(query)
        print(query)
        print(len(query_res))

        if len(query_res) == 0:
            res_hostname, res_description = get_hostname_when_new(
                macs_int, client, description
            )
        else:
            res_hostname, res_description = get_hostname_when_exists(
                query_res, client, description
            )
    else:
        abort(400)
    # for macs_rows in query_res:
    #     print(macs_rows["mac_str"], "has the id", macs_rows["hostname_id"])

    # # Set the number of digits
    # if 'digits' in request.json:
    #     digits = request.json.get('digits')
    # else:
    #     digits = 4

    # # Set the start decimal
    # if 'start' in request.json:
    #     start_number = str(request.json.get('start')).zfill(digits)
    # else:
    #     start_number = str(1).zfill(digits)

    # Build the initial hostname
    # hostname = pattern.replace('%i', str(start_number))
    # filename_for_hostname = create_csv_filename(pattern)
    # hostname_exists = find_string_in_file(DATA_DIRECTORY + filename_for_hostname, hostname)
    # if hostname_exists: # Find the highest one and add one. Replace the hostname pattern then.
    #     new_hostnumber = get_max_value_from_file(DATA_DIRECTORY + filename_for_hostname) + 1
    #     hostname = pattern.replace('%i', str(new_hostnumber).zfill(digits))

    # hostname = str(hostname)
    # write_hostname_to_file(DATA_DIRECTORY + filename_for_hostname, hostname)
    if res_hostname == None or res_description == None:
        abort(400)

    return jsonify({"hostname": res_hostname, "description": res_description})


# # Get a random hostname string
# @app.route("/hostname_server/api/v1.0/random", methods=["GET"])
# def get_random():
#     """Return a completely random hostname"""
#     random_hostname = "".join(
#         random.choice(string.ascii_uppercase + string.digits)
#         for _ in range(HOSTNAME_RANDOM_LENGTH)
#     ).lower()
#     write_hostname_to_file(DATA_DIRECTORY + "hostname_random.csv", random_hostname)
#     return jsonify({"hostname": random_hostname})


# Error handling
@app.errorhandler(404)
def not_found(error):
    """Handing 404 messages"""
    error_message = {
        "error": "Not found.",
        "info": "Try POST: http//:<host>:<port>/hostname_server/api/v1.1/generate",
        "url": "hostname_server",
    }
    return make_response(jsonify(error_message), 404)


if __name__ == "__main__":
    # app.run(host=LISTEN_IP, port=LISTEN_PORT)
    # app.run(debug=True)
    app.run()
