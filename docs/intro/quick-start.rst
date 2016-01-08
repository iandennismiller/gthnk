Quick Start
===========

Installation
------------

Make sure you have the :doc:`system-requirements` installed.  You will need Python, pip, virtualenv, and virtualenvwrapper.

**gthnk** currently installs on OSX systems.  Open a terminal and type the following:

::

    mkvirtualenv gthnk
    pip install gthnk
    install_osx.sh

This will install **gthnk** on your system and make the **gthnk** server start automatically. The setup process will ask you to create an account. See :doc:`installation` for more information about these steps.

Use the Journal
---------------

**gthnk** uses a basic :doc:`/user/text-file-format` because anything more complicated isn't reliable enough for something as important as your thoughts.

Create a file on your desktop called ``journal.txt`` and use a text editor to paste the following into it:

::

    2016-01-08

    0840

    Hello world!  I am making a note in my work journal.

    1322

    The gthnk website is http://gthnk.com

This is a basic journal file for January 8, 2016.  It has two entries, one at 8:40am and another at 1:22pm.  Based in this example, you can probably imagine how to make journal entries for any other day and time.

Accessing the Journal
---------------------

Access **gthnk** in your browser with this URL: http://localhost:1620/admin/journal/latest.html

To immediately load from ``journal.txt``, click the *reload* button in **gthnk**.  You will see that the journal entries have been added to the database and the text file has been reset to a blank file.

Next Steps
----------

Read :doc:`/user/using-the-journal` to understand how to get the most out of **gthnk**.
