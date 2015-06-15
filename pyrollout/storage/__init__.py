class FeatureStorageManager(object):
    """
    Base class for feature storage managers, which are used to read and/or persist the rollout data.
    """

    def get_feature_config(self, feature_name):
        """
        Get feature configuration for `feature_name`.

        :param feature_name: Name of feature
        :type feature_name: basestring
        :return: Feature
        :rtype: pyrollout.feature.Feature
        """
        raise NotImplementedError

    def set_feature_config(self, feature_name, feature_data):
        """
        Save a feature configuration for `feature_name`.

        :param feature_name: Name of feature
        :type feature_name: basestring
        :param feature_data: Feature configuration
        :type feature_data: pyrollout.feature.Feature
        """
        raise NotImplementedError


class UserStorageManager(object):
    """
    Base class for user storage managers, which are used to read and/or persist the rollout data.

    This is generally intended to be read-only.
    """

    def get_user_id(self, user):
        """
        Get user ID. This may need to be implemented differently for different types of user objects.

        :param user: User object
        :type user: dict or object
        :return: User ID
        :rtype: int or basestring
        """
        return self.get_user_property(user, 'id')

    def get_user_property(self, user, property_name, default_value=None):
        """
        Get a property from a user object. This may need to be implemented differently
        for different types of user objects.

        :param user: User object
        :type user: dict or object
        :param property_name: Name of property
        :type property_name: basestring
        :param default_value: Default return value if property is not defined (default: None)
        :return: Property value or `default_value`
        """
        raise NotImplementedError

    def get_groups(self, user):
        """
        Get user's groups. This may need to be implemented differently for different types of user objects.

        :param user: User object
        :type user: dict or object
        :return: List of user's groups
        :rtype: list of strs
        """
        return self.get_user_property(user, 'groups', [])

    def is_in_group(self, user, group_or_groups):
        """
        Check if user is in a group. This may need to be implemented differently for different types of user objects.

        :param user: User object
        :type user: dict or object
        :param group_or_groups: Group name or list of group names
        :type group_or_groups: str or list of strs or set of strs
        :rtype: bool
        """
        if not isinstance(group_or_groups, (list, set)):
            group_or_groups = [group_or_groups]
        user_groups = self.get_groups(user)
        return set(group_or_groups) & set(user_groups)
