import os

import click
from trogon import tui

from . import Gthnk
from .model.journal import Journal
from .filetree.buffer import FileBuffer


@tui()
@click.group()
def cli():
    "Gthnk: a journaling tool"

@cli.command()
@click.option('--current', is_flag=True, default=False, help="Print the current configuration")
@click.argument('gthnk_path', default="/tmp/gthnk", required=False)
def config(gthnk_path:str, current:bool):
    "Generate a sample config file or view current configuration"
    if current:
        gthnk = Gthnk()
        with open(gthnk.config_filename, 'r', encoding="utf-8") as file_handle:
            buf = f"# Filename: {gthnk.config_filename}\n" + file_handle.read()
    else:
        secret_key = str(os.urandom(24))
        buf = CONFIG_TEMPLATE.format(
            gthnk_path=gthnk_path,
            secret_key=secret_key,
        )
    print(buf)

@cli.command(name="path")
def print_path():
    "Display the path of the journal filetree"
    print(Gthnk().filetree.path)

@cli.command()
def rotate():
    "Import file buffers and rotate them"
    Gthnk().rotate_buffers()

@cli.command()
def buffer():
    "Display the contents of the file buffers"
    gthnk = Gthnk()
    journal = Journal(gthnk=gthnk)
    # parse and accumulate into a blank journal
    for buffer_name in gthnk.buffers:
        FileBuffer(buffer_name, journal=journal).read()
    print(journal)

@cli.command()
@click.argument('filename')
def read(filename:str):
    "Import a properly-formatted text file into the journal"
    gthnk = Gthnk()
    FileBuffer(filename, journal=gthnk.journal).read()
    gthnk.filetree.write_journal()
    print(f"Journal contains {len(gthnk.journal)} entries")

@cli.command(name="day")
@click.option('--date', is_flag=True, default=False, help="Print only the date, not the entry")
@click.option('--previous',
    is_flag=True,
    default=False,
    help="Retrieve the day before the id provided"
)
@click.option('--next', is_flag=True, default=False, help="Retrieve the day after the id provided")
@click.option('--latest', is_flag=True, default=False, help="Retrieve the latest day")
@click.option('--uri', is_flag=True, default=False, help="URI of the day")
@click.argument('datestamp', default=None, required=False)
def print_day(date:bool, previous:bool, next:bool, latest:bool, uri:bool, datestamp:str): # pylint: disable=redefined-builtin
    "Retrieve a day from the journal by id (YYYY-MM-DD)"
    gthnk = Gthnk()

    if datestamp is None:
        if latest:
            datestamp = gthnk.journal.get_latest_datestamp()
        else:
            print("Please provide a day id")
            return

    day = gthnk.journal.get_day(datestamp)
    if len(day.entries) == 0:
        print("Day not found")
        return

    if previous:
        day = gthnk.journal.get_previous_day(day)
    elif next:
        day = gthnk.journal.get_next_day(day)

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
@click.option('--count',
    is_flag=True,
    default=False,
    help="Print the number of entries that matched"
)
@click.option('--num', default=None, help="Number of entries to return")
@click.argument('query', nargs=-1)
def search(date:bool, uri:bool, path:bool, count:bool, num:int, reverse:bool, query:str):
    "Search the journal for a query"
    gthnk = Gthnk()

    query_str = " ".join(query)
    if not query_str:
        print("Please provide a query")
        return

    if num:
        num = int(num)

    if count:
        print(len(list(gthnk.journal.search(query_str))))
        return

    if uri and path:
        print("Cannot provide both --uri and --path at the same time")
        return

    counter = 0
    for entry in gthnk.journal.search(query_str, chronological=reverse):
        counter += 1
        if date and uri:
            print(entry.day.uri)
        elif date and path:
            print(f"{gthnk.filetree.path}/day{entry.day.uri}")
        elif date:
            print(entry.day.datestamp)
        elif uri:
            print(entry.uri)
        elif path:
            print(f"{gthnk.filetree.path}/entry{entry.uri}")
        else:
            print(entry)
        if num and counter >= num:
            break


CONFIG_TEMPLATE = """\
# Gthnk Configuration
FILETREE_ROOT = "{gthnk_path}"
INPUT_FILES = "{gthnk_path}/journal.txt"
LOG_FILENAME = "{gthnk_path}/gthnk.log"
LOG_LEVEL = "INFO"
SECRET_KEY = {secret_key}
BASE_URL = "http://gthnk.lan"
"""
