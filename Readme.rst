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

User Interface
^^^^^^^^^^^^^^

To interact with the gthnk journal, connect to http://localhost:1620 and log in with the username ``gthnk`` and the password ``gthnk``.

Click the **fast-forward** icon to view the live journal buffer.
As you edit ``journal.txt``, this live buffer will be updated.

Once the journals have been rotated, the history of previous days becomes available within the gthnk Interface.

Journal Rotation
^^^^^^^^^^^^^^^^

When the journal rotates, all the entries are imported from ``journal.txt`` into the database.
After import, the ``journal.txt`` file is wiped.

The preferred rotation method method is to use an automatic process like ``cron``, ``systemd``, or ``launchd``.
A full server with rotation using ``docker-compose`` is available in the readme.

The journal can be manually rotated using the interface by clicking the **refresh** button in the hamburger menu.

Before ``journal.txt`` is wiped, its contents are backed up to ``~/.gthnk/backups`` - so information is never lost even if there is a problem with rotation.

Integration with Text Editors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Text editor integrations make it easier to insert journal entries.

- VS Code: https://marketplace.visualstudio.com/items?itemName=IanDennisMiller.gthnk
- Sublime Text: https://github.com/iandennismiller/gthnk/tree/master/src/sublime-text-plugin

After installing the plugin for your editor, the following key combinations are available:

- Ctrl-Alt-Cmd-N: Insert date marker YYYYMMDD
- Ctrl-Alt-Cmd-M: Insert time marker HHMM

Tags
^^^^

Tagging is available with double-square brackets:

::

    2020-07-04

    0804

    To insert a [[tag]] in [[gthnk]], put one or more words inside square brackets.

A tag links to all other entries containing the tag or fulltext keyword.

Configuration
^^^^^^^^^^^^^

The default configuration file is ``~/.gthnk/gthnk.conf``.
This file can be edited to change the location of input journal files, database, logging, and other system parameters.

In particular, you can change ``INPUT_FILES`` to pull from multiple journal text sources including shared files on other devices.

Cloud Sync
^^^^^^^^^^

You can sync gthnk to multiple devices using a cloud file system like Dropbox or Seafile.
Use the ``docker run -v`` flag to point to your cloud storage: ``-v ${PATH_TO_CLOUD}/gthnk:/home/gthnk/cloud-storage``

A complete example using Dropbox could look like:

::

    docker run -d --rm \
        --name gthnk-server \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/.gthnk:/home/gthnk/.gthnk \
        -v ~/Dropbox/gthnk:/home/gthnk/cloud-storage \
        iandennismiller/gthnk

This configuration supports running gthnk on a dedicated server, like a local Linux machine, while editing the journal files on devices that are synced via the cloud.

To support a laptop and phone, edit ``~/.gthnk/gthnk.conf`` to specify multiple INPUT_FILES located on cloud storage.

::

    INPUT_FILES = "/home/gthnk/cloud-storage/journal-laptop.txt,/home/gthnk/cloud-storage/journal-phone.txt"

Full Server with Rotation
^^^^^^^^^^^^^^^^^^^^^^^^^

In order for gthnk to rotate the journals automatically, a separate process needs to run periodically.

The full suite of gthnk server processes can be run as:

::

    wget https://github.com/iandennismiller/gthnk/raw/master/src/docker/docker-compose.yaml
    docker-compose up -d

Other gthnk Resources
^^^^^^^^^^^^^^^^^^^^^

- Project repository
    - https://github.com/iandennismiller/gthnk
- Public website
    - http://www.gthnk.com
    - repo: https://github.com/iandennismiller/www-gthnk
- Read The Docs
    - https://readthedocs.org/projects/gthnk
    - repo: https://github.com/iandennismiller/gthnk/tree/master/docs
- Python Package Index
    - https://pypi.org/project/gthnk/
- Presentation
    - https://iandennismiller.github.io/pres-gthnk-overview
    - repo: https://github.com/iandennismiller/pres-gthnk-overview
- Chat room (matrix)
    - https://riot.im/app/#/room/#gthnk:matrix.org
- Continuous Integration
    - https://travis-ci.org/iandennismiller/gthnk
- Code Coverage
    - https://coveralls.io/github/iandennismiller/gthnk
- VS Code Extension
    - https://marketplace.visualstudio.com/items?itemName=IanDennisMiller.gthnk
    - repo: https://github.com/iandennismiller/vscode-gthnk
- Chrome App
    - https://github.com/iandennismiller/gthnk/tree/master/src/chrome-app
- Python-Markdown gthnk journal Extension
    - https://pypi.org/project/mdx_journal/
    - repo: https://github.com/iandennismiller/mdx_journal

Diamond Methods
^^^^^^^^^^^^^^^

- Routine
    - http://www.idmiller.com/books/routine/index.html
    - https://www.amazon.com/Routine-Reflection-Ian-Dennis-Miller/dp/1974269108
- Project System
    - https://project-system.readthedocs.io/en/latest/
    - python: https://pypi.org/project/project-system/
    - repo: https://github.com/iandennismiller/project-system
- Diamond Patterns
    - https://diamond-patterns.readthedocs.io/en/latest/
    - python: https://pypi.org/project/diamond-patterns/
    - repo: https://github.com/iandennismiller/diamond-patterns
- Gthnk
    - http://www.gthnk.com
    - python: https://pypi.org/project/gthnk/
    - repo: https://github.com/iandennismiller/gthnk

Documentation
^^^^^^^^^^^^^

http://docs.gthnk.com
