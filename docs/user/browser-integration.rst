Browser Integration
===================

**Gthnk** runs a private web server that only you can connect to.
There are a few browser tricks that make it easier to get extra use out of **Gthnk**.

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

That would search **Gthnk** for anything matching *http*, which would hopefully find the URL you bookmarked.

App Launcher
^^^^^^^^^^^^

1. Enable the necessary Chrome flags
    1. chrome://flags
    2. chrome://flags/#bookmark-apps - Enable
    3. chrome://flags/#disable-hosted-apps-in-windows - Enable
2. Add Gthnk as an App
    1. Navigate to http://localhost:1620/admin/journal/latest.html
    2. Click the 3-dot "more" tool button
    3. Click "More Tools"
    4. Click "Add to Applications"
    5. Call it "Gthnk"
3. Done

Chrome Extension
^^^^^^^^^^^^^^^^

This method has been replaced by the App Launcher, which is better...

The **Gthnk** Google Chrome extension enables **Gthnk** to be launched from the menu bar using the Chrome Launcher.

1. Download the extension code from github

::

    git clone https://github.com/iandennismiller/gthnk.git

2. Open chrome://extensions/ in your browser
3. Check *Developer mode*
4. Click *Load unpacked extension...*
5. Navigate to gthnk/integrations/chrome-app
6. Click *OK*

Now, you have an icon that will launch **Gthnk**.

Hotkey
^^^^^^

I use Spark.app to create a hotkey pattern for launching the Gthnk app.

- https://github.com/Jean-Daniel/Spark
- https://www.shadowlab.org/softwares/spark.php

Many launchers will work, but the important part is that you must create an "App Launcher" for Gthnk before the hotkey can be created.

Steps for adding a Gthnk hotkey:

1. Click the gear icon to drop down the list of things to create
2. Choose `Application`
3. Set a unique shortcut key combination
4. name it `Gthnk`
5. Action: `Launch`
6. Choose: locate the gthnk chrome app
    1. Navigate to wherever your apps are and looks for `Chrome Apps`
    2. On OS X, this is probably `/Applications/Chrome Apps`
    3. Select `Gthnk` in the `Chrome Apps` folder
7. Done

Other Browsers
--------------

Since **Gthnk** is provided as a web server, you can use any browser to connect to it.  If you craft integrations for other browsers, please `create an issue <https://github.com/iandennismiller/gthnk/issues>`_ that describes your process and we can add it to this document.
