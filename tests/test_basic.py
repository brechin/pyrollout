import unittest

from pyrollout import Rollout
from pyrollout.feature import Feature
from pyrollout.storage.memory import MemoryUserStorage, MemoryFeatureStorage


class TestBasicFunctions(unittest.TestCase):
    def setUp(self):
        self.rollout = Rollout()
        self.rollout.add_feature(Feature('feature_for_all', groups=['ALL']))
        self.rollout.add_feature(Feature('feature_for_none', groups=['NONE']))
        self.rollout.add_feature(Feature('feature_for_some', groups=['some']))

    # noinspection PyDefaultArgument
    def _add_user(self, user_id=[1], groups=None, string_id=False):
        user_id[0] += 1
        if string_id:
          uid = str(user_id[0])
        else:
          uid = user_id[0]
        self.assertTrue(isinstance(self.rollout.user_storage, MemoryUserStorage))
        new_user = {
            'id': uid,
            'name': 'TestUser {ID}'.format(ID=user_id[0])
        }
        if groups is not None:
            new_user['groups'] = groups
        return self.rollout.user_storage.add_user(new_user)

    def test_undefined_feature(self):
        user = self._add_user()
        self.assertFalse(self.rollout.can(user, 'undefined_feature'))

    def test_undefined_feature_default_true(self):
        user = self._add_user()
        self.rollout.default_undefined_feature = True
        self.assertTrue(self.rollout.can(user, 'undefined_feature_true'))

    def test_specify_storage(self):
        rollout = Rollout(feature_storage=MemoryFeatureStorage(), user_storage=MemoryUserStorage())
        rollout.add_feature(Feature('feature_for_all', groups=['ALL']))
        user = self._add_user()
        self.assertTrue(self.rollout.can(user, 'feature_for_all') is True)

    def test_repr(self):
        feature = Feature('ff1', groups=['a'], users=[1], percentage=1)
        feature_repr = repr(feature)
        feature_compare = eval(feature_repr)
        self.assertEqual(feature.name, feature_compare.name)
        self.assertEqual(feature.groups, feature_compare.groups)
        self.assertEqual(feature.percentage, feature_compare.percentage)
        self.assertEqual(feature.randomize, feature_compare.randomize)
        self.assertEqual(feature.users, feature_compare.users)

    def test_str(self):
        feature_str = str(Feature('ff1', groups=['a'], users=[1], percentage=1))
        print feature_str
        self.assertTrue("Groups:['a']" in feature_str)
        self.assertTrue("Users:[1]" in feature_str)
        self.assertTrue("Percent:1:False" in feature_str)

    def test_all(self):
        user = self._add_user()
        self.assertTrue(self.rollout.can(user, 'feature_for_all') is True)

    def test_none(self):
        user = self._add_user()
        self.assertTrue(self.rollout.can(user, 'feature_for_none') is False)

    def test_some(self):
        user = self._add_user()
        self.assertTrue(self.rollout.can(user, 'feature_for_some') is False)
        user = self._add_user(groups=['some'])
        self.assertTrue(self.rollout.can(user, 'feature_for_some') is True)

    def test_percentage_string_user_id(self):
        users = [self._add_user(string_id=True) for _ in range(100)]
        self.assertIsInstance(users[0].get('id'), basestring)
        self.rollout.add_feature(Feature('20pct', percentage=20))
        self.assertEquals(20, [self.rollout.can(u, '20pct') for u in users].count(True))

    def test_percentage_20(self):
        users = [self._add_user() for _ in range(100)]
        self.rollout.add_feature(Feature('20pct', percentage=20))
        self.assertEquals(20, [self.rollout.can(u, '20pct') for u in users].count(True))

    def test_percentage_0(self):
        users = [self._add_user() for _ in range(100)]
        self.rollout.add_feature(Feature('pct', percentage=0))
        self.assertEquals(0, [self.rollout.can(u, 'pct') for u in users].count(True))

    def test_percentage_100(self):
        users = [self._add_user() for _ in range(100)]
        self.rollout.add_feature(Feature('pct', percentage=100))
        self.assertEquals(100, [self.rollout.can(u, 'pct') for u in users].count(True))

    def test_pct_10_rand(self):
        users = [self._add_user() for _ in range(100)]
        self.rollout.add_feature(Feature('pctx', percentage=10, randomize=True))
        self.assertEquals(10, [self.rollout.can(u, 'pctx') for u in users].count(True))

    def test_pct_string_user_id_rand(self):
        users = [self._add_user(string_id=True) for _ in range(100)]
        self.rollout.add_feature(Feature('pctx', percentage=10, randomize=True))
        self.assertEquals(10, [self.rollout.can(u, 'pctx') for u in users].count(True))


    def test_user_feature(self):
        u = self._add_user()
        self.rollout.add_feature(Feature('myfeature', users=[u['id']]))
        self.rollout.add_feature(Feature('notmyfeature', users=[-1]))
        self.assertTrue(self.rollout.can(u, 'myfeature'))
        self.assertFalse(self.rollout.can(u, 'notmyfeature'))
