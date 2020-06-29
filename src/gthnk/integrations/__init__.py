# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import random
import string
import subprocess
from six.moves import input
from getpass import getpass

from jinja2 import Environment, PackageLoader


# render templates as files
env = Environment(
    loader=PackageLoader('gthnk.integration', 'templates')
)


# create directories
def md(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("created:\t{0}".format(directory))
    else:
        print("exists:\t{0}".format(directory))


def launchd(cmd, target):
    print("exec:\tlaunchctl {0} {1}".format(cmd, target))
    res = subprocess.check_output(["/bin/launchctl", cmd, target])
    if not res:
        res = "OK"
    print("result:\t{0}".format(res))


def render(config, src, dst):
    if not os.path.isfile(dst):
        with open(dst, "w") as f:
            template = env.get_template(src)
            f.write(template.render(**config))
            print("created:\t{0}".format(dst))
    else:
        print("exists:\t{0}".format(dst))


def rm(target):
    if target and os.path.isfile(target):
        # delete that file
        os.remove(target)
    else:
        print("gone:\t{0}".format(target))


def create_db(db_filename, conf_filename, python_path, manage_path):
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


def make_config():
    from .osx import install_osx, uninstall_osx
    from .windows import install_windows, uninstall_windows

    chars = string.ascii_letters + string.digits + '^!$&=?+~#-_.:,;'

    if os.name == 'nt':
        config = {
            'secret_key': repr(os.urandom(24)),
            'hash_salt': "".join([random.choice(chars) for _ in range(24)]),
            'home_directory': os.environ["USERPROFILE"],
            "app_data": os.environ["APPDATA"],
            'do_install': install_windows,
            'do_uninstall': uninstall_windows,
        }
    else:
        config = {
            'secret_key': repr(os.urandom(24)),
            'hash_salt': "".join([random.choice(chars) for _ in range(24)]),
            'home_directory': os.path.expanduser("~"),
            'do_install': install_osx,
            'do_uninstall': uninstall_osx,
        }

    return(config)
