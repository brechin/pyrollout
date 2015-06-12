import timeit
import unittest


class TestBasicFunctions(unittest.TestCase):
    def test_add_feature_performance(self):
        print timeit.timeit(
            "rollout.add_feature(Feature('feature_for_all', groups=['ALL']))",
            setup='from pyrollout import Rollout; from pyrollout.feature import Feature; rollout = Rollout()',
            number=100000)

    def test_can_none_performance(self):
        print timeit.timeit(
            "rollout.can({'id':1}, 'feature_for_none')",
            setup='from pyrollout import Rollout; from pyrollout.feature import Feature; rollout = Rollout();'
                  "rollout.add_feature(Feature('feature_for_none', groups=['NONE']))",
            number=100000)

    def test_can_all_performance(self):
        print timeit.timeit(
            "rollout.can({'id':1}, 'feature_for_all')",
            setup='from pyrollout import Rollout; from pyrollout.feature import Feature; rollout = Rollout();'
                  "rollout.add_feature(Feature('feature_for_all', groups=['ALL']))",
            number=100000)

    def test_can_group_performance(self):
        print timeit.timeit(
            "rollout.can({'id':1, 'groups': ['foo', 'bar']}, 'feature_for_group')",
            setup='from pyrollout import Rollout; from pyrollout.feature import Feature; rollout = Rollout();'
                  "rollout.add_feature(Feature('feature_for_group', groups=['foo']))",
            number=100000)

    def test_can_user_performance(self):
        print timeit.timeit(
            "rollout.can({'id':1}, 'feature_for_me')",
            setup='from pyrollout import Rollout; from pyrollout.feature import Feature; rollout = Rollout();'
                  "rollout.add_feature(Feature('feature_for_me', users=[{'id': 1}]))",
            number=100000)

    def test_can_pct_performance(self):
        print timeit.timeit(
            "rollout.can({'id':1}, 'feature_for_pct')",
            setup='from pyrollout import Rollout; from pyrollout.feature import Feature; rollout = Rollout();'
                  "rollout.add_feature(Feature('feature_for_pct', percentage=100))",
            number=100000)
