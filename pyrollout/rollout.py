import logging
# noinspection PyUnresolvedReferences
import feature  #noqa

logging.basicConfig(level=logging.DEBUG)


class Rollout(object):
    __version__ = '0.3.5'

    def __init__(self, feature_storage=None, user_storage=None, undefined_feature_access=False):
        """
        Manage feature flags for groups, users, or on a percentage basis. Use your own
        user models and persistence with replaceable modules.

        :param feature_storage: Object to manage storage of feature definitions
        :type feature_storage: pyrollout.storage.FeatureStorageManager
        :param user_storage: Object to manage storage of users
        :type user_storage: pyrollout.storage.UserStorageManager
        :param undefined_feature_access: Should undefined features be allowed (default:True) or denied (False) access?
        :type undefined_feature_access: bool
        """
        if feature_storage is None:
            from storage.memory import MemoryFeatureStorage

            self.feature_storage = MemoryFeatureStorage()
        else:
            self.feature_storage = feature_storage

        if user_storage is None:
            from storage.memory import MemoryUserStorage

            self.user_storage = MemoryUserStorage()
        else:
            self.user_storage = user_storage

        self.default_undefined_feature = undefined_feature_access

    def add_feature(self, feature):
        """
        Add a feature to be handled by this instance

        :param feature: New feature to add
        :type feature: pyrollout.feature.Feature
        """
        self.feature_storage.set_feature_config(feature.name, feature_data=feature)

    def can(self, user, feature_name):
        """
        Check whether user has access to the given feature.

        :param user: User object to check, must be compatible with user storage manager in use
        :type user: dict or object
        :param feature_name: Name of feature to check against
        :type feature_name: basestring
        :return: True if user has access, False otherwise
        :rtype: bool
        """
        feature = self.feature_storage.get_feature_config(feature_name)
        if feature is None:
            return self.default_undefined_feature
        return feature.can(self.user_storage, user)
