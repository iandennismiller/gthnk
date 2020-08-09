Text File Format
================

**Gthnk** uses a basic text file format because anything more complicated isn't reliable enough for something as important as your thoughts.  Even though journal entries are stored in a sqlite3 database for fast indexing, they are also exported as plain text files every night.

Text Formatting
---------------

There are a few simple rules that serve to partition a text file into a sequence of journal entries.

Timestamp and Datestamp
^^^^^^^^^^^^^^^^^^^^^^^

An *entry* is denoted by a *timestamp*, which is written using hours and minutes, like ``0815`` for 8:15am and ``1425`` for 2:25pm.  This must have a blank line before it and a blank line after it.

A *day* is denoted by a *datestamp*, which is written using year-month-day, like ``2016-01-08`` for January 8, 2016.  This must have a blank line before it and a blank line after it.

Markdown
^^^^^^^^

Any journal entry may contain Markdown.  This makes it easy to add lists and URLs.  You don't have to do anything special to enable Markdown.

Custom Markdown Extension
^^^^^^^^^^^^^^^^^^^^^^^^^

To support rendering **Gthnk** journals in a more aesthetically pleasing way, `mdx_journal <https://github.com/iandennismiller/mdx_journal>`_ was written to provide a minor extension to basic markdown.  This extension will cause datestamps to become large headings and timestamps to become slightly smaller headings.  It makes a day's entries much more readable.

Filesystem Exports
------------------

One of the goals for using text files is to ensure the journal has a higher likelihood of being readable to future generations.  One thing we've learned is that file formats can become obsolete in a matter of years. However, ASCII text has been with us since 1960, so let's stick with what works.
