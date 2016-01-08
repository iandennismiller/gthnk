Text Editor Macros
==================

It would be pretty annoying to manually type out a timestamp every time you wanted to make a journal entry.  Luckily, many text editors can be extended with macros to make this automatic.

Sublime Text
------------

I personally use Sublime Text 3 as my primary method for editing my work journal.  The following steps will help you extend Sublime Text 3 to add datestamps and timestamps using a key combination.

1. Download `journal_date.py <https://raw.githubusercontent.com/iandennismiller/gthnk/master/integration/sublime-text/journal_date.py>`_
2. Copy ``journal_date.py`` to the Sublime Text 3 Packages directory

::

    cp journal_date.py "$HOME/Library/Application Support/Sublime Text 3/Packages/User"

3. Add the following to ``Default (OSX).sublime-keymap``

::

    [
        { "keys": ["ctrl+super+alt+n"], "command": "insert_date" },
        { "keys": ["ctrl+super+alt+m"], "command": "insert_time" }
    ]

This creates two hotkeys that will automatically insert datestamps and timestamps.  You can change the keymap however you want to make the hotkeys convenient for you.

Jota+
-----

Jota+ for Android enables me to add notes to my journal using a phone or tablet.  I create a file in dropbox called ``journal-phone.txt`` and add regular entries to it, just like always.

Jota+ provides macros, but it calls them *fixed phrases*.  You can create two *fixed phrases* for adding datestamps and timestamps:

- datestamp: ``%yyyy%-%MM%-%dd%``
- timestamp: ``%HH%%mm%``

Be sure that the fixed phrases include blank lines around the timestamp.

Other text editors
------------------

Any text editor that provides macros for the date and time is likely to support **gthnk**.  If you successfully set up another text editor, please `create an issue <https://github.com/iandennismiller/gthnk/issues>`_ that describes your process and we can add it to this document.
