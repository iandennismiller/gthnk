# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from jinja2 import Environment, PackageLoader
from os.path import expanduser
import os
import string
import random
import subprocess

def osx_paths(config):
    # create directories
    def md(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("created:\t{0}".format(directory))
        else:
            print("exists:\t{0}".format(directory))

    md(os.path.join(config["home_directory"], "Library", "Gthnk"))
    md(os.path.join(config["home_directory"], "Library", "Gthnk", "backup"))
    md(os.path.join(config["home_directory"], "Library", "Gthnk", "export"))

def osx_files(config):
    # render templates as files
    env = Environment(
        loader=PackageLoader('gthnk.integration', 'osx')
    )

    def render(src, dst):
        if not os.path.isfile(dst):
            with open(dst, "w") as f:
                template = env.get_template(src)
                f.write(template.render(**config))
                print("created:\t{0}".format(dst))
        else:
            print("exists:\t{0}".format(dst))

    render('gthnk.conf.j2',
        os.path.join(config['home_directory'], "Library", "Gthnk", "gthnk.conf"))
    render('com.gthnk.dashboard.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.dashboard.plist"))
    render('com.gthnk.server.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.server.plist"))
    render('com.gthnk.librarian.plist.j2',
        os.path.join(config['home_directory'], "Library", "LaunchAgents", "com.gthnk.librarian.plist"))

def osx_launchd(config):
    def launchd(cmd, target):
        print("exec:\tlaunchctl {0} {1}".format(cmd, target))
        res = subprocess.check_output([ "/bin/launchctl", cmd, target ])
        if not res:
            res = "OK"
        print("result:\t{0}".format(res))

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

        """
        echo "Create a User Account"
        echo -n "username: "
        read email
        echo -n "password: "
        read -s password
        echo
        echo "Creating..."
        SETTINGS=$HOME/Library/Gthnk/gthnk.conf manage.py useradd -e ${email} -p ${password} && echo "OK"
        unset email
        unset password
        """

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

def install_windows():
    print("Performing install on Windows")

def uninstall_windows():
    print("Performing uninstall on Windows")

