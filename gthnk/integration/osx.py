# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os

from . import launchd, md, render


def osx_paths(config):

    md(os.path.join(config["home_directory"], "Library", "Gthnk"))
    md(os.path.join(config["home_directory"], "Library", "Gthnk", "backup"))
    md(os.path.join(config["home_directory"], "Library", "Gthnk", "export"))


def osx_files(config):

    render(config, 'osx/gthnk.conf.j2',
        os.path.join(config['home_directory'], "Library", "Gthnk", "gthnk.conf"))
    render(config, 'osx/com.gthnk.dashboard.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents",
            "com.gthnk.dashboard.plist"))
    render(config, 'osx/com.gthnk.server.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents",
            "com.gthnk.server.plist"))
    render(config, 'osx/com.gthnk.librarian.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents",
            "com.gthnk.librarian.plist"))


def osx_launchd(config):
    # stop any server process
    launchd("stop", "com.gthnk.server")

    # unload any existing launch agents
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.dashboard.plist"))
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.librarian.plist"))
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.server.plist"))

    # load the launch agents
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.dashboard.plist"))
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.librarian.plist"))
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.server.plist"))

    # start the server process
    launchd("start", "com.gthnk.server")


def osx_database(config):
    filename = os.path.join(config["home_directory"], "Library", "Gthnk", "gthnk.db")
    if not os.path.isfile(filename):
        # pushd ${VIRTUAL_ENV}/share
        # SETTINGS=$HOME/Library/Gthnk/gthnk.conf manage.py db upgrade

        # if migration:
        #     # create database using migrations
        #     print("applying migration")
        #     upgrade()
        # else:
        #     # create database from model schema directly
        #     db.create_all()
        #     db.session.commit()
        #     cfg = alembic.config.Config("gthnk/migrations/alembic.ini")
        #     alembic.command.stamp(cfg, "head")
        # # Role.add_default_roles()

        # """
        # echo "Create a User Account"
        # SETTINGS=$HOME/Library/Gthnk/gthnk.conf manage.py useradd -e ${email} -p ${password} \
        # && echo "OK"
        # """

        # if admin:
        #     roles = ["Admin"]
        # else:
        #     roles = ["User"]
        # User.register(
        #     email=email,
        #     password=password,
        #     confirmed=True,
        #     roles=roles
        # )

        pass
    else:
        print("exists:\t{0}".format(filename))


def install_osx(config):
    print("Performing install on UNIX")
    osx_paths(config)
    osx_files(config)
    osx_database(config)
    osx_launchd(config)
    print("OK")


def uninstall_osx(config):
    print("Performing uninstall on OSX")
