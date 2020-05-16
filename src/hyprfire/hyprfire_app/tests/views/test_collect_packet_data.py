from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from hyprfire_app import views
from hyprfire_app.utils import json


def post(client, data):
    return client.post(path=reverse(views.collect_packet_data), data=data, content_type='application/json')


class CollectPacketDataTestCase(TestCase):

    def setUp(self):
        self.data = {
            'filename': 'testdump',
            'start': '1588259850.741137926',
            'end': '1588259850.747131652'
        }

    def test_correct_data(self):
        response = post(self.client, self.data)
        data = json.load_json(response.content)['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 5)

    def test_bad_request(self):
        """
        test_bad_request

        The endpoint should only accept POST requests
        """
        response = self.client.get(path=reverse(views.download_pcap_snippet),
                                   data=self.data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertEqual(str(response.reason_phrase), 'Method Not Allowed')

    def test_json_error(self):
        """
        test_json_error

        Invalid JSON should return a 400 Bad Request response
        """
        self.data = 'invalid_json'

        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)

    def test_nonexistent_file(self):
        """
        test_nonexistent_file

        A nonexistent file should return a 404 Not Found response
        """
        self.data['filename'] = 'invalidfile'
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(str(response.reason_phrase), 'File Not Found.')
