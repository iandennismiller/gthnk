# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import subprocess
from six.moves import input
from getpass import getpass

from . import md, render, rm


def create_database(config):
    db_filename = os.path.join(config["app_data"], "Gthnk", "gthnk.db")
    conf_filename = os.path.join(config["app_data"], "Gthnk", "gthnk.conf")
    venv_path = os.environ["VIRTUAL_ENV"]
    python_path = os.path.join(venv_path, "Scripts", "python.exe")
    manage_path = os.path.join(venv_path, "Scripts", "manage.py")

    if not os.path.isfile(db_filename):
        print("create:\tdb\t{0}".format(db_filename))
        os.environ["SETTINGS"] = conf_filename
        res = subprocess.check_output([python_path, manage_path, "db", "upgrade"])
        if not res:
            res = "OK"
        print("result:\t{0}".format(res))

        username = input("Choose a username for accessing Gthnk: ")
        password = getpass("Choose a password:")
        res = subprocess.check_output([python_path, manage_path, "user_add",
            "-e", username, "-p", password])
        if not res:
            res = "OK"
        print("result:\t{0}".format(res))
    else:
        print("exists:\t{0}".format(db_filename))


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

    create_database(config)


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
