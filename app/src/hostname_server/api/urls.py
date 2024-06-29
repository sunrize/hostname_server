from flask import request

from ..app import app
from .controllers import (
    post_get_hostname,
)


@app.route("/api/get_hostname", methods=["POST"])
def api_post_get_hostname():
    if request.method == 'POST':
        if request.json is not None:
            return post_get_hostname(request)
        else:
            return 'JSON is None'
    else:
        return 'Method is Not Allowed'