Using the Journal
=================

Create a file on your desktop called ``journal.txt`` and open it with a text editor.  This file is called a "journal buffer" and anything you write in it will be added to the journal once per day.  You can change this file by editing ``INPUT_FILES`` in the configuration file ``~/Library/Gthnk/gthnk.conf``.

An *entry* is denoted by a *timestamp*, which is written using hours and minutes, like ``0815`` for 8:15am and ``1425`` for 2:25pm.  A *day* is denoted by a *datestamp*, which is written using year-month-day, like ``2016-01-08`` for January 8, 2016.  Usually, :doc:`/user/text-editor-macros` will do this for you, so you really don't need to worry about it.

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

Access **gthnk** in your browser with this URL: http://localhost:1620/admin/journal/latest.html

:doc:`/user/browser-integration` makes it easy to search **gthnk** by keyword, so you can easily find old entries.  A variety of GUI methods enable navigation between days.

Daily Journal Maintenance
-------------------------

Every day, **gthnk** automatically does two maintenance tasks:

- Just after midnight, **gthnk** will collect any new journal entries for the day and store them in the database.
- At 9:00am, **gthnk** will open a browser window with the previous day's entries.

Attachments
-----------

Archive images and PDFs in the journal by dragging those files onto the "Attachments" target in the GUI.  Use this to attach :doc:`/user/handwritten-notes-on-paper` to your digital entries, bridging the gap with the writing/drawing experience.

Next Steps
----------

Read the following to learn more about **gthnk**:

- :doc:`/user/text-editor-macros`
- :doc:`/user/handwritten-notes-on-paper`
- :doc:`/user/browser-integration`
- :doc:`/user/mobile-devices`
