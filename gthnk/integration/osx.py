# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from jinja2 import Environment, PackageLoader
from os.path import expanduser
import os
import string
import random
import subprocess
from . import md, launchd, render


def osx_paths(config):

    md(os.path.join(config["home_directory"], "Library", "Gthnk"))
    md(os.path.join(config["home_directory"], "Library", "Gthnk", "backup"))
    md(os.path.join(config["home_directory"], "Library", "Gthnk", "export"))


def osx_files(config):

    render('osx/gthnk.conf.j2',
        os.path.join(config['home_directory'], "Library", "Gthnk", "gthnk.conf"))
    render('osx/com.gthnk.dashboard.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.dashboard.plist"))
    render('osx/com.gthnk.server.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.server.plist"))
    render('osx/com.gthnk.librarian.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.librarian.plist"))


def osx_launchd(config):
    # stop any server process
    launchd("stop", "com.gthnk.server")

    # unload any existing launch agents
    launchd("unload",os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.dashboard.plist"))
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.librarian.plist"))
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.server.plist"))

    # load the launch agents
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.dashboard.plist"))
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.librarian.plist"))
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.server.plist"))

    # start the server process
    launchd("start", "com.gthnk.server")


def osx_database(config):
    filename = os.path.join(config["home_directory"], "Library", "Gthnk", "gthnk.db")
    if not os.path.isfile(filename):
        # pushd ${VIRTUAL_ENV}/share
        # SETTINGS=$HOME/Library/Gthnk/gthnk.conf manage.py db upgrade

        if migration:
            # create database using migrations
            print("applying migration")
            upgrade()
        else:
            # create database from model schema directly
            db.create_all()
            db.session.commit()
            cfg = alembic.config.Config("gthnk/migrations/alembic.ini")
            alembic.command.stamp(cfg, "head")
        # Role.add_default_roles()

        """
        echo "Create a User Account"
        SETTINGS=$HOME/Library/Gthnk/gthnk.conf manage.py useradd -e ${email} -p ${password} && echo "OK"
        """

        if admin:
            roles = ["Admin"]
        else:
            roles = ["User"]
        User.register(
            email=email,
            password=password,
            confirmed=True,
            roles=roles
        )

        pass
    else:
        print("exists:\t{0}".format(filename))


def install_osx():
    print("Performing install on UNIX")

    # variables for installation
    chars = string.ascii_letters + string.digits + '^!$&=?+~#-_.:,;'
    home_directory = expanduser("~")
    config = {
        'secret_key': repr(os.urandom(24)),
        'hash_salt': "".join([random.choice(chars) for _ in range(24)]),
        'home_directory': home_directory,
    }

    osx_paths(config)
    osx_files(config)
    osx_database(config)
    osx_launchd(config)
    print("OK")


def uninstall_osx():
    print("Performing uninstall on OSX")
