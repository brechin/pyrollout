class Feature(object):
    def __init__(self, name, groups=None, percentage=None, randomize=False, users=None):
        """
        A representation of a feature for use in PyRollout.

        :param name: Name of feature, this is what you will pass in when checking access
        :type name: basestring
        :param groups: optional list of group names to allow access to "ALL" and "NONE" are special names
        :type groups: list
        :param percentage: 0-100 percentage of users who should have access
        :type percentage: int
        :param randomize: randomize percentage access, normally based simply on user ID
        :type randomize: bool
        :param users: list of user IDs that should have access
        :type users: list
        """
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
        """
        Build Feature representation.

        :returns: str repr: ``eval``-ready string representation of feature.
        """
        s = []
        if self.name:
            s.append("'%s'" % self.name)
        for p in ['groups', 'percentage', 'randomize', 'users']:
            v = getattr(self, p)
            s.append('%s=%s' % (p, repr(v)))
        s = ', '.join(s)
        return 'Feature(%s)' % s

    def __str__(self):
        """
        Nicer representation of feature with semi-readable configuration.

        :returns: str str: Human-readable string representation of feature.
        """
        repr_string = '<Feature {NAME} - %s>'.format(NAME=self.name)
        config_string = ''
        if len(self.users) > 0:
            config_string += 'Users:%s ' % self.users
        if len(self.groups) > 0:
            config_string += 'Groups:%s ' % self.groups
        if self.percentage != 0:
            config_string += 'Percent:{PCT}:{RAND}'.format(
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
        """
        Check if user can access feature by group.

        :param user_storage:
        :type user_storage: pyrollout.storage.UserStorageManager
        :param user:
        :type user: dict or object
        :return: Can user access feature
        :rtype: bool
        """
        if 'ALL' in self.groups:
            return True
        elif 'NONE' in self.groups:
            return False
        else:
            return user_storage.is_in_group(user, self.groups)

    def can_user_id(self, user_storage, user):
        """
        Check if user can access feature by user ID.

        :param user_storage:
        :type user_storage: pyrollout.storage.UserStorageManager
        :param user:
        :type user: dict or object
        :return: Can user access feature
        :rtype: bool
        """
        return user_storage.get_user_id(user) in self.users

    def can_user_pct(self, user_storage, user):
        """
        Check if user can access feature by percentage.

        :param user_storage:
        :type user_storage: pyrollout.storage.UserStorageManager
        :param user:
        :type user: dict or object
        :return: Can user access feature
        :rtype: bool
        """
        user_id = user_storage.get_user_id(user)
        if self.randomize:
            user_id += hash(self.name)

        return user_id % 100 < self.percentage
