import os

import click
from trogon import tui # type: ignore

from . import Gthnk
from .model.journal import Journal
from .filetree.buffer import FileBuffer


@tui()
@click.group()
def cli():
    pass

@cli.command()
@click.option('--current', is_flag=True, default=False, help="Print the current configuration")
@click.argument('gthnk_path', default="/tmp/gthnk", required=False)
def config(gthnk_path:str, current:bool):
    "Generate a sample config file or view current configuration"
    if current:
        g = Gthnk()
        with open(g.config_filename, 'r') as f:
            buf = f.read()
    else:
        secret_key = str(os.urandom(24))
        buf = config_template.format(
            gthnk_path=gthnk_path,
            secret_key=secret_key,
        )
    print(buf)

@cli.command()
def path():
    "Display the path of the journal filetree"
    print(Gthnk().filetree.path)

@cli.command()
def rotate():
    "Import file buffers and rotate them"
    Gthnk().rotate_buffers()

@cli.command()
def buffer():
    "Display the contents of the file buffers"
    g = Gthnk()
    j = Journal(gthnk=g)
    # parse and accumulate into a blank journal
    for buffer in g.buffers:
        FileBuffer(buffer, journal=j).read()
    print(j)

@cli.command()
@click.argument('filename')
def read(filename:str):
    "Import a properly-formatted text file into the journal"
    g = Gthnk()
    FileBuffer(filename, journal=g.journal).read()
    g.filetree.write_journal()
    print(f"Journal contains {len(g.journal)} entries")

@cli.command()
@click.option('--date', is_flag=True, default=False, help="Print only the date, not the entry")
@click.option('--previous', is_flag=True, default=False, help="Retrieve the day before the id provided")
@click.option('--next', is_flag=True, default=False, help="Retrieve the day after the id provided")
@click.option('--latest', is_flag=True, default=False, help="Retrieve the latest day")
@click.option('--uri', is_flag=True, default=False, help="URI of the day")
@click.argument('datestamp', default=None, required=False)
def day(date:bool, previous:bool, next:bool, latest:bool, uri:bool, datestamp:str):
    "Retrieve a day from the journal by id (YYYY-MM-DD)"
    g = Gthnk()

    if datestamp is None:
        if latest:
            datestamp = g.journal.get_latest_datestamp()
        else:
            print("Please provide a day id")
            return
    
    day = g.journal.get_day(datestamp)
    if len(day.entries) == 0:
        print("Day not found")
        return
    
    if previous:
        day = g.journal.get_previous_day(day)
    elif next:
        day = g.journal.get_next_day(day)
    
    if date:
        print(day.datestamp)
    elif uri:
        print(day.uri)
    else:
        print(day)

@cli.command()
@click.option('--date', is_flag=True, default=False, help="Print only the date")
@click.option('--uri', is_flag=True, default=False, help="Print only the uri")
@click.option('--path', is_flag=True, default=False, help="Print the full file path")
@click.option('--reverse', is_flag=True, default=False, help="Reverse the order of the entries")
@click.option('--count', is_flag=True, default=False, help="Print the number of entries that matched")
@click.option('--num', default=None, help="Number of entries to return")
@click.argument('query', nargs=-1)
def search(date:bool, uri:bool, path:bool, count:bool, num:int, reverse:bool, query:str):
    "Search the journal for a query"
    g = Gthnk()

    query_str = " ".join(query)
    if not query_str:
        print("Please provide a query")
        return

    if num:
        num = int(num)

    if count:
        print(len(list(g.journal.search(query_str))))
        return

    if uri and path:
        print("Cannot provide both --uri and --path at the same time")
        return

    counter = 0
    for entry in g.journal.search(query_str, chronological=reverse):
        counter += 1
        if date and uri:
            print(entry.day.uri)
        elif date and path:
            print(f"{g.filetree.path}/day{entry.day.uri}")
        elif date:
            print(entry.day.datestamp)
        elif uri:
            print(entry.uri)
        elif path:
            print(f"{g.filetree.path}/entry{entry.uri}")
        else:
            print(entry.render_standalone())
        if num and counter >= num:
            break


config_template = """\
# Gthnk Configuration
FILETREE_ROOT = "{gthnk_path}"
INPUT_FILES = "{gthnk_path}/journal.txt"
LOG_FILENAME = "{gthnk_path}/gthnk.log"
LOG_LEVEL = "INFO"
SECRET_KEY = {secret_key}
BASE_URL = "http://gthnk.lan"
"""
