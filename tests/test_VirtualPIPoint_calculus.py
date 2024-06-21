"""Test VirtualPIPoint calculus."""

from .fakes import VirtualTestCase  # pylint: disable=unused-import


class TestVirtualAddition:
    """Test VirtualPIPoint addition."""

    def test_add_integer_current_value(self, pi_point: VirtualTestCase):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = pi_point.point + 1
        cur_value1 = pi_point.values[-1] + 1
        try:
            cur_value2 = point2.current_value
        except Exception as e:
            raise AttributeError(
                f"Error in current_value (type {type(e)!r}, attribute: {type(point2)})"
            ) from e
        assert round(cur_value2 - cur_value1, ndigits=7) == 0

    def test_add_integer_reverse_current_value(self, pi_point: VirtualTestCase):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 1 + pi_point.point
        assert round(point2.current_value - (pi_point.values[-1] + 1), ndigits=7) == 0

    def test_add_pipoints_current_value(self, pi_point: VirtualTestCase):
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

    def test_multiply_integer_current_value(self, pi_point: VirtualTestCase):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = pi_point.point * 1
        assert round(point2.current_value - (pi_point.values[-1] * 1), ndigits=7) == 0

    def test_multiply_integer_reverse_current_value(self, pi_point: VirtualTestCase):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 1 * pi_point.point
        assert round(point2.current_value - (pi_point.values[-1] * 1), ndigits=7) == 0

    def test_multiply_pipoints_current_value(self, pi_point: VirtualTestCase):
        """Test adding two PIPoints via the current value."""
        total = pi_point.point * pi_point.point
        assert (
            round(
                total.current_value - (pi_point.values[-1] * pi_point.values[-1]),
                ndigits=7,
            )
            == 0
        )

    def test_multiply_integer_two_current_value(self, pi_point: VirtualTestCase):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = pi_point.point * 2
        assert round(point2.current_value - (pi_point.values[-1] * 2), ndigits=7) == 0

    def test_multiply_integer_two_reverse_current_value(self, pi_point: VirtualTestCase):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 2 * pi_point.point
        assert round(point2.current_value - (pi_point.values[-1] * 2), ndigits=7) == 0

    def test_multiply_float_two_current_value(self, pi_point: VirtualTestCase):
        """Test adding an integer to a PIPoint via the current value."""
        point2 = pi_point.point * 2.0
        assert round(point2.current_value - (pi_point.values[-1] * 2.0), ndigits=7) == 0

    def test_multiply_float_two_reverse_current_value(self, pi_point: VirtualTestCase):
        """Test adding a PIPoint to an integer via the current value."""
        point2 = 2.0 * pi_point.point
        assert round(point2.current_value - (pi_point.values[-1] * 2.0), ndigits=7) == 0
