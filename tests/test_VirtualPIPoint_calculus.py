"""Test VirtualPIPoint calculus."""
# pragma pylint: disable=unused-import
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import (
    ascii,
    bytes,
    chr,
    dict,
    filter,
    hex,
    input,
    int,
    list,
    map,
    next,
    object,
    oct,
    open,
    pow,
    range,
    round,
    str,
    super,
    zip,
)

from .fakes import pi_point  # pylint: disable=unused-import

# pragma pylint: enable=unused-import


class TestVirtualAddition:
    """Test VirtualPIPoint addition."""

    def test_add_integer_current_value(self, pi_point):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = pi_point.point + 1
        assert round(point2.current_value - (pi_point.values[-1] + 1), ndigits=7) == 0

    def test_add_integer_reverse_current_value(self, pi_point):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 1 + pi_point.point
        assert round(point2.current_value - (pi_point.values[-1] + 1), ndigits=7) == 0

    def test_add_pipoints_current_value(self, pi_point):
        """Test adding two PIPoints via the current value."""
        total = pi_point.point + pi_point.point
        assert (
            round(
                total.current_value - (pi_point.values[-1] + pi_point.values[-1]),
                ndigits=7,
            )
            == 0
        )


class TestVirtualMultiplication:
    """Test VirtualPIPoint addition."""

    def test_multiply_integer_current_value(self, pi_point):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = pi_point.point * 1
        assert round(point2.current_value - (pi_point.values[-1] * 1), ndigits=7) == 0

    def test_multiply_integer_reverse_current_value(self, pi_point):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 1 * pi_point.point
        assert round(point2.current_value - (pi_point.values[-1] * 1), ndigits=7) == 0

    def test_multiply_pipoints_current_value(self, pi_point):
        """Test adding two PIPoints via the current value."""
        total = pi_point.point * pi_point.point
        assert (
            round(
                total.current_value - (pi_point.values[-1] * pi_point.values[-1]),
                ndigits=7,
            )
            == 0
        )

    def test_multiply_integer_two_current_value(self, pi_point):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = pi_point.point * 2
        assert round(point2.current_value - (pi_point.values[-1] * 2), ndigits=7) == 0

    def test_multiply_integer_two_reverse_current_value(self, pi_point):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 2 * pi_point.point
        assert round(point2.current_value - (pi_point.values[-1] * 2), ndigits=7) == 0

    def test_multiply_float_two_current_value(self, pi_point):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = pi_point.point * 2.0
        assert round(point2.current_value - (pi_point.values[-1] * 2.0), ndigits=7) == 0

    def test_multiply_float_two_reverse_current_value(self, pi_point):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 2.0 * pi_point.point
        assert round(point2.current_value - (pi_point.values[-1] * 2.0), ndigits=7) == 0
