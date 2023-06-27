Installation
============

There are currently two ways to install **Gthnk**:

1. Run it inside a Docker image
2. Install as a python package

Docker Image
------------

Use Docker to run **Gthnk** with all files stored locally in ``~/.gthnk``.

::

    docker run -d --rm \
        --name gthnk \
        -p 1620:1620 \
        -e TZ=America/Toronto \
        -v ~/.gthnk:/opt/gthnk/var \
        iandennismiller/gthnk:0.8

The default text file where you will record journal entries is ``~/.gthnk/journal.txt``.

If you want to store your files somewhere other than ``~/.gthnk`` then update the ``-v`` argument:

::

        -v /opt/somewhere-else:/opt/gthnk/var \

If you want to use a port other than 1620, update the ``-p`` argument:

::

        -p 5000:1620 \

Python Installation
-------------------

**Gthnk** also installs as a python package - but the Docker method is strongly recommended.

Every system is different but python installation looks like this:

::

    git clone https://github.com/iandennismiller/gthnk.git
    cd gthnk
    pip3 install --user ./src
    gthnk config

By default, gthnk uses ```/tmp/gthnk`` for data storage.
Configure gthnk with ``~/.config/gthnk/gthnk.conf``.

Next Steps
----------

Now check out :doc:`/user/using-the-journal` to learn techniques for actually getting stuff done with **Gthnk**.
