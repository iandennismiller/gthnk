#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import sys
import traceback
sys.path.insert(0, '.')

import warnings
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)

"""
integration.py

Manage the integration of Gthnk into various operating systems.
"""

import click
import os
from gthnk.__meta__ import __version__
from gthnk.integration import install_windows, install_osx

@click.group()
@click.version_option(__version__)
def cli():
    "Gthnk Integration"

@cli.command('install', short_help='integrate Gthnk with the operating system')
def do_install():
    if os.name == 'nt':
        install_windows()
    else:
        install_osx()

@cli.command('uninstall', short_help='remove Gthnk installation')
def do_uninstall():
    pass

if __name__ == '__main__':
    cli()
