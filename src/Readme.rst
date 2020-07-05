gthnk
=====

`gthnk <http://www.gthnk.com>`_ is a personal knowledge management system.
Capture your ideas using plain old text files.
Make a journal that lasts 100 years.

.. image:: https://img.shields.io/pypi/v/gthnk.svg
    :target: https://pypi.org/project/gthnk/
    :alt: Python Package

.. image:: https://readthedocs.org/projects/gthnk/badge/?version=latest
    :target: https://gthnk.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://travis-ci.org/iandennismiller/gthnk.svg?branch=master
    :target: https://travis-ci.org/github/iandennismiller/gthnk
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/iandennismiller/gthnk/badge.svg?branch=master
    :target: https://coveralls.io/github/iandennismiller/gthnk
    :alt: Coverage Status

.. image:: https://img.shields.io/github/stars/iandennismiller/gthnk.svg?style=social&label=GitHub
    :target: https://github.com/iandennismiller/gthnk
    :alt: Github Project

Overview
--------

- **gthnk** presents a **journal** consisting of many **entries**.
- **Entries** are created using plain old text files, which **gthnk** imports once per day.
- Any text editor can be used to add information to **gthnk**.
- **Entries** are searchable using the embedded **gthnk** server, which can be accessed with a browser.
- Plain-text enables backup/restore via hardcopy (e.g. paper) for long-term archival.

.. Additional media, including images and PDFs, can be attached to the journal.

The easiest way to run **gthnk** is with Docker.
**gthnk** also installs on Windows, Linux, and MacOS systems with Python 3.5+.
See the `Installation document <https://gthnk.readthedocs.io/en/latest/intro/installation.html>`_ for more details.

Quick Start
^^^^^^^^^^^

Use Docker to run gthnk with all files stored locally in ``~/.gthnk``.

::

    docker run -d --rm \
        --name gthnk-server \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/.gthnk:/home/gthnk/.gthnk \
        iandennismiller/gthnk

The default text file where you will record journal entries is ``~/.gthnk/journal.txt``.

Open ``journal.txt`` with a text editor to add new journal entries.

Open http://localhost:1620 to access the user interface.

Journal Entries
^^^^^^^^^^^^^^^

Use the journal by editing ``journal.txt`` with a text editor.
First, insert a date marker **YYYY-MM-DD** and a blank line to start a new journal day.
Then, insert a time marker **HHMM** and a blank line to start a journal entry.

::

    2020-07-04

    0804

    This is a simple journal entry.

    0805

    And this is a separate entry, a minute later.

Those two delimiters - date and time followed by a blank line - are all there is to the gthnk journal file format.
The rest is Markdown.

You can add multiple entries per day - and multiple days in a single journal - by inserting date and time markers as you work.

Documentation
^^^^^^^^^^^^^

http://docs.gthnk.com
