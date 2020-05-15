from django.test import TestCase

from scapy.layers.inet import IP, TCP

from hyprfire_app.new_scripts.packet_manipulator import packet


class CustomScapyTest(TestCase):
    def setUp(self):
        """
        setUp

        Create a fake packet object to pass into test methods
        """
        self.test_packet = IP(ttl=64) / TCP()

        self.test_packet.time = 123
        self.test_packet.category = 'TCP'
        self.test_packet.src = '127.0.0.2'
        self.test_packet.dst = '127.0.0.3'
        self.test_packet.sport = 80
        self.test_packet.dport = 443

    def test_correct_timestamp(self):
        """
        test_correct_timestamp

        get_timestamp should return '123'
        """
        res = packet.get_timestamp(self.test_packet)
        expected_time = str(self.test_packet.time)

        self.assertEqual(expected_time, res)

    def test_correct_category(self):
        """
        test_correct_category

        get_category should return 'TCP'
        """
        res = packet.get_category(self.test_packet)
        expected_category = self.test_packet.category

        self.assertEqual(expected_category, res)

    def test_correct_ip_data(self):
        """
        test_correct_ip_data

        get_ip_data should return a dict with two keys:
            src: 127.0.0.2
            dst: 127.0.0.3
        """
        res = packet.get_ip_data(self.test_packet)
        expected_ip_data = {
            'src': self.test_packet.src,
            'dst': self.test_packet.dst
        }

        self.assertEqual(expected_ip_data['src'], res['src'])
        self.assertEqual(expected_ip_data['dst'], res['dst'])

    def test_correct_transport_data(self):
        """
        test_correct_transport_data

        get_transport_data should return a dict with two keys:
            src_port: 80 (http)
            dst_port: 443 (https)
        """
        res = packet.get_transport_data(self.test_packet)
        expected_sport = f'{self.test_packet.sport} (http)'
        expected_dport = f'{self.test_packet.dport} (https)'

        self.assertEqual(expected_sport, res['src_port'])
        self.assertEqual(expected_dport, res['dst_port'])
