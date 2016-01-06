gthnk
=====

**gthnk** is a personal knowledge management system.  Securely record your thoughts without depending upon cloud services.

Overview
--------

**gthnk** presents a *journal* consisting of many *entries*. Entries are created using plain old text files, which **gthnk** will import every 24 hours.  Any text editor can be used to add information to **gthnk**.  Entries are searchable using the embedded **gthnk** server, which can be accessed with a browser. Additional media, including images and PDFs, can be attached to the journal.

Installation
^^^^^^^^^^^^

**gthnk** currently installs on OSX systems.

::

    mkvirtualenv gthnk
    pip install gthnk
    install_osx.sh

Linux support is coming.

Documentation
^^^^^^^^^^^^^

http://gthnk.readthedocs.org

Flask-Diamond
^^^^^^^^^^^^^

**gthnk** serves as the `Flask-Diamond <http://flask-diamond.readthedocs.org>`_ reference application.  One of the purposes of **gthnk** is to demonstrate a real-world use for `Flask-Diamond <http://flask-diamond.readthedocs.org>`_.
