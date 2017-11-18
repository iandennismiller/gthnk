#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import sys

import click
import os
import warnings

from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)

sys.path.insert(0, '.')
from gthnk.__meta__ import __version__
from gthnk.integration.osx import install_osx, uninstall_osx
from gthnk.integration.windows import install_windows, uninstall_windows

r"""
integration.py.

Manage the integration of Gthnk into various operating systems.

Windows invocation:
    workon gthnk
    python %virtual_env%\Scripts\integration.py

UNIX invocation:
    workon gthnk
    integration.py
"""


@click.group()
@click.version_option(__version__)
def cli():
    "Gthnk Integration."


@cli.command('install', short_help='integrate Gthnk with the operating system')
def do_install():
    if os.name == 'nt':
        install_windows()
    else:
        install_osx()


@cli.command('uninstall', short_help='remove Gthnk installation')
def do_uninstall():
    if os.name == 'nt':
        uninstall_windows()
    else:
        uninstall_osx()

if __name__ == '__main__':
    cli()
