"""Test VirtualPIPoint calculus."""
# Copyright 2017 Hugo van den Berg, Stijn de Jong

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# pragma pylint: disable=unused-import
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (
    bytes,
    dict,
    int,
    list,
    object,
    range,
    str,
    ascii,
    chr,
    hex,
    input,
    next,
    oct,
    open,
    pow,
    round,
    super,
    filter,
    map,
    zip,
)

# pragma pylint: enable=unused-import

from .fakes import pi_point  # pylint: disable=unused-import


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
