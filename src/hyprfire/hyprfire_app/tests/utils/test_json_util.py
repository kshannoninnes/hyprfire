import json

from hyprfire_app.exceptions import JSONError
from hyprfire_app.utils.json import load_json, validate_json_length

from django.test import TestCase


class JsonUtilsTestCase(TestCase):
    def test_correct_json_loads(self):
        json_data = {
            'name': 'hello'
        }

        res = load_json(json.dumps(json_data))

        self.assertEqual(res, json_data)

    def test_incorrect_json_excepts(self):
        self.assertRaises(JSONError, load_json, 'incorrect_json')

    def test_invalid_length_excepts(self):
        json_data = {
            'name': 'one',
            'name2': 'two'
        }

        self.assertRaises(JSONError, validate_json_length, json.loads(json.dumps(json_data)), 3)
