#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import sys

import click
import os
import random
import string
import warnings

from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)

sys.path.insert(0, '.')
from gthnk.__meta__ import __version__
from gthnk.integration.osx import install_osx, uninstall_osx
from gthnk.integration.windows import install_windows, uninstall_windows


def make_config():
    # variables for installation
    chars = string.ascii_letters + string.digits + '^!$&=?+~#-_.:,;'

    if os.name == 'nt':
        config = {
            'secret_key': repr(os.urandom(24)),
            'hash_salt': "".join([random.choice(chars) for _ in range(24)]),
            'home_directory': os.environ["USERPROFILE"],
            "app_data": os.environ["APPDATA"],
            'do_install': install_windows,
            'do_ininstall': uninstall_windows,
        }
    else:
        config = {
            'secret_key': repr(os.urandom(24)),
            'hash_salt': "".join([random.choice(chars) for _ in range(24)]),
            'home_directory': os.path.expanduser("~"),
            'do_install': install_osx,
            'do_ininstall': uninstall_osx,
        }

    return(config)


@click.group()
@click.version_option(__version__)
def cli():
    r"""
    Gthnk integration.

    Manage the integration of Gthnk into various operating systems.

    Windows invocation:
        workon gthnk
        python %virtual_env%\Scripts\integration.py

    UNIX invocation:
        workon gthnk
        integration.py
    """


@cli.command('install', short_help='integrate Gthnk with the operating system')
def do_install():
    config = make_config()
    config.do_install()


@cli.command('uninstall', short_help='remove Gthnk installation')
def do_uninstall():
    config = make_config()
    config.do_uninstall()

if __name__ == '__main__':
    cli()
