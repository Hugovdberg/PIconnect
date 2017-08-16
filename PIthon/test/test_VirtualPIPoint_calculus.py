"""Test VirtualPIPoint calculus."""
import unittest
import PIthon as PI


class TestVirtualAddition(unittest.TestCase):
    """Test VirtualPIPoint addition."""

    def test_add_integer_current_value(self):
        """Test adding an integer to a PIPoint via the current value."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            point2 = point + 1
            self.assertEqual(point.current_value + 1, point2.current_value)

    def test_add_integer_reverse_current_value(self):
        """Test adding a PIPoint to an integer via the current value."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            point2 = 1 + point
            self.assertEqual(point.current_value + 1, point2.current_value)

    def test_add_pipoints_current_value(self):
        """Test adding two PIPoints via the current value."""
        with PI.PIServer() as server:
            point_053 = server.search('L_140_053_LT053_01_Meetwaarde')[0]
            point_054 = server.search('L_140_054_LT054_01_Meetwaarde')[0]
            total = point_053 + point_054
            self.assertEqual(point_053.current_value + point_054.current_value,
                             total.current_value)
