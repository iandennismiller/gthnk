# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os

from . import launchd, md, render, create_db, rm


def osx_paths(config):

    md(os.path.join(config["home_directory"], "Library", "Gthnk"))
    md(os.path.join(config["home_directory"], "Library", "Gthnk", "backup"))
    md(os.path.join(config["home_directory"], "Library", "Gthnk", "export"))


def osx_files(config):

    render(config, 'osx/gthnk.conf.j2',
        os.path.join(config['home_directory'], "Library", "Gthnk", "gthnk.conf"))
    render(config, 'osx/com.gthnk.review.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents",
            "com.gthnk.review.plist"))
    render(config, 'osx/com.gthnk.server.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents",
            "com.gthnk.server.plist"))
    render(config, 'osx/com.gthnk.rotate.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents",
            "com.gthnk.rotate.plist"))


def osx_launchd(config):
    # stop any server process
    launchd("stop", "com.gthnk.server")

    # unload any existing launch agents
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.review.plist"))
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.rotate.plist"))
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.server.plist"))

    # load the launch agents
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.review.plist"))
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.rotate.plist"))
    launchd("load", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.server.plist"))

    # start the server process
    launchd("start", "com.gthnk.server")


def osx_database(config):
    db_filename = os.path.join(config["home_directory"], "Library", "Gthnk", "gthnk.db")
    conf_filename = os.path.join(config["home_directory"], "Library", "Gthnk", "gthnk.conf")
    venv_path = os.environ["VIRTUAL_ENV"]
    python_path = os.path.join(venv_path, "bin", "python")
    manage_path = os.path.join(venv_path, "bin", "manage.py")
    create_db(db_filename, conf_filename, python_path, manage_path)


def install_osx(config):
    print("Performing install on UNIX")
    osx_paths(config)
    osx_files(config)
    osx_database(config)
    osx_launchd(config)
    print("OK")


def uninstall_osx(config):
    print("Performing uninstall on OSX")

    # Stopping any existing gthnk server processes
    launchd("stop", "com.gthnk.server")

    # unload any existing launch agents
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.review.plist"))
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.rotate.plist"))
    launchd("unload", os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.server.plist"))

    rm(os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.server.plist"))
    rm(os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.rotate.plist"))
    rm(os.path.join(config['home_directory'], "Library", "LaunchAgents",
        "com.gthnk.review.plist"))

    # remove gthnk.conf
    # rm(os.path.join(config['home_directory'], "Library", "Gthnk", "gthnk.com"))
