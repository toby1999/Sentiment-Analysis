from flask import escape
import pandas as pd

def helloWorld(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <
http://flask.pocoo.org/docs/1.0/api/#flask.Request
>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <
http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response
>.
    """
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data

    elif content_type == 'text/plain':
        name = request.data

    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    return 'Hello world {}!'.format(escape(name))
