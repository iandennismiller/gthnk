Using the Journal
=================

An *entry* is denoted by a *timestamp*, which is written using hours and minutes, like ``0815`` for 8:15am and ``1425`` for 2:25pm.  A *day* is denoted by a *datestamp*, which is written using year-month-day, like ``2016-01-08`` for January 8, 2016.  Usually, :doc:`/user/text-editor-macros` will do this for you, so you really don't need to worry about it.  Read more about the :doc:`text-file-format` to learn other tricks.

The default **Gthnk** installation will create a file on your desktop called ``journal.txt``.  This file is called a "journal buffer" and anything you write in it will be added to the journal once per day.  You can change the location of this file by editing ``~/.gthnk/gthnk.conf`` and changing the ``INPUT_FILES`` entry.

Example
^^^^^^^

A simple journal consisting of 1 day and 3 entries looks like this:

::

    2016-01-08

    0840

    Hello world!  I am making a note in my work journal.

    1825

    The gthnk website is http://gthnk.com

    2210

    I had an interesting thought.  What if...


There is no limit to the number of days you can have in a journal buffer.  It is also possible to use multiple journal buffers in order to gather entries from :doc:`/user/mobile-devices`.

Accessing the Journal
---------------------

Access **Gthnk** in your browser with this URL: http://localhost:1620/day/live

:doc:`/user/browser-integration` makes it easy to search **Gthnk** by keyword, so you can easily find old entries.  A variety of GUI methods enable navigation between days.

Daily Journal Maintenance
-------------------------

Every day, **Gthnk** automatically does two maintenance tasks:

- Just after midnight, **Gthnk** will collect any new journal entries for the day and store them in the database.
- At 9:00am, **Gthnk** will open a browser window with the previous day's entries.

Next Steps
----------

Read the following to learn more about **Gthnk**:

- :doc:`/user/text-editor-macros`
- :doc:`/user/browser-integration`
- :doc:`/user/mobile-devices`
- :doc:`/user/text-file-format`
