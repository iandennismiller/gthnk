Installation
============

Make sure you have the :doc:`system-requirements` installed.  You will need Python, pip, virtualenv, and virtualenvwrapper.

Installation
------------

There are three steps to installing **gthnk**:

1. create a Python virtual environment called `gthnk`
2. install `gthnk` from PyPI
3. set up your computer using ``install_osx.sh``

These three steps are accomplished with the following commands, which are entered in the terminal:

::

    mkvirtualenv gthnk
    pip install gthnk
    install_osx.sh

Troubleshooting
^^^^^^^^^^^^^^^

- If ``mkvirtualenv`` does not work, then you have a problem with virtualenv or virtualenvwrapper.
- If ``pip`` does not work, then review :doc:`system-requirements` to be sure you have installed everything.
- If ``install_osx.sh`` does not work, then closely read the terminal output to look for any errors.

User Account
------------

The installation script will prompt you to create a user account for **gthnk**.  You will need to use this account to gain access to your journal.  Choose a username and a password, then ensure you track that information for later.

File Locations
--------------

During the installation process, files are created in the following locations:

- ``~/.virtualenvs`` - virtualenvwrapper uses this to store all of the python files that are associated with the gthnk virtual environment.  This insulates **gthnk** from any changes to the system, which ensures that it will keep running for years.
- ``~/Library/Gthnk`` - **gthnk** itself will store its configuration, database, backups, logs, and exports here.  Be sure this folder is backed up somewhere, because it is the key to 

Uninstallation
--------------

::

    workon gthnk
    uninstall_osx.sh
