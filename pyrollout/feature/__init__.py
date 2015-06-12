class Feature(object):
    """
    A representation of a feature for use in PyRollout.
    """
    def __init__(self, name, groups=None, percentage=None, randomize=False, users=None):
        self.name = name
        if groups is None:
            groups = []
        if 'ALL' in groups:
            assert ('NONE' not in groups)
        self.groups = groups

        if users is None:
            users = []
        self.users = users

        if percentage is None:
            percentage = 0
        self.percentage = percentage

        self.randomize = randomize

    def __repr__(self):
        repr_string = '<Feature {NAME} - %s>'.format(NAME=self.name)
        config_string = ''
        if len(self.users) > 0:
            config_string += 'U:%s ' % self.users
        if len(self.groups) > 0:
            config_string += 'G:%s ' % self.groups
        if self.percentage != 0:
            config_string += 'P:{PCT}:{RAND}'.format(
                PCT=self.percentage,
                RAND=self.randomize
            )
        return repr_string % config_string.strip()

    def can(self, user_storage, user):
        """
        Check if user, stored in user_storage, can access this feature.

        :param user_storage:
        :type user_storage: pyrollout.storage.UserStorageManager
        :param user:
        :type user: dict or object
        :return: Can user access feature
        :rtype: bool
        """
        if self.can_group(user_storage, user):
            return True
        elif self.can_user_id(user_storage, user):
            return True
        elif self.can_user_pct(user_storage, user):
            return True
        else:
            return False

    def can_group(self, user_storage, user):
        if 'ALL' in self.groups:
            return True
        elif 'NONE' in self.groups:
            return False
        else:
            return user_storage.is_in_group(user, self.groups)

    def can_user_id(self, user_storage, user):
        return user_storage.get_user_id(user) in self.users

    def can_user_pct(self, user_storage, user):
        user_id = user_storage.get_user_id(user)
        if self.randomize:
            user_id += hash(self.name)

        return user_id % 100 < self.percentage
