gthnk
=====

`gthnk <http://www.gthnk.com>`_ is a personal knowledge management system.
Capture your ideas using plain old text files.
Make a journal that lasts 100 years.

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

.. Additional media, including images and PDFs, can be attached to the journal.

The easiest way to run **gthnk** is with Docker.
**gthnk** also installs on Windows, Linux, and MacOS systems with Python 3.5+.
See the `Installation document <http://docs.gthnk.com/en/latest/intro/installation.html>`_ for more details.

Quick Start
^^^^^^^^^^^

Run gthnk locally with a local journal and local database in ``~/.gthnk``.

::

    docker run -d --rm \
        --name gthnk-server \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/.gthnk:/home/gthnk/.gthnk \
        iandennismiller/gthnk

Usage
^^^^^

The default journal where you will record your entries is ``~/.gthnk/journal.txt``.
Open ``journal.txt`` with a text editor to add entries to the journal.

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

Gthnk Interface
^^^^^^^^^^^^^^^

To interact with the gthnk journal, connect to http://localhost:1620 and log in with the username ``gthnk`` and the password ``gthnk``.

Click the **fast-forward** icon to view the live journal buffer.
As you edit ``journal.txt``, this live buffer will be updated.

Once the journals have been rotated, the history of previous days becomes available within the gthnk Interface.

Journal Rotation
^^^^^^^^^^^^^^^^

When the journal rotates, all the entries are imported from ``journal.txt`` into the database.
After import, the ``journal.txt`` file is wiped.

The preferred rotation method method is to use an automatic process like cron, systemd, or launchd.
A complete example, including gthnk server and cron server, is described below and can be launched with ``docker-compose``.

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

Tagging
^^^^^^^

An experimental Tagging feature is available with double-square brackets:

::

    2020-07-04

    0804

    To insert a [[tag]] in [[gthnk]], put one or more words inside square brackets.

Configuration
^^^^^^^^^^^^^

The default configuration file is ``~/.gthnk/gthnk.conf``.

You can edit the configuration - particularly ``INPUT_FILES`` - in order to pull from multiple journal text sources, which can include shared files on other devices.

Using Cloud Sync
^^^^^^^^^^^^^^^^

You can sync gthnk to multiple devices using a cloud file system like Dropbox or Seafile.
Use the ``docker run -v`` flag to point to your cloud storage: ``-v ${PATH_TO_CLOUD}/gthnk:/home/gthnk/.gthnk``

A complete example using Dropbox could look like:

::

    docker run -d --rm \
        --name gthnk-server \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/Dropbox/gthnk:/home/gthnk/.gthnk \
        iandennismiller/gthnk

Running the server with rotation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order for gthnk to rotate the journals automatically, a separate process needs to run periodically.

The full suite of gthnk server processes can be run as:

::

    wget https://github.com/iandennismiller/gthnk/raw/simplify/src/docker/docker-compose.yaml
    docker-compose up -d

Other gthnk Projects
^^^^^^^^^^^^^^^^^^^^

- Python-Markdown Journal Extension: https://github.com/iandennismiller/mdx_journal
- VS Code Extension: https://github.com/iandennismiller/vscode-gthnk
- gthnk Presentation: https://github.com/iandennismiller/pres-gthnk-overview
- Chrome App: https://github.com/iandennismiller/gthnk/tree/master/src/chrome-app
- Website Repo: https://github.com/iandennismiller/www-gthnk

Documentation
^^^^^^^^^^^^^

http://docs.gthnk.com
