import unittest

from .wifi import Wifi


class TestWifi(unittest.TestCase):

    def test_status(self):
        # blank interface
        blank = Wifi()
        self.assertEqual(blank.status, {})
        interface = next(iter(Wifi.get_interfaces()))
        blank.interface = interface
        blank.update()