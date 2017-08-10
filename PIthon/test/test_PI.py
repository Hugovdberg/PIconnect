import datetime
import unittest
import PIthon as PI

class TestServer(unittest.TestCase):

    def test_search_single_string(self):
        with PI.PIServer() as server:
            points = server.search('L_140_053*')
            self.assertIsInstance(points, list)
            for point in points:
                self.assertIsInstance(point, PI.PI.PIPoint)

    def test_search_multiple_strings(self):
        with PI.PIServer() as server:
            points = server.search(['L_140_053', 'M_127*'])
            self.assertIsInstance(points, list)
            for point in points:
                self.assertIsInstance(point, PI.PI.PIPoint)

    def test_current_value(self):
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('current_value' in dir(point))
            self.assertIsInstance(point.current_value, float)

    def test_last_update(self):
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('last_update' in dir(point))
            self.assertIsInstance(point.last_update, datetime.datetime)

    def test_units_of_measurement(self):
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('units_of_measurement' in dir(point))
            self.assertIsInstance(point.units_of_measurement, basestring)

    def test_description(self):
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('description' in dir(point))
            self.assertIsInstance(point.description, basestring)

    def test_raw_attributes(self):
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('raw_attributes' in dir(point))
            self.assertIsInstance(point.raw_attributes, dict)

    def test_compressed_data(self):
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('compressed_data' in dir(point))

    def test_sampled_data(self):
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('sampled_data' in dir(point))
