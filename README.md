# pyrollout
Python feature flagging

[![Build Status](https://travis-ci.org/brechin/pyrollout.svg?branch=master)](https://travis-ci.org/brechin/pyrollout)

Inspired by the [rollout](https://github.com/FetLife/rollout) Ruby gem by [James Golick](https://github.com/jamesgolick)
and a Python port of it called
[proclaim](https://github.com/asenchi/proclaim) by [Curt Micol](Curt Micol) which I found after reading
[Using Feature Flags to Ship Changes with Confidence](http://blog.travis-ci.com/2014-03-04-use-feature-flags-to-ship-changes-with-confidence/)
by [Mathias Meyer](https://github.com/roidrage).

Both of these use redis, and I don't like that requirement. I seek to support multiple storage/persistence mechanisms.

Usage
-----

To initialize pyrollout with the default in-memory feature & user storage:

```
import pyrollout
rollout = pyrollout.Rollout()
```

Now add features:

```
from pyrollout.feature import Feature
# Open to all by using the special group 'ALL'
rollout.add_feature(Feature('feature_for_all', groups=['ALL']))
# Open to select groups
rollout.add_feature(Feature('feature_for_groups', groups=['vip', 'early_adopter]))
# Open to specific user(s), by user ID
rollout.add_feature(Feature('feature_for_users', users=[123, 456, 789]))
# Open to 20% of users, calculated via user ID
rollout.add_feature(Feature('20pct', percentage=20))
```

Check access to features:

```
def untested_feature(user):
    # Because this feature was not defined, access will always be denied (by default)
    if not rollout.can(user, 'use_untested_feature'):
        return None
    else:
        do_cool_things()

class FooHandler(BaseHandler):
    def get(self):
        # self.user is a user object in a format pyrollout understands
        if not rollout.can(self.user, 'feature_for_users'):
            self.abort(403)
        else:
            do_foo()
```

Some feature ideas
------------------

* Flag by user
* Flag by group (including special groups _ALL_ and _NONE_)
* Flag on percentage
* Flag on user property
* Flag on lambda passed the user object
* Use memory
* Use file
* Use memcache, e.g. in Google App Engine
* Use some other persistent database
