from django.test import TestCase, Client


def get_url(filename='testdump', start='1588259869.842212489', end='1588259869.845959007'):
    return f'/download/{filename}/{start}/{end}/'


class DownloadPcapSnippetTests(TestCase):

    def setUp(self):
        """
        setUp

        Ensure we have a valid data set before each test
        """
        self.client = Client()
        self.data = {
            'filename': 'testdump',
            'start': '1588259869.842212489',
            'end': '1588259869.845959007'
            }

    def test_correct_request_returns_file_download(self):
        """
        test_correct

        A valid request should return a file download
        """
        response = self.client.get(get_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'],
                         f'attachment; filename="{self.data["filename"]}-filtered.pcap"')

    def test_non_get_request_returns_405_response(self):
        """
        test_non_get_request_returns_405_response

        A request type of anything other than GET should return a 405 response
        """
        response = self.client.post(get_url())

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.reason_phrase, 'Method Not Allowed')

    def test_bad_filename_returns_404(self):
        """
        test_bad_filename_returns_404

        A bad filename should return a 404 File Not Found response
        """
        response = self.client.get(get_url(filename='BADFILE'))

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
        response = self.client.get(f'/download/testdump/')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.reason_phrase, 'Not Found')

