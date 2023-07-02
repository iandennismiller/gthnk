Gthnk
=====

`Gthnk <http://www.gthnk.com>`_ is a personal knowledge management system.
Capture your ideas using plain old text files.
Make a journal that lasts 100 years.

.. image:: https://img.shields.io/pypi/v/gthnk.svg
    :target: https://pypi.org/project/gthnk/
    :alt: Python Package

.. image:: https://readthedocs.org/projects/gthnk/badge/?version=latest
    :target: https://gthnk.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/github/stars/iandennismiller/gthnk.svg?style=social&label=GitHub
    :target: https://github.com/iandennismiller/gthnk
    :alt: Github Project

Overview
--------

- **Gthnk** presents a **journal** consisting of many **entries**.
- **Entries** are created using plain old text files, which **Gthnk** imports once per day.
- Any text editor can be used to add information to **Gthnk**.
- **Entries** are searchable using the embedded **Gthnk** server, which can be accessed with a browser.
- Plain-text enables backup/restore via hardcopy (e.g. paper) for long-term archival.

The easiest way to run **Gthnk** is with Docker.
**Gthnk** also installs on Windows, Linux, and MacOS systems with Python 3.5+.
See the `Installation document <https://gthnk.readthedocs.io/en/latest/intro/installation.html>`_ for more details.

Quick Start
^^^^^^^^^^^

Use Docker to run Gthnk with all files stored locally in ``~/.gthnk``.

::

    docker run -d --rm \
        --name gthnk \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/.gthnk:/opt/gthnk/var \
        iandennismiller/gthnk:0.8.1

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

Those two delimiters - date and time followed by a blank line - are all there is to the Gthnk journal file format.
The rest is Markdown.

You can add multiple entries per day - and multiple days in a single journal - by inserting date and time markers as you work.

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^

While the Docker container is running, the Gthnk command line interface is available using ``docker exec``.
Create a shell alias to simplify access.

::

    alias gthnk="docker exec -it gthnk /opt/gthnk/.venv/bin/gthnk"
    gthnk --help

To view the current journal buffer, use ``gthnk buffer``.

To search for a keyword, use ``gthnk search``.

Web Interface
^^^^^^^^^^^^^

To interact with the Gthnk journal, connect to http://localhost:1620.

Click the **fast-forward** icon to view the live journal buffer.
As you edit ``journal.txt``, this live buffer will be updated.

Once the journals have been rotated, the history of previous days becomes available within the Gthnk Interface.

Journal Rotation
^^^^^^^^^^^^^^^^

When the journal rotates, all the entries are imported from ``journal.txt`` into the database.
After import, the ``journal.txt`` file is wiped.

The preferred rotation method method is to use an automatic process like ``cron``, ``systemd``, or ``launchd``.
The journal can be manually rotated with the command line interface: ``gthnk rotate``.

Before ``journal.txt`` is wiped, its contents are backed up.
Information is never lost even if there is a problem with rotation.

Integration with Text Editors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Text editor integrations make it easier to insert journal entries.

- VS Code: https://marketplace.visualstudio.com/items?itemName=IanDennisMiller.gthnk
- Sublime Text: https://github.com/iandennismiller/sublime-text-gthnk

After installing the plugin for your editor, the following key combinations are available:

- Ctrl-Alt-Cmd-N: Insert date marker YYYYMMDD
- Ctrl-Alt-Cmd-M: Insert time marker HHMM

Cloud Sync
^^^^^^^^^^

You can sync Gthnk to multiple devices using a cloud file system like Dropbox or Syncthing.
Use the ``docker run -v`` flag to point to your cloud storage: ``-v ${PATH_TO_CLOUD}/gthnk:/opt/gthnk/var``

A complete example using Dropbox could look like:

::

    docker run -d --rm \
        --name gthnk-server \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/Dropbox/gthnk:/opt/gthnk/var \
        iandennismiller/gthnk:0.8.1

This configuration supports running Gthnk on a dedicated server, like a local Linux machine, while editing the journal files on devices that are synced via the cloud.

To support a laptop and phone, use a custom configuration file.

::

    docker run -d --rm \
        --name gthnk-server \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/.gthnk/gthnk.conf:/opt/gthnk/.config/gthnk/gthnk.conf \
        -v ~/Dropbox/gthnk:/opt/gthnk/var
        iandennismiller/gthnk:0.8.1

Then edit ``~/.gthnk/gthnk.conf`` to specify multiple INPUT_FILES.

::

    INPUT_FILES = "/opt/gthnk/var/journal-laptop.txt,/opt/gthnk/var/journal-phone.txt"

Other Gthnk Resources
^^^^^^^^^^^^^^^^^^^^^

- `Project repository <https://github.com/iandennismiller/gthnk>`_
- `Public website <http://www.gthnk.com>`_ - `website repo <https://github.com/iandennismiller/www-gthnk>`_
- `Read The Docs <https://gthnk.readthedocs.io/en/latest/>`_ - `project <https://readthedocs.org/projects/gthnk>`_ - `docs repo <https://github.com/iandennismiller/gthnk/tree/master/docs>`_
- `Python Package Index <https://pypi.org/project/gthnk/>`_
- `Presentation: Overview of Gthnk <https://iandennismiller.github.io/pres-gthnk-overview>`_ - `presentation repo <https://github.com/iandennismiller/pres-gthnk-overview>`_
- `Continuous Integration <https://travis-ci.org/iandennismiller/gthnk>`_
- `VS Code Extension <https://marketplace.visualstudio.com/items?itemName=IanDennisMiller.gthnk>`_ - `vsc extension repo <https://github.com/iandennismiller/vscode-gthnk>`_
- `Chrome App <https://github.com/iandennismiller/gthnk/tree/master/share/chrome-app>`_
- `Python-Markdown gthnk journal Extension <https://pypi.org/project/mdx_journal/>`_ - `mdx_journal repo <https://github.com/iandennismiller/mdx_journal>`_

Documentation
^^^^^^^^^^^^^

http://docs.gthnk.com
