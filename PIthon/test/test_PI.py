"""Test communication with the PI System."""
import datetime
import unittest
import PIthon as PI


class TestServer(unittest.TestCase):
    """Test connecting to the server"""

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

    def test_current_value(self):
        """Test retrieving the current value from a PI point."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('current_value' in dir(point))
            self.assertIsInstance(point.current_value, float)

    def test_last_update(self):
        """Test retrieving the last update timestamp."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('last_update' in dir(point))
            self.assertIsInstance(point.last_update, datetime.datetime)

    def test_units_of_measurement(self):
        """Test retrieving the units of measurement of the returned PI point."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('units_of_measurement' in dir(point))
            self.assertIsInstance(point.units_of_measurement, basestring)

    def test_description(self):
        """Test retrieving the description of the PI point."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('description' in dir(point))
            self.assertIsInstance(point.description, basestring)

    def test_raw_attributes(self):
        """Test retrieving the attributes of the PI point as a dict."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('raw_attributes' in dir(point))
            self.assertIsInstance(point.raw_attributes, dict)

    def test_compressed_data(self):
        """Test retrieving some compressed data from the server."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('compressed_data' in dir(point))
            data = point.compressed_data('01-07-2017', '02-07-2017')
            self.assertEqual(data.size, 70)

    def test_sampled_data(self):
        """Test retrieving some sampled data from the server."""
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('sampled_data' in dir(point))
            data = point.sampled_data('01-07-2017', '02-07-2017', '1h')
            self.assertEqual(data.size, 25)
