import unittest

from pyrollout.feature import Feature


class TestFeatures(unittest.TestCase):
    def test_feature_creation(self):
        feature = Feature('feature1', groups=['g1'])
        self.assertEqual(feature.name, 'feature1')
        self.assertListEqual(feature.groups, ['g1'])
