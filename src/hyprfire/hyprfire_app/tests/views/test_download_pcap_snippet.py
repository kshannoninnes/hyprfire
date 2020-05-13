from decimal import Decimal

from django.urls import reverse
from django.test import TestCase

from hyprfire_app import views


def post(client, data):
    return client.post(path=reverse(views.download_pcap_snippet), data=data, content_type='application/json')


class DownloadPcapSnippetTests(TestCase):

    def setUp(self):
        self.data = {
            'filename': 'testdump',
            'start': 1588259869.842212489,
            'end': 1588259869.845959007
            }

    """ SUCCESS TEST CASES """

    def test_zero_start(self):
        self.data['start'] = 0
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'],
                         f'attachment; filename="{self.data["filename"]}-filtered.pcap"')

    """ FAIL TEST CASES """

    def test_bad_request(self):
        response = self.client.get(path=reverse(views.download_pcap_snippet),
                                   data=self.data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertEqual(str(response.reason_phrase), 'Method Not Allowed')

    def test_nonexistent_file(self):
        self.data['filename'] = 'invalidfile'
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(str(response.reason_phrase), 'File Not Found.')

    def test_timestamp_wrong_type(self):
        self.data['start'] = 'Hello World'
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'Invalid timestamp. Are you sure it\'s a valid number?')

    def test_negative_start(self):
        self.data['start'] = -1
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'Start timestamp must be on or after the unix epoch ("0")')

    def test_early_end(self):
        self.data['end'] = -1
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'End timestamp must be greater than start timestamp')

    def test_infinite_start(self):
        self.data['start'] = Decimal("inf")
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'Timestamps cannot be infinite')

    def test_infinite_end(self):
        self.data['end'] = Decimal("inf")
        response = post(self.client, self.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.reason_phrase), 'Timestamps cannot be infinite')

