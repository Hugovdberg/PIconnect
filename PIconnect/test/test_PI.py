""" PIconnect.test.test_PI
    Test communication with the PI System.
"""
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

import datetime
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

# pragma pylint: enable=unused-import

import PIconnect as PI
import pytest
import pytz
from PIconnect.test.fakes import pi_point  # pylint: disable=unused-import


class TestServer:
    """Test connecting to the server"""

    def test_connection(self):
        """Test that creating a PI.PIServer object without arguments raises no exception"""
        PI.PIServer()

    def test_server_name(self):
        """Test that the server reports the same name as which was connected to."""
        server = PI.PIServer("Testing")
        assert server.server_name == "Testing"

    def test_warn_unkown_server(self):
        """Test that the server reports a warning when an unknown host is specified."""
        server_names = [name for name in PI.PIServer.servers]
        server_name = "__".join(server_names + ["UnknownHostName"])
        with pytest.warns(UserWarning):
            PI.PIServer(server_name)

    def test_repr(self):
        """Test that the server representation matches the connected server."""
        server = PI.PIServer("Testing")
        assert repr(server) == "PIServer(\\\\Testing)"


class TestSearchPIPoints:
    """Test searching for PI Points on the default server."""

    def test_search_single_string(self):
        """Test searching for PI points using a single string."""
        with PI.PIServer() as server:
            points = server.search("L_140_053*")
            assert isinstance(points, list)
            for point in points:
                assert isinstance(point, PI.PI.PIPoint)

    def test_search_multiple_strings(self):
        """Tests searching for PI points using a list of strings."""
        with PI.PIServer() as server:
            points = server.search(["L_140_053*", "M_127*"])
            assert isinstance(points, list)
            for point in points:
                assert isinstance(point, PI.PI.PIPoint)

    # def test_search_integer_raises_error(self):
    #     """Tests searching for PI points using an integer raises a TypeError."""
    #     with PI.PIServer() as server, self.assertRaises(TypeError):
    #         server.search(1)


class TestPIPoint:
    """Test valid interface of PIPoint."""

    def test_repr(self, pi_point):
        """Test representation of the PI Point."""
        assert repr(pi_point.point) == "%s(%s, %s; Current Value: %s %s)" % (
            "PIPoint",
            pi_point.tag,
            pi_point.attributes["descriptor"],
            pi_point.values[-1],
            pi_point.attributes["engunits"],
        )

    def test_name(self, pi_point):
        """Test retrieving the name of the PI Point."""
        assert pi_point.point.tag == pi_point.tag

    def test_current_value(self, pi_point):
        """Test retrieving the current value from a PI point."""
        assert pi_point.point.current_value == pi_point.values[-1]

    def test_last_update(self, pi_point):
        """Test retrieving the last update timestamp."""
        origin = datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.utc)
        assert (
            round(
                (pi_point.point.last_update - origin).total_seconds()
                - pi_point.timestamp_numbers[-1],
                ndigits=7,
            )
            == 0
        )

    def test_units_of_measurement(self, pi_point):
        """Test retrieving the units of measurement of the returned PI point."""
        assert pi_point.point.units_of_measurement == pi_point.attributes["engunits"]

    def test_description(self, pi_point):
        """Test retrieving the description of the PI point."""
        assert pi_point.point.description == pi_point.attributes["descriptor"]

    def test_raw_attributes(self, pi_point):
        """Test retrieving the attributes of the PI point as a dict."""
        assert pi_point.point.raw_attributes == pi_point.attributes

    def test_recorded_values_values(self, pi_point):
        """Test retrieving some recorded data from the server."""
        data = pi_point.point.recorded_values("01-07-2017", "02-07-2017")
        assert list(data.values) == pi_point.values

    def test_recorded_values_timestamps(self, pi_point):
        """Test retrieving some recorded data from the server."""
        data = pi_point.point.recorded_values("01-07-2017", "02-07-2017")
        assert list(data.index) == pi_point.timestamps

    def test_interpolated_values_values(self, pi_point):
        """Test retrieving some interpolated data from the server."""
        data = pi_point.point.interpolated_values("01-07-2017", "02-07-2017", "1h")
        assert list(data.values) == pi_point.values

    def test_interpolated_values_timestamps(self, pi_point):
        """Test retrieving some interpolated data from the server."""
        data = pi_point.point.interpolated_values("01-07-2017", "02-07-2017", "1h")
        assert list(data.index) == pi_point.timestamps
