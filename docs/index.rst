.. gthnk documentation master file

Overview
========

- **Gthnk** presents a **journal** consisting of many **entries**.
- **Entries** are created using plain old text files, which **Gthnk** imports once per day.
- Any text editor can be used to add information to **Gthnk**.
- **Days** and **Entries** are searchable from the command line and web UI.

Try Gthnk
---------

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

Introduction
------------

.. toctree::
    :maxdepth: 1

    intro/quick-start
    intro/system-requirements
    intro/installation

User Guide
----------

.. toctree::
    :maxdepth: 1

    user/using-the-journal
    user/text-editor-macros
    user/browser-integration
    user/mobile-devices
    user/text-file-format
    user/uninstallation

Community
---------

.. toctree::
    :maxdepth: 1

    community/contributing
    community/developer

Development
-----------

.. toctree::
    :maxdepth: 1

    dev/release

About
-----

.. toctree::
    :maxdepth: 1

    about/vision
    about/history
    changelog
    License
