from django.test import TestCase, Client
from hyprfire_app.utils import json


def get_url(filename='testdump', start='1588259869.842212489', end='1588259869.845959007'):
    return f'/collect/{filename}/{start}/{end}/'


class CollectPacketDataTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_correct_request_returns_valid_dict(self):
        """
        test_correct_request_returns_valid_dict

        A correct get request should return an HttpResponse containing a dictionary with a list of packet details
        """
        response = self.client.get(get_url())
        data = json.load_json(response.content)['packet_data_list']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 10)

    def test_incorrect_request_returns_405_response(self):
        """
        test_incorrect_request_returns_405_response

        The endpoint should only accept GET requests
        """
        response = self.client.post(get_url())

        self.assertEqual(response.status_code, 405)
        self.assertEqual(str(response.reason_phrase), 'Method Not Allowed')

    def test_nonexistent_file_returns_404_response(self):
        """
        test_nonexistent_file

        A nonexistent file should return a 404 Not Found response
        """
        response = self.client.get(get_url(filename='invalidfile'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(str(response.reason_phrase), 'File Not Found.')

    def test_bad_timestamp_format_returns_400_response(self):
        """
        test_bad_timestamp_format_returns_400_response

        A bad timestamp format should return a 400 Timestamp must be a number response
        """
        response = self.client.get(get_url(start='hello world'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.reason_phrase, 'Timestamp must be a number')

    def test_missing_url_parameter_returns_404_response(self):
        """
        test_missing_url_parameter_returns_404_response

        An invalid URL should return a 404 Not Found response
        """
        response = self.client.get(f'/collect/testdump/')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.reason_phrase, 'Not Found')
