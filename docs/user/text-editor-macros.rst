Text Editor Macros
==================

It would be pretty annoying to manually type out a timestamp every time you wanted to make a journal entry.  Luckily, many text editors can be extended with macros to make this automatic.

Sublime Text
------------

Download 


Add the following to ``Default (OSX).sublime-keymap``

::

    [
        { "keys": ["ctrl+super+alt+n"], "command": "insert_date" },
        { "keys": ["ctrl+super+alt+m"], "command": "insert_time" }
    ]



Jota+ for Android
-----------------

