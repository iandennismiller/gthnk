Mobile Devices
==============

One of the key features of **gthnk** is that it runs on your computer - not in the cloud - so you can keep your thoughts private.  However, sometimes you're on the road and you really want to write something down.

This scenario is no problem for **gthnk** - just use a service like Dropbox or Seafile to sync your journal buffers back to your computer.  This permits you to take non-sensitive notes even when you're not by your computer.

Journal buffers via Dropbox
---------------------------

**gthnk** can import any number of journal buffers every day.  Edit ``INPUT_FILES`` in the configuration file ``~/Library/Gthnk/gthnk.conf`` and add any Dropbox files there.

Since Dropbox is usually ``~/Dropbox``, you might create a file called ``~/Dropbox/journal-phone.txt`` for capturing notes that come from your phone.  To accomplish this, you would edit the configuration like this:

::

    INPUT_FILES = "/Users/me/Dropbox/journal-phone.txt,/Users/me/Desktop/journal.txt"

Now **gthnk** will import entries from the file on your Desktop and from your phone.  It doesn't matter if these files are empty most of the time; that doesn't bother **gthnk**.

Mobile Text Editors
-------------------

- `Jota+ for Android <https://play.google.com/store/apps/details?id=jp.sblo.pandora.jota.plus&hl=en>`_ supports Dropbox and supports macros.

Have you had success with other mobile text editors?  Please `create an issue <https://github.com/iandennismiller/gthnk/issues>`_ that describes your experience and we can add it to this document.
