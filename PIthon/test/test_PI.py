import unittest
import PIthon as PI

class TestServer(unittest.TestCase):

    def test_search_single_string(self):
        with PI.PIServer() as server:
            points = server.search('L_140*')
            self.assertEqual(type(points), list)
            for point in points:
                self.assertEqual(type(point), PI.PI.PIPoint)

    def test_search_multiple_strings(self):
        with PI.PIServer() as server:
            points = server.search(['L_140*', 'M_127*'])
            self.assertEqual(type(points), list)
            for point in points:
                self.assertEqual(type(point), PI.PI.PIPoint)
