from unittest.case import TestCase
from pyrollout.storage.memory import MemoryUserStorage


class TestMemoryStorage(TestCase):
    def setUp(self):
        self.user_storage = MemoryUserStorage()

    # noinspection PyDefaultArgument
    def _add_user(self, user_id=[1], groups=None):
        user_id[0] += 1
        new_user = {
            'id': user_id[0],
            'name': 'TestUser {ID}'.format(ID=user_id[0])
        }
        if groups is not None:
            new_user['groups'] = groups
        return self.user_storage.add_user(new_user)

    def test_add_user(self):
        users = [self._add_user() for _ in xrange(5)]
        print self.user_storage.user_data
        for u in users:
            self.assertDictEqual(u, self.user_storage.user_data[u['id']])

    def test_user_in_group(self):
        user = self._add_user(groups=['foo'])
        self.assertTrue(self.user_storage.is_in_group(user, 'foo'))
