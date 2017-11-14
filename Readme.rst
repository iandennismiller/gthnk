gthnk
=====

`gthnk <http://gthnk.com>`_ is a personal knowledge management system.  Capture your ideas using plain old text files without any cloud services.

Read the `Quick Start <http://gthnk.readthedocs.org/en/latest/intro/quick-start.html>`_ to try it yourself.

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

**gthnk** presents a *journal* consisting of many *entries*. Entries are created using plain old text files, which **gthnk** imports once per day.  Any text editor can be used to add information to **gthnk**.  Entries are searchable using the embedded **gthnk** server, which can be accessed with a browser. Additional media, including images and PDFs, can be attached to the journal.

Installation
^^^^^^^^^^^^

**gthnk** currently installs on OSX systems. See the `Installation document <http://gthnk.readthedocs.org/en/latest/intro/installation.html>`_ for more details.

First install ImageMagick 6.

::

    brew install imagemagick@6
    brew link --force --overwrite imagemagick@6

Then install gthnk.

::

    mkvirtualenv gthnk
    pip install gthnk
    install_osx.sh

Documentation
^^^^^^^^^^^^^

http://gthnk.readthedocs.org
