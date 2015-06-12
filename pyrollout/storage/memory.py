from . import FeatureStorageManager, UserStorageManager


class MemoryFeatureStorage(FeatureStorageManager):
    def __init__(self):
        self.feature_data = {}

    def get_feature_config(self, feature_name):
        return self.feature_data.get(feature_name, None)

    def set_feature_config(self, feature_name, feature_data):
        self.feature_data[feature_name] = feature_data


class MemoryUserStorage(UserStorageManager):
    """
    This will store users in a dict that looks like this:
    {
        '123': {
            'username': 'John Doe',
            'id': 123,
            'groups': ['a', 'b'],
            ...
        },
        '456': {
            'id': 456,
            ...
        }
    }
    """

    def __init__(self):
        self.user_data = {}

    def get_user_property(self, user, property_name, default_value=None):
        return user.get(property_name, default_value)

    def add_user(self, user):
        self.user_data[self.get_user_id(user)] = user
        return user

    def is_in_group(self, user, group_or_groups):
        if not isinstance(group_or_groups, (list, set)):
            group_or_groups = [group_or_groups]
        user_groups = self.get_groups(user)
        return set(group_or_groups) & set(user_groups)
