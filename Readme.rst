Gthnk
=====

`Gthnk <http://www.gthnk.com>`_ is a personal knowledge management system.
Capture your ideas using plain old text files without any cloud services.

Start using Gthnk now with our `Installation Wizard <http://install.gthnk.com>`_ for Windows and OS X.

.. image:: https://img.shields.io/pypi/v/gthnk.svg
    :target: http://python.gthnk.com

.. image:: https://readthedocs.org/projects/gthnk/badge/?version=latest
    :target: http://docs.gthnk.com
    :alt: Documentation Status

.. image:: https://travis-ci.org/iandennismiller/gthnk.svg?branch=master
    :target: http://builds.gthnk.com

.. image:: https://coveralls.io/repos/github/iandennismiller/gthnk/badge.svg?branch=master
    :target: http://coverage.gthnk.com

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/github/stars/iandennismiller/gthnk.svg?style=social&label=GitHub
    :target: https://github.com/iandennismiller/gthnk

Overview
--------

**gthnk** presents a *journal* consisting of many *entries*.
Entries are created using plain old text files, which **gthnk** imports once per day.
Any text editor can be used to add information to **gthnk**.
Entries are searchable using the embedded **gthnk** server, which can be accessed with a browser.
Additional media, including images and PDFs, can be attached to the journal.

**gthnk** installs on Windows and OSX systems with Python 3.5+ and Python 2.7.
See the `Installation document <http://docs.gthnk.com/en/latest/intro/installation.html>`_ for more details.

Install Windows
^^^^^^^^^^^^^^^

Ensure you have the `System Requirements <http://docs.gthnk.com/en/latest/intro/system-requirements.html>`_ installed: Python 3.6, ``virtualenv``, ``virtualenvwrapper``, and ``virtualenvwrapper-win``.
Once the requirements are installed, launch `cmd.exe` and run the following:

::

    mkvirtualenv gthnk
    workon gthnk
    easy_install -U mr.bob==0.1.2
    pip install gthnk
    python %virtual_env%\Scripts\integration.py install
    gthnk

Install OS X
^^^^^^^^^^^^

Ensure you have the `System Requirements <http://docs.gthnk.com/en/latest/intro/system-requirements.html>`_ installed: Python 3.6, ``virtualenv``, and ``virtualenvwrapper``.
Once the requirements are installed, launch ``terminal.app`` and run the following:

::

    mkvirtualenv gthnk
    workon gthnk
    pip install gthnk
    integration.py install

Documentation
^^^^^^^^^^^^^

http://docs.gthnk.com
