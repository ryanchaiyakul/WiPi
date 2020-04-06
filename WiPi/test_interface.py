import unittest
from unittest import mock

from .interface import Interface


class MockInterface(Interface):

    def update(self):
        super().update()


class TestInterface(unittest.TestCase):

    def test_interface(self):
        # Cannot test interface validity
        if len(MockInterface._Interface__interfaces) == 0:
            return

        # initializes as ''
        blank = MockInterface()
        self.assertEqual(blank.interface, '')

        # interface should be '' if deleted
        del blank.interface
        self.assertEqual(blank.interface, '')

        if not bool(Interface.get_interfaces()):
            # Cannot check validation
            blank.interface = "does not matter"
            self.assertEqual(blank.interface, "does not matter")
        else:

            # Checking validation
            valid_interface = next(iter(Interface.get_interfaces()))
            blank.interface = valid_interface
            self.assertEqual(blank.interface, valid_interface)

            # Unique interface
            multi = MockInterface(valid_interface)
            self.assertEqual(multi.interface, '')

            # Valid interface
            multi.interface = "should not work"
            self.assertEqual(multi.interface, '')

            # Does del correctly remove block
            del blank.interface
            multi.interface = valid_interface
            self.assertEqual(multi.interface, valid_interface)

            del multi.interface
            self.assertEqual(multi.interface, '')
