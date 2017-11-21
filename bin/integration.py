#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import sys
import click
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
    sys.path.insert(0, '.')
    from gthnk.integration import make_config
    config = make_config()
    config["do_install"](config)


@cli.command('uninstall', short_help='remove Gthnk installation')
def do_uninstall():
    sys.path.insert(0, '.')
    from gthnk.integration import make_config
    config = make_config()
    config["do_uninstall"](config)


if __name__ == '__main__':
    cli()
