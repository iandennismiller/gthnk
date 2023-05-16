import os
import sys
import hashlib
import logging
from rich.logging import RichHandler
from rich.console import Console


def overwrite_if_different(filename, new_content):
    "Check whether the new_content is different from the existing file."

    # see whether the file exists
    if os.path.isfile(filename):
        # if so, gather the md5 checksums
        with open(filename, "r", encoding='utf-8') as f:
            existing_checksum = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        generated_checksum = hashlib.md5(new_content.encode('utf-8')).hexdigest()

        # compare to md5 checksum of generated file.
        # if different, then overwrite.
        if generated_checksum == existing_checksum:
            return False

    with open(filename, "wb") as f:
        f.write(new_content.encode('utf-8'))
    return True


def overwrite_if_different_bytes(filename, new_content):
    # see whether the file exists
    if os.path.isfile(filename):
        # if so, gather the md5 checksums
        with open(filename, "rb") as f:
            existing_checksum = hashlib.md5(f.read()).hexdigest()
        generated_checksum = hashlib.md5(new_content).hexdigest()

        # compare to md5 checksum of generated file.
        # if different, then overwrite.
        if generated_checksum == existing_checksum:
            return False

    with open(filename, "wb") as f:
        f.write(new_content)
    return True


# create directories
def md(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info("created:\t{0}".format(directory))
    else:
        logging.info("exists:\t{0}".format(directory))


def merge_two_dicts(x, y):
    # go through both loops and make a smart merge
    z = y.copy()
    for day in x:
        for timestamp in x[day]:
            z[day][timestamp] += x[day][timestamp]
    return z


def split_filename_list(filename_str):
    """
    """
    return([x.strip() for x in filename_str.split(',')])


def init_logger(logger=None, name=None, filename=None, level=None):
    if logger is None and name is not None:
        logger = logging.getLogger(name)
    
    if logger is None:
        raise Exception("Either logger or name must be provided")

    # only the first invocation will configure this
    if not len(logger.handlers):
        if filename is None:
            name_snakecase = change_case(logger.name)
            filename = os.path.join("var", f"{name_snakecase}.log")

        if level is None:
            level = logging.getLevelName("WARNING")

        logger.setLevel(level)
        logger.propagate = False

        logfile = open(filename, 'a')
        monitor_format = logging.Formatter('%(message)s')
        stderr = Console(file=logfile, tab_size=2, width=130, force_terminal=True)
        handler = RichHandler(markup=True, console=stderr, show_path=True, show_time=True, show_level=True, rich_tracebacks=True)
        handler.setFormatter(monitor_format)
        logger.addHandler(handler)

        logger.info(f"Process {os.getpid()} (parent {os.getppid()}) logging to {filename} at level {level}")

    return logger


def change_case(str):     
    return ''.join(['_'+i.lower() if i.isupper()
               else i for i in str]).lstrip('_')
