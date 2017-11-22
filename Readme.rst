gthnk
=====

`gthnk <http://gthnk.com>`_ is a personal knowledge management system.
Capture your ideas using plain old text files without any cloud services.

Read the `Quick Start <http://gthnk.readthedocs.io/en/latest/intro/quick-start.html>`_ to try it yourself.

.. image:: https://img.shields.io/github/stars/iandennismiller/gthnk.svg?style=social&label=GitHub
    :target: https://github.com/iandennismiller/gthnk

.. image:: https://img.shields.io/pypi/v/gthnk.svg
    :target: https://pypi.python.org/pypi/gthnk

.. image:: https://readthedocs.org/projects/gthnk/badge/?version=latest
    :target: http://gthnk.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/iandennismiller/gthnk.svg?branch=master
    :target: https://travis-ci.org/iandennismiller/gthnk

.. image:: https://coveralls.io/repos/github/iandennismiller/gthnk/badge.svg?branch=master
    :target: https://coveralls.io/github/iandennismiller/gthnk?branch=master

Overview
--------

**gthnk** presents a *journal* consisting of many *entries*.
Entries are created using plain old text files, which **gthnk** imports once per day.
Any text editor can be used to add information to **gthnk**.
Entries are searchable using the embedded **gthnk** server, which can be accessed with a browser.
Additional media, including images and PDFs, can be attached to the journal.

**gthnk** installs on Windows and OSX systems with Python 3.5+ and Python 2.7.
See the `Installation document <http://gthnk.readthedocs.io/en/latest/intro/installation.html>`_ for more details.

Install Windows
^^^^^^^^^^^^^^^

Ensure you have the `System Requirements <http://gthnk.readthedocs.io/en/latest/intro/system-requirements.html>`_ installed: Python 3.6, ``virtualenv``, ``virtualenvwrapper``, and ``virtualenvwrapper-win``.
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

Ensure you have the `System Requirements <http://gthnk.readthedocs.io/en/latest/intro/system-requirements.html>`_ installed: Python 3.6, ``virtualenv``, and ``virtualenvwrapper``.
Once the requirements are installed, launch ``terminal.app`` and run the following:

::

    mkvirtualenv gthnk
    workon gthnk
    pip install gthnk
    integration.py install

Documentation
^^^^^^^^^^^^^

http://gthnk.readthedocs.io
