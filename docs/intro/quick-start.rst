Quick Start
===========

Installation
------------

Make sure you have the :doc:`system-requirements` installed.  You will need Python, pip, virtualenv, and virtualenvwrapper.

To install **gthnk**, open a terminal and type the following:

::

    mkvirtualenv gthnk
    pip install gthnk
    install_osx.sh

This will install **gthnk** on your system and make the **gthnk** server start automatically. The setup process will ask you to create an account.

See the :doc:`installation` document for a more detailed guide.

Use the Journal
---------------

Create a file on your desktop called ``journal.txt`` and paste the following into it with a text editor:

::

    2016-01-08

    0840

    Hello world!  I am making a note in my work journal.

    0843

    The gthnk website is http://gthnk.com

Now you have a simple journal file.  See :doc:`/user/using-the-journal` to learn what you can do.

Accessing the Journal
---------------------

Access **gthnk** in your browser with this URL: http://localhost:1620/admin/journal/latest.html

Now you have access to your journal.  To immediately load from ``journal.txt``, click the *reload* button in **gthnk**.  You will see that the journal entries have been added to the database and the text file has been reset to a blank file.

Next Steps
----------

Read the following to learn more about **gthnk**:

- :doc:`/user/text-editor-macros`
- :doc:`/user/handwritten-notes-on-paper`
- :doc:`/user/browser-integration`
- :doc:`/user/mobile-devices`
