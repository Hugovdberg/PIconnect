''' test_PI tests connection to the PI System
'''
import datetime
import unittest
import PIthon as PI
from PIthon.test.fakes import FakePIPoint


class TestServer(unittest.TestCase):
    ''' TestServer tests connecting to the server
    '''

    def test_connection(self):
        try:
            PI.PIServer()
        except:
            self.fail("PI.PIServer() raised Exception unexpectedly.")


class TestSearchPIPoints(unittest.TestCase):
    """Test searching for PI Points on the default server."""

    def test_search_single_string(self):
        ''' tests searching for PI point using a single string
        '''
        with PI.PIServer() as server:
            points = server.search('L_140_053*')
            self.assertIsInstance(points, list)
            for point in points:
                self.assertIsInstance(point, PI.PI.PIPoint)

    def test_search_multiple_strings(self):
        ''' tests searching for PI point using a list of strings
        '''
        with PI.PIServer() as server:
            points = server.search(['L_140_053*', 'M_127*'])
            self.assertIsInstance(points, list)
            for point in points:
                self.assertIsInstance(point, PI.PI.PIPoint)


class TestPIPoint(unittest.TestCase):
    """Test valid interface of PIPoint."""

    def setUp(self):
        import datetime
        self.point = FakePIPoint(values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                 timestamps=[datetime.datetime.fromtimestamp(x)
                                             for x in [1502654535.813251,
                                                       1502671554.038452,
                                                       1502695584.315902,
                                                       1502704569.874902,
                                                       1502709576.898902,
                                                       1502713512.168902,
                                                       1502718534.453902,
                                                       1502722585.816163,
                                                       1502731598.316851,
                                                       1502732545.013568
                                                       ]])

    def test_current_value(self):
        ''' tests retrieving the current value from a PI point
        '''
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('current_value' in dir(point))
            self.assertIsInstance(point.current_value, float)

    def test_last_update(self):
        ''' tests retrieving the last update timestamp
        '''
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('last_update' in dir(point))
            self.assertIsInstance(point.last_update, datetime.datetime)

    def test_units_of_measurement(self):
        ''' tests retrieving the units of measurement of the returned PI point
        '''
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('units_of_measurement' in dir(point))
            self.assertIsInstance(point.units_of_measurement, basestring)

    def test_description(self):
        ''' tests retrieving the description
        '''
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('description' in dir(point))
            self.assertIsInstance(point.description, basestring)

    def test_raw_attributes(self):
        ''' tests retrieving the attributes of the PI point as a dict
        '''
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('raw_attributes' in dir(point))
            self.assertIsInstance(point.raw_attributes, dict)

    def test_compressed_data(self):
        ''' tests retrieving some compressed data from the server
        '''
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('compressed_data' in dir(point))
            data = point.compressed_data('01-07-2017', '02-07-2017')
            self.assertEqual(data.size, 70)

    def test_sampled_data(self):
        ''' tests retrieving some sampled data from the server
        '''
        with PI.PIServer() as server:
            point = server.search('L_140_053_FQIS053_01_Meetwaarde')[0]
            self.assertIsInstance(point, PI.PI.PIPoint)
            self.assertTrue('sampled_data' in dir(point))
            data = point.sampled_data('01-07-2017', '02-07-2017', '1h')
            self.assertEqual(data.size, 25)
