Browser Integration
===================

**gthnk** runs a private web server that only you can connect to.  There are a few browser tricks that make it easier to get extra use out of **gthnk**.

Google Chrome
-------------

Search Bar
^^^^^^^^^^

1. In chrome, visit chrome://settings
2. Click *Manage search engines...* (or click chrome://settings/searchEngines)
3. Scroll to the bottom of the list of search engines and *Add a new search engine*
    1. call it "gthnk"
    2. use a simple keyword like "j" for journal
    3. paste the following: http://localhost:1620/admin/journal/search?q=%s

Now you can quickly search the journal in the search bar.  For example, if you knew you saved a URL in the last week, you might type the following in the search bar:

::

    "j http"

That would search **gthnk** for anything matching *http*, which would hopefully find the URL you bookmarked.

App Launcher
^^^^^^^^^^^^

The **gthnk** Google Chrome extension enables **gthnk** to be launched from the menu bar using the Chrome Launcher.

1. Download the extension code from github

::

    git clone https://github.com/iandennismiller/gthnk.git

2. Open chrome://extensions/ in your browser
3. Check *Developer mode*
4. Click *Load unpacked extension...*
5. Navigate to gthnk/integrations/chrome-app
6. Click *OK*

Now, you have an icon that will launch **gthnk**.

Other Browsers
--------------

Since **gthnk** is provided as a web server, you can use any browser to connect to it.  If you craft integrations for other browsers, please `create an issue <https://github.com/iandennismiller/gthnk/issues>`_ that describes your process and we can add it to this document.
