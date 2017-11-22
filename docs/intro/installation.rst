Installation
============

**gthnk** installs on Windows and OSX systems in just a few steps:

1. create a Python virtual environment called `gthnk`
2. install `gthnk` from PyPI
3. set up your computer using `integration.py install`
4. open Gthnk in your web browser

Windows
^^^^^^^

First, install Python 3.6 from https://www.python.org/downloads/windows/.
Then, run the following commands in PowerShell to install :doc:`system-requirements`:

::

    start-process powershell –verb runAs
    pip install virtualenv
    pip install virtualenvwrapper
    pip install virtualenvwrapper-win

Once the requirements are installed, launch `cmd.exe` and run the following commands to install Gthnk:

::

    cmd.exe
    mkvirtualenv gthnk
    workon gthnk
    easy_install mr.bob==0.1.2
    pip install gthnk
    python %virtual_env%\Scripts\integration.py install
    gthnk

Now Gthnk is available from the command line with `gthnk` - but there are many ways to access Gthnk.

OS X
^^^^

Gthnk installs pretty easily on OSX with Homebrew.
Make sure you are using the *admin* user for this process, just like a normal Homebrew operation.

::

    brew install python --universal --framework
    brew install pyenv-virtualenv
    brew install pyenv-virtualenvwrapper
    brew install sqlite
    pip install --upgrade pip

Now drop administrative privileges and become your regular user again.
OS X installation is accomplished with the following commands, which are entered in the terminal:

::

    mkvirtualenv gthnk
    pip install gthnk
    integration.py install
    open http://localhost:1620

Troubleshooting
^^^^^^^^^^^^^^^

- If ``mkvirtualenv`` or ``pip`` does not work, then review :doc:`system-requirements` to be sure you have installed everything.
- If ``integration.py`` does not work, then closely read the terminal output to look for any errors.

User Account
------------

The installation script will prompt you to create a user account for **gthnk**.
You will need to use this account to gain access to your journal.
Choose a username and a password, then ensure you track that information for later.

File Locations
--------------

During the installation process, files are created in the following locations:

- ``~/.virtualenvs`` - virtualenvwrapper uses this to store all of the python files that are associated with the gthnk virtual environment.  This insulates **gthnk** from any changes to the system, which ensures that it will keep running for years.
- ``~/Library/Gthnk`` - **gthnk** itself will store its configuration, database, backups, logs, and exports here.  Be sure this folder is backed up somewhere.

Next Steps
----------

Now check out :doc:`/user/using-the-journal` to learn techniques for actually getting stuff done with **gthnk**.
