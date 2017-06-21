
from google.appengine.ext import ndb
from pyrollout.feature import Feature
from pyrollout.storage import FeatureStorageManager, UserStorageManager


class PyRolloutFeature(ndb.Model):
    name = ndb.StringProperty(required=True)
    groups = ndb.StringProperty(repeated=True)
    users = ndb.GenericProperty(repeated=True)
    percentage = ndb.IntegerProperty()
    randomize = ndb.BooleanProperty(default=False)

    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.name == name).get()


class GAEFeatureStorage(FeatureStorageManager):

    def get_feature_config(self, feature_name):
        feature = PyRolloutFeature.get_by_name(feature_name)
        if feature:
            feature = Feature(
                feature.name,
                groups=feature.groups,
                users=feature.users,
                percentage=feature.percentage,
                randomize=feature.randomize)

        return feature

    def set_feature_config(self, feature_name, feature_data):
        feature = PyRolloutFeature.get_by_name(feature_name)
        if feature:
            feature.groups = feature_data.groups
            feature.users = feature_data.users
            feature.percentage = feature_data.percentage
            feature.randomize = feature_data.randomize
        else:
            feature = PyRolloutFeature(name=feature_data.name,
                                       groups=feature_data.groups,
                                       users=feature_data.users,
                                       percentage=feature_data.percentage,
                                       randomize=feature_data.randomize)
        feature.put()


class GAEUserStorage(UserStorageManager):
    """Left unimplemented because every software's implementation of users is different."""

    def get_user_property(self, user, property_name, default_value=None):
        raise NotImplementedError()

    def add_user(self, user):
        raise NotImplementedError()
