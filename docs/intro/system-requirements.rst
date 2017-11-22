System Requirements
===================

Gthnk requires some software to be installed in order to function.
The following packages should be installed globally, as the superuser, for all users on the system to access.

- Python 3.6, Python 3.5, or Python 2.7.
- Python development libraries (i.e. header files for compiling C code)
- `pip <http://pip.readthedocs.org/en/latest/>`_
- `virtualenv <http://virtualenv.readthedocs.org/en/latest/>`_
- `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/>`_

The following sections describe the process for installing these requirements on various systems.
In each of the following examples, it is assumed you will be using a root account (or some other privileged account).

Windows
-------

First, install Python 3.6 for Windows from https://www.python.org/downloads/windows/.
Then, launch PowerShell and gain administrative privileges.
Finally, use `pip` to perform a site-wide install of several core libraries.

::

    start-process powershell –verb runAs
    pip install virtualenv
    pip install virtualenvwrapper
    pip install virtualenvwrapper-win

Now you have everything needed to install Gthnk on a Windows system.
Read :doc:`installation` to continue.

OSX
---

Gthnk installs pretty easily on OSX with Homebrew.
Make sure you are using the *admin* user for this process, just like a normal Homebrew operation.

::

    brew install python --universal --framework
    brew install pyenv-virtualenv
    brew install pyenv-virtualenvwrapper
    brew install sqlite
    pip install --upgrade pip

Debian/Ubuntu
-------------

*NB: there are currently no startup scripts for Linux.*

gthnk installs cleanly on Debian and Ubuntu systems.

::

    apt-get install python python-dev python-pip build-essential
    apt-get install sqlite-dev
    pip install --upgrade pip
    pip install --upgrade virtualenv
    pip install virtualenvwrapper

Redhat
------

*NB: there are currently no startup scripts for Linux.*

gthnk can be installed on RedHat, but ensure your package manager is installing Python 2.7; as of August 2015, RHEL provides an older version.

::

    yum install python python-devel python-pip
    yum install sqlite-devel
    pip install --upgrade pip
    pip install --upgrade virtualenv
    pip install virtualenvwrapper

Next Steps
----------

Now that you have the system requirements installed, read :doc:`installation` to put **gthnk** on your computer.
