class FeatureStorageManager(object):
    """
    Base class for feature storage managers,
     which are used to read and/or persist the rollout data.
    """

    def get_feature_config(self, feature_name):
        raise NotImplementedError

    def set_feature_config(self, feature_name, feature_data):
        raise NotImplementedError


class UserStorageManager(object):
    """
    Base class for user storage managers,
     which are used to read and/or persist the rollout data.

     Currently this is intended to be read-only.
    """

    def get_user_id(self, user):
        return self.get_user_property(user, 'id')

    def get_user_property(self, user, property_name, default_value=None):
        raise NotImplementedError

    def get_groups(self, user):
        return self.get_user_property(user, 'groups', [])

    def is_in_group(self, user, group):
        raise NotImplementedError
