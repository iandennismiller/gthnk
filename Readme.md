# greenthink-library (c) 2013 Ian Dennis Miller

# Greenthink

So greenthink is actually a few things.  First, it is a self-actualization project.  Next, it is a technology that, through gthnk.com, enables others to self-actualize, themselves.

For my part, I need to do a few things before I can consider my stuff to be totally organized and whatnot.  I think, though, that a few of my big projects are going to be reflected in greenthink.  For example: the way in which ~/Work projects are listed in the life dashboard is a big way I can reflect on recently completed work.

It's possible there is a difference between what happens in ~/Work/skel and what happens elsewhere.  I may want to track my templates separately.  Maybe not.  I don't know.  It's working as it is.

Anyway, here are some notes about things I need to do to get all this working:

- split idm-global into idm-home and idm-bin
- gitlab provides interface into hosted repositories
- review ~/Work: prune unused projects, ensure they are in repo, create any useful templates
- greenthink-search or whatever needs to be a full-time daemon running locally

Part of the trick with idm-bin is that it will contain code for managing the repos.  Between new-repo, list-repos, and get-repo, I have everything I need to make projects and manage them.  However, I don't yet have a way to manage the management scripts...  and idm-global isn't good enough.

# default screen

The default screen of the greenthink webapp is the "focus" view.

The new greenthink may as well use the flask-admin interface to organize the different tabs.

They will load on-demand as separate tabs.  The "recent projects" tab can cache for 24 hours, and a cron job will ping the cache every 6 hours to ensure it is fresh.  This way, any time a human (e.g. myself) hits the "recent projects" tab, it won't take forever to load.  Also, I will streamline the datestamping process further...  something is still screwy with it.

# administration

- Makefile: direct action in the working directory, executes locally
- manage.py: application administrative tasks, including databases
- fabfile.py: coordinates deployment, actions execute remotely

# Makefile

## to install

    make install

## to launch an interactive session

    make shell

## to start the dev server locally

    make server

## to test the package locally

    make test

## to watch files for changes and repeatedly re-run tests

    make watch

## to generate documentation

    make doc

## to create and deploy a migration

    export SETTINGS=../etc/dev.conf
    bin/manage.py db migrate -m "description of changes"
    bin/manage.py db upgrade

# fabfile

## to deploy to example.com

fab -H example.com rsync setup

# TODO
