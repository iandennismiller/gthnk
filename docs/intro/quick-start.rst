Quick Start
===========

The simplest installation method is to use Docker.

::

    docker run -d --rm \
        --name gthnk \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/.gthnk:/opt/gthnk/var \
        iandennismiller/gthnk:0.8

However, advanced methods are also available to install **Gthnk** as a Python package.
Read :doc:`installation` for more installation options.

Use the Journal
---------------

**Gthnk** uses a basic :doc:`/user/text-file-format` because anything more complicated isn't reliable enough for something as important as your thoughts.

Create a file called ``~/.gthnk/journal.txt`` and use a text editor to paste the following into it:

::

    2016-01-08

    0840

    Hello world!  I am making a note in my work journal.

    1322

    The Gthnk website is http://gthnk.com

This is a basic journal file for January 8, 2016.  It has two entries, one at 8:40am and another at 1:22pm.
Based in this example, you can probably imagine how to make journal entries for any other day and time.

Accessing the Journal
---------------------

Access **Gthnk** in your browser with this URL: http://localhost:1620/

You will see that the journal entries have been added to the database and the text file has been reset to a blank file.

Next Steps
----------

Read :doc:`/user/using-the-journal` to understand how to get the most out of **Gthnk**.
