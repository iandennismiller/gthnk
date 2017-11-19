# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import subprocess

from . import md, render, rm


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


def schedule(name, filename, when):
    # https://technet.microsoft.com/en-us/library/cc725744.aspx
    # It also uses the /it parameter to specify that the task runs only when the user under whose
    # account the task runs is logged onto the computer
    try:
        res = subprocess.check_output(['schtasks', "/query", "/v", "/fo", "list", "/tn", name])
        print("skip:\tschedule\t{0}".format(name))
    except subprocess.CalledProcessError:
        print("exec:\tschedule\t{0}".format(name))
        res = subprocess.check_output(['C:\Windows\System32\schtasks.exe', "/create", "/tn", name,
            "/tr", filename, '/sc', 'daily', '/st', '00:03', '/it'])
        if not res:
            res = "OK"
        print("result:\t{0}".format(res))


def unschedule(name):
    try:
        res = subprocess.check_output(['schtasks', "/query", "/v", "/fo", "list", "/tn", name])
        print("exec:\tschtasks.exe\t{0}".format(name))
        res = subprocess.check_output(['C:\Windows\System32\schtasks.exe', "/delete", "/f", "/tn",
            name])
        if not res:
            res = "OK"
        print("result:\t{0}".format(res))
    except subprocess.CalledProcessError:
        print("skip:\tunschedule\t{0}".format(name))


def install_windows(config):
    print("Performing install on Windows")

    # create folders
    md(os.path.join(config['app_data'], "Gthnk"))
    md(os.path.join(config['app_data'], "Gthnk", "backup"))
    md(os.path.join(config['app_data'], "Gthnk", "export"))

    # create files
    render(config, 'windows/gthnk.conf.j2',
        os.path.join(config['app_data'], "Gthnk", "gthnk.conf"))
    render(config, 'windows/startup.bat.j2',
        os.path.join(config['home_directory'], "Start Menu", "Programs",
            "Startup", "gthnk-startup.bat"))

    # schedule daily journal rotation task
    filename = os.path.join(config['home_directory'], "Envs", "Gthnk", "Scripts",
        "gthnk-rotate.cmd")
    schedule("Gthnk Rotate", filename, '00:03')

    # schedule daily review task
    filename = os.path.join(config['home_directory'], "Envs", "Gthnk", "Scripts",
        "gthnk.cmd")
    schedule("Gthnk Review", filename, '09:00')

    # create_database(config)


def uninstall_windows(config):
    print("Performing uninstall on Windows")

    # remove startup.bat
    rm(os.path.join(config['home_directory'], "Start Menu", "Programs",
        "Startup", "gthnk-startup.bat"))

    # remove gthnk.conf
    rm(os.path.join(config['app_data'], "Gthnk", "gthnk.conf"))

    # remove Gthnk Review
    unschedule("Gthnk Review")

    # remove Gthnk Rotate
    unschedule("Gthnk Rotate")
