from decimal import Decimal

from django.urls import reverse
from django.test import TestCase

from hyprfire_app import views


def post(client, data):
    return client.post(path=reverse(views.download_pcap_snippet), data=data, content_type='application/json')


class DownloadPcapSnippetTests(TestCase):

    def setUp(self):
        """
        setUp

        Ensure we have a valid data set before each test
        """
        self.data = {
            'filename': 'testdump',
            'start': '1588259869.842212489',
            'end': '1588259869.845959007'
            }

    def test_zero_start(self):
        """
        test_zero_start

        A timestamp value of zero is considered valid
        """
        self.data['start'] = 0
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'],
                         f'attachment; filename="{self.data["filename"]}-filtered.pcap"')

    """ FAIL TEST CASES """

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

    def test_timestamp_wrong_type(self):
        """
        test_timestamp_wrong_type

        An incorrect type being passed as a timestamp should return a 400 Bad Request response
        """
        self.data['start'] = 'Hello World'
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'Invalid timestamp. Are you sure it\'s a valid number?')

    def test_negative_start(self):
        """
        test_negative_start

        A negative start timestamp should return a 400 Bad Request response
        """
        self.data['start'] = -1
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'Start timestamp must be on or after the unix epoch ("0")')

    def test_early_end(self):
        """
        test_early_end

        An end timestamp less than the start timestamp should return a 400 Bad Request response
        """
        self.data['end'] = -1
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'End timestamp must be greater than start timestamp')

    def test_infinite_start(self):
        """
        test_infinite_start

        An infinite start timestamp should return a 400 Bad Request response
        """
        self.data['start'] = Decimal("inf")
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'Timestamps cannot be infinite')

    def test_infinite_end(self):
        """
        test_infinite_end

        An infinite end timestamp should return a 400 Bad Request response
        """
        self.data['end'] = Decimal("inf")
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'Timestamps cannot be infinite')

