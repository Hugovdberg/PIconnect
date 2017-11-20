""" PIthon.test.test_PI
    Test communication with the PI System.
"""
# Copyright 2017 Hugo van den Berg, Stijn de Jong

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import datetime
import unittest

import pytz

import PIthon as PI
from PIthon.test.fakes import FakePIPoint


class TestServer(unittest.TestCase):
    """Test connecting to the server"""

    def test_connection(self):
        """Test that creating a PI.PIServer object without arguments raises no exception"""
        try:
            PI.PIServer()
        except Exception as e:
            self.fail("PI.PIServer() raised %s unexpectedly." % e.__class__.__name__)


class TestSearchPIPoints(unittest.TestCase):
    """Test searching for PI Points on the default server."""

    def test_search_single_string(self):
        """Test searching for PI points using a single string."""
        with PI.PIServer() as server:
            points = server.search('L_140_053*')
            self.assertIsInstance(points, list)
            for point in points:
                self.assertIsInstance(point, PI.PI.PIPoint)

    def test_search_multiple_strings(self):
        """Tests searching for PI points using a list of strings."""
        with PI.PIServer() as server:
            points = server.search(['L_140_053*', 'M_127*'])
            self.assertIsInstance(points, list)
            for point in points:
                self.assertIsInstance(point, PI.PI.PIPoint)


class TestPIPoint(unittest.TestCase):
    """Test valid interface of PIPoint."""

    def setUp(self):
        self.tag = 'TEST_140_053_FQIS053_01_Meetwaarde'
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.timestamp_numbers = [
            1502654535.813,
            1502671554.038,
            1502695584.315,
            1502704569.874,
            1502709576.898,
            1502713512.168,
            1502718534.453,
            1502722585.816,
            1502731598.316,
            1502732545.013
        ]
        self.timestamps = [datetime.datetime.fromtimestamp(x, tz=pytz.utc)
                           for x in self.timestamp_numbers]
        self.attributes = {
            'engunits': 'm3/h',
            'descriptor': 'Flow'
        }
        self.point = PI.PI.PIPoint(FakePIPoint(tag=self.tag,
                                               values=self.values,
                                               timestamps=self.timestamps,
                                               attributes=self.attributes))

    def test_name(self):
        """Test retrieving the name of the PI Point."""
        self.assertEqual(self.point.tag, self.tag)

    def test_current_value(self):
        """Test retrieving the current value from a PI point."""
        self.assertEqual(self.point.current_value, self.values[-1])

    def test_last_update(self):
        """Test retrieving the last update timestamp."""
        origin = datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.utc)
        self.assertAlmostEqual((self.point.last_update - origin).total_seconds(),
                               self.timestamp_numbers[-1])

    def test_units_of_measurement(self):
        """Test retrieving the units of measurement of the returned PI point."""
        self.assertEqual(self.point.units_of_measurement, self.attributes['engunits'])

    def test_description(self):
        """Test retrieving the description of the PI point."""
        self.assertEqual(self.point.description, self.attributes['descriptor'])

    def test_raw_attributes(self):
        """Test retrieving the attributes of the PI point as a dict."""
        self.assertEqual(self.point.raw_attributes, self.attributes)

    def test_compressed_data_values(self):
        """Test retrieving some compressed data from the server."""
        data = self.point.compressed_data('01-07-2017', '02-07-2017')
        self.assertEqual(list(data.values), self.values)

    def test_compressed_data_timestamps(self):
        """Test retrieving some compressed data from the server."""
        data = self.point.compressed_data('01-07-2017', '02-07-2017')
        self.assertEqual(list(data.index), self.timestamps)

    def test_sampled_data_values(self):
        """Test retrieving some compressed data from the server."""
        data = self.point.sampled_data('01-07-2017', '02-07-2017', '1h')
        self.assertEqual(list(data.values), self.values)

    def test_sampled_data_timestamps(self):
        """Test retrieving some sampled data from the server."""
        data = self.point.sampled_data('01-07-2017', '02-07-2017', '1h')
        self.assertEqual(list(data.index), self.timestamps)
