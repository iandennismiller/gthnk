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


from gthnk.__meta__ import __version__


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
    config["do_install"](config)


@cli.command('uninstall', short_help='remove Gthnk installation')
def do_uninstall():
    config = make_config()
    config["do_uninstall"](config)


def make_config():
    sys.path.insert(0, '.')
    from gthnk.integration.osx import install_osx, uninstall_osx
    from gthnk.integration.windows import install_windows, uninstall_windows

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


if __name__ == '__main__':
    cli()
