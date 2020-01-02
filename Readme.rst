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

Quick Start
^^^^^^^^^^^

::

    docker run -d --rm \
        --name gthnk \
        -p 1620:1620 \
        -v ~/.gthnk:/home/gthnk/storage \
        iandennismiller/gthnk

Usage
^^^^^

The default journal is ~/.gthnk/journal.txt, where you will record your notes.
Open ``journal.txt`` with a text editor:

::

    code ~/.gthnk/journal.txt

Journal Entries
^^^^^^^^^^^^^^^

To get started with ``journal.txt``, insert a date marker (Ctrl-Alt-Cmd-N) to start a new journal day.
Then, insert a time marker (Ctrl-Alt-Cmd-M) to start a journal entry.
Now you can compose your note in ``journal.txt``.

You can add multiple entries per day - and even multiple days - by inserting date and time markers as you work.

Gthnk Interface
^^^^^^^^^^^^^^^

To interact with the Gthnk journal, connect to http://localhost:1620 and log in with the username ``user@example.com`` and the password ``secret``.

Click the **refresh** icon in the Journal interface to make Gthnk import from ``journal.txt``.
Now your journal entries are indexed and searchable - and ``journal.txt`` is a blank document waiting for your next entries.

Next Steps
^^^^^^^^^^

Gthnk can do much more than this - `see the Gthnk website <http://www.gthnk.com>`_ to learn about Gthnk.

Documentation
^^^^^^^^^^^^^

http://docs.gthnk.com
