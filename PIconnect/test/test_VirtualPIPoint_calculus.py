"""Test VirtualPIPoint calculus."""
# pragma pylint: disable=unused-import
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str,
                      ascii, chr, hex, input, next, oct, open,
                      pow, round, super,
                      filter, map, zip)
# pragma pylint: enable=unused-import

import PIconnect as PI
from PIconnect.test.fakes import VirtualTestCase

class TestVirtualAddition(VirtualTestCase):
    """Test VirtualPIPoint addition."""

    def test_add_integer_current_value(self):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = self.point + 1
        self.assertAlmostEqual(point2.current_value, self.values[-1] + 1)

    def test_add_integer_reverse_current_value(self):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 1 + self.point
        self.assertAlmostEqual(point2.current_value, self.values[-1] + 1)

    def test_add_pipoints_current_value(self):
        """Test adding two PIPoints via the current value."""
        total = self.point + self.point
        self.assertAlmostEqual(total.current_value, self.values[-1] + self.values[-1])


class TestVirtualMultiplication(VirtualTestCase):
    """Test VirtualPIPoint addition."""

    def test_multiply_integer_current_value(self):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = self.point * 1
        self.assertAlmostEqual(point2.current_value, self.values[-1] * 1)

    def test_multiply_integer_reverse_current_value(self):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 1 * self.point
        self.assertAlmostEqual(point2.current_value, self.values[-1] * 1)

    def test_multiply_pipoints_current_value(self):
        """Test adding two PIPoints via the current value."""
        total = self.point * self.point
        self.assertAlmostEqual(total.current_value, self.values[-1] * self.values[-1])

    def test_multiply_integer_two_current_value(self):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = self.point * 2
        self.assertAlmostEqual(point2.current_value, self.values[-1] * 2)

    def test_multiply_integer_two_reverse_current_value(self):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 2 * self.point
        self.assertAlmostEqual(point2.current_value, self.values[-1] * 2)

    def test_multiply_float_two_current_value(self):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = self.point * 2.0
        self.assertAlmostEqual(point2.current_value, self.values[-1] * 2.0)

    def test_multiply_float_two_reverse_current_value(self):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 2.0 * self.point
        self.assertAlmostEqual(point2.current_value, self.values[-1] * 2.0)
