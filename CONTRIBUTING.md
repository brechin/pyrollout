# How To Contribute

We welcome contributions of all types. Please review the [Code of Conduct](CODE_OF_CONDUCT.md)
and submit your bug reports, feature requests, and pull requests at will.

## Making changes

* Fork the repository
* Create a topic branch from where you want to base your work.
  * This is usually the master branch.
  * To quickly create a topic branch based on master; `git checkout -b
    fix/master/my_contribution master`. Please avoid working directly on the
    `master` branch.
* Make commits of logical units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format.

````
    (Issue #123) Summary of changes made

    Brief paragraph describing why and how the changes were made.

    Any additional references, links, caveats, warnings, etc.
````

* Make sure you have added the necessary tests for your changes.
* Run _all_ the tests to assure nothing else was accidentally broken.
* Push your code to your forked copy and make a pull request.
