import json
from json import JSONDecodeError

from hyprfire_app.exceptions import JSONError


def load_json(request_body):
    try:
        return json.loads(request_body)
    except JSONDecodeError:
        raise JSONError('Could not decode JSON.')


def validate_json_length(data, expected_length):
    if len(data) != expected_length:
        raise JSONError('Invalid parameters.')
