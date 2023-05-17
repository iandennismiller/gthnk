# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import logging
import subprocess

from jinja2 import Environment, PackageLoader


# render templates as files
env = Environment(
    loader=PackageLoader('gthnk_integration', 'templates')
)


def launchd(cmd, target):
    logging.info("exec:\tlaunchctl {0} {1}".format(cmd, target))
    res = subprocess.check_output(["/bin/launchctl", cmd, target])
    if not res:
        res = "OK"
    logging.info("result:\t{0}".format(res))


def render(config, src, dst):
    if not os.path.isfile(dst):
        with open(dst, "w") as f:
            template = env.get_template(src)
            f.write(template.render(**config))
            logging.info("created:\t{0}".format(dst))
    else:
        logging.info("exists:\t{0}".format(dst))


def rm(target):
    if target and os.path.isfile(target):
        # delete that file
        os.remove(target)
    else:
        logging.info("gone:\t{0}".format(target))


# def create_db(db_filename, conf_filename, python_path, manage_path):
#     if not os.path.isfile(db_filename):
#         logging.info("create:\tdb\t{0}".format(db_filename))
#         os.environ["SETTINGS"] = conf_filename
#         res = subprocess.check_output([python_path, manage_path, "db", "upgrade"])
#         if not res:
#             res = "OK"
#         logging.info("result:\t{0}".format(res))

#         username = input("Choose a username for accessing Gthnk: ")
#         password = getpass("Choose a password:")
#         res = subprocess.check_output([python_path, manage_path, "user_add",
#             "-e", username, "-p", password])
#         if not res:
#             res = "OK"
#         logging.info("result:\t{0}".format(res))
#     else:
#         logging.info("exists:\t{0}".format(db_filename))
