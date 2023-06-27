import os
import logging
from rich.logging import RichHandler
from rich.console import Console


def init_logger(logger=None, name=None, filename=None, level=None):
    "Initialize a logger with a RichHandler."

    if logger is None and name is not None:
        logger = logging.getLogger(name)

    if logger is None:
        raise ValueError("Either logger or name must be provided")

    # only the first invocation will configure this
    if not logger.handlers:
        if filename is None:
            name_snakecase = change_case(logger.name)
            filename = os.path.join("/tmp", f"{name_snakecase}.log")

        if level is None:
            level = logging.getLevelName("WARNING")

        logger.setLevel(level)
        logger.propagate = False

        logfile = open(filename, 'a', encoding="utf-8") # pylint: disable=consider-using-with
        monitor_format = logging.Formatter('%(message)s')
        stderr = Console(
            file=logfile,
            tab_size=2,
            width=100,
            force_terminal=True
        )
        handler = RichHandler(
            markup=True,
            console=stderr,
            show_path=True,
            show_time=True,
            show_level=True,
            rich_tracebacks=True
        )
        handler.setFormatter(monitor_format)
        logger.addHandler(handler)

        logger.info(
            "Process %d (parent %d) logging to %s at level %s",
            os.getpid(),
            os.getppid(),
            filename,
            level
        )

    return logger

def change_case(input_string):
    "Convert a string to snake_case"
    return ''.join(['_'+i.lower() if i.isupper()
               else i for i in input_string]).lstrip('_')
