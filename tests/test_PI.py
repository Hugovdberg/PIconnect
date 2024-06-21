"""Test communication with the PI System."""

import datetime

import pytest
import pytz

import PIconnect as PI
import PIconnect.PI as PI_

from .fakes import VirtualTestCase, pi_point

__all__ = ["TestServer", "TestSearchPIPoints", "TestPIPoint", "pi_point"]


class TestServer:
    """Test connecting to the server."""

    def test_connection(self):
        """Test that creating a PI.PIServer object without arguments raises no exception."""
        PI.PIServer()

    def test_server_name(self):
        """Test that the server reports the same name as which was connected to."""
        default_server = PI.PIServer.default_server
        if default_server is None:
            pytest.skip("No default server found.")
        servername = default_server.Name
        server = PI.PIServer(servername)
        assert server.server_name == servername

    def test_warn_unkown_server(self):
        """Test that the server reports a warning when an unknown host is specified."""
        server_names = list(PI.PIServer.servers)
        server_name = "__".join(server_names + ["UnknownHostName"])
        with pytest.warns(UserWarning):
            PI.PIServer(server_name)

    def test_repr(self):
        """Test that the server representation matches the connected server."""
        default_server = PI.PIServer.default_server
        if default_server is None:
            pytest.skip("No default server found.")
        servername = default_server.Name
        server = PI.PIServer(servername)
        assert repr(server) == "PIServer(\\\\{})".format(servername)


class TestSearchPIPoints:
    """Test searching for PI Points on the default server."""

    def test_search_single_string(self):
        """Test searching for PI points using a single string."""
        with PI.PIServer() as server:
            points = server.search("L_140_053*")
            assert isinstance(points, list)
            for point in points:
                assert isinstance(point, PI_.PIPoint)

    def test_search_multiple_strings(self):
        """Tests searching for PI points using a list of strings."""
        with PI.PIServer() as server:
            points = server.search(["L_140_053*", "M_127*"])
            assert isinstance(points, list)
            for point in points:
                assert isinstance(point, PI_.PIPoint)

    # def test_search_integer_raises_error(self):
    #     """Tests searching for PI points using an integer raises a TypeError."""
    #     with PI.PIServer() as server, self.assertRaises(TypeError):
    #         server.search(1)


class TestPIPoint:
    """Test valid interface of PIPoint."""

    def test_repr(self, pi_point: VirtualTestCase):
        """Test representation of the PI Point."""
        assert repr(pi_point.point) == "%s(%s, %s; Current Value: %s %s)" % (
            "PIPoint",
            pi_point.tag,
            pi_point.attributes["descriptor"],
            pi_point.values[-1],
            pi_point.attributes["engunits"],
        )

    def test_name(self, pi_point: VirtualTestCase):
        """Test retrieving the name of the PI Point."""
        assert pi_point.point.tag == pi_point.tag

    def test_current_value(self, pi_point: VirtualTestCase):
        """Test retrieving the current value from a PI point."""
        assert pi_point.point.current_value == pi_point.values[-1]

    def test_last_update(self, pi_point: VirtualTestCase):
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

    def test_units_of_measurement(self, pi_point: VirtualTestCase):
        """Test retrieving the units of measurement of the returned PI point."""
        assert pi_point.point.units_of_measurement == pi_point.attributes["engunits"]

    def test_description(self, pi_point: VirtualTestCase):
        """Test retrieving the description of the PI point."""
        assert pi_point.point.description == pi_point.attributes["descriptor"]

    def test_raw_attributes(self, pi_point: VirtualTestCase):
        """Test retrieving the attributes of the PI point as a dict."""
        assert pi_point.point.raw_attributes == pi_point.attributes

    def test_recorded_values_values(self, pi_point: VirtualTestCase):
        """Test retrieving some recorded data from the server."""
        data = pi_point.point.recorded_values("01-07-2017", "02-07-2017")
        assert list(data.values) == pi_point.values

    def test_recorded_values_timestamps(self, pi_point: VirtualTestCase):
        """Test retrieving some recorded data from the server."""
        data = pi_point.point.recorded_values("01-07-2017", "02-07-2017")
        assert list(data.index) == pi_point.timestamps

    def test_interpolated_values_values(self, pi_point: VirtualTestCase):
        """Test retrieving some interpolated data from the server."""
        data = pi_point.point.interpolated_values("01-07-2017", "02-07-2017", "1h")
        assert list(data.values) == pi_point.values

    def test_interpolated_values_timestamps(self, pi_point: VirtualTestCase):
        """Test retrieving some interpolated data from the server."""
        data = pi_point.point.interpolated_values("01-07-2017", "02-07-2017", "1h")
        assert list(data.index) == pi_point.timestamps
