Release Procedure
=================

The project advances as a progression of project releases in which each release is a new iteration of the project.
Project planning consists of managing which items in ``docs/Todo.md`` will be included in each Milestone.
In general, each Milestone corresponds to a 0.0.1 increment in the release number.

The project source code repository contains two main branches: *master* and *develop*.
All of the active work happens in the develop branch.
When a milestone is reached, all of the work from the develop branch is merged into the master branch in order to prepare for a release.

In order to actually perform the release, there are several steps that must be performed each time.
This document discusses the "Release Procedure" that causes a new iteration of the project to be publicly released.

Overview
--------

- start in the develop branch.
- update version in  ``__meta__.py``.
- update ``docs/changelog.rst`` with the todo items that were completed for this release.
- `git commit` these final changes to the develop branch and `git push` them to the remote repo.
- `git checkout master` and `git merge develop` to bring in all changes from the develop branch.
- `git push` the master branch to kick off Travis CI and Coveralls.
- `make release`.
- verify the release on `pypi` at https://pypi.python.org/pypi/gthnk

Finalize develop branch
-----------------------

Start in the develop branch.

::

    git checkout develop

Update version in  ``__meta__.py``.

Update ``docs/changelog.rst`` with the todo items that were completed for this release.

Commit final changes to the develop branch and push them to the remote repo.

::

    git commit -am "prepare develop for release"
    git push

Release Master
--------------

Checkout the master branch and merge from develop to bring in all changes from the develop branch.

::

    git checkout master
    git merge develop

Push to the master branch to kick off Travis CI and Coveralls.

::

    git push

Use the Makefile `release` target, which delegates to the `setuptools` upload support for pypi.

::

    make release

Verify the release on `pypi` at https://pypi.python.org/pypi/gthnk

Release Candidates
------------------

In anticipation of a release, there are many reasons why it might be useful to provide a preview release called a "release candidate".
The procedure for a release candidate is the same as for a release.
The only notable change for a release candidate is the version scheme.
The version uses the number of the upcoming release with `rcX` appended, where `rc1` is the first release candidate, `rc2` is the second, and so on.
So in anticipation of `0.9.0`, the first release candidate might be called `0.9.0rc1`.
