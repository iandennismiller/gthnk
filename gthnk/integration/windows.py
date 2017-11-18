# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import random
import string

from . import md, render


def create_database(config):
    filename = os.path.join(config["app_data"], "Gthnk", "gthnk.db")
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
        # SETTINGS=$HOME/Library/Gthnk/gthnk.conf manage.py useradd -e ${email}
        #     -p ${password} && echo "OK"
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


def install_windows():
    print("Performing install on Windows")

    # variables for installation
    chars = string.ascii_letters + string.digits + '^!$&=?+~#-_.:,;'
    config = {
        'secret_key': repr(os.urandom(24)),
        'hash_salt': "".join([random.choice(chars) for _ in range(24)]),
        'home_directory': os.environ["USERPROFILE"],
        "app_data": os.environ["APPDATA"],
    }

    # create folders
    md(os.path.join(config['app_data'], "Gthnk"))

    # create files
    render(config, 'windows/gthnk.conf.j2',
        os.path.join(config['app_data'], "Gthnk", "gthnk.conf"))
    render(config, 'windows/startup.bat.j2',
        os.path.join(config['home_directory'], "Start Menu", "Programs",
            "Startup", "gthnk-startup.bat"))

    # schedule daily journal rotation task
    # https://technet.microsoft.com/en-us/library/cc725744.aspx
    # schtasks.exe
    # schtasks /create /tn "My App" /tr c:\apps\myapp.exe /sc daily /st 08:00 /ed 31/12/2002
    # It also uses the /it parameter to specify that the task runs only when the user under whose
    # account the task runs is logged onto the computer

    # schedule daily review task
    # start "" "http://localhost:1621"

    # create_database(config)


def uninstall_windows():
    print("Performing uninstall on Windows")

    # remove startup.bat

    # remove gthnk.conf

    # leave APPDATA/Gthnk for the database
