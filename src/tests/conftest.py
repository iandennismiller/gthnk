import pytest
import shutil

from gthnk.model.journal import Journal
from gthnk.filetree import FileTree
from gthnk import Gthnk


@pytest.fixture()
def clean_path():
    shutil.rmtree("/tmp/gthnk", ignore_errors=True, onerror=None)

@pytest.fixture()
def config_tmp():
    return {
        "INPUT_FILES": "/tmp/gthnk/journal.txt",
        "BACKEND": "filetree",
        "FILETREE_ROOT": "/tmp/gthnk",
        "LOG_FILENAME": "/tmp/gthnk-test.log",
        "LOG_LEVEL": "INFO",
    }

@pytest.fixture()
def gthnk(clean_path, config_tmp):
    return Gthnk(config=config_tmp)

@pytest.fixture()
def journal(gthnk):
    return gthnk.journal

@pytest.fixture()
def filetree(gthnk):
    return FileTree(journal=gthnk.journal)

@pytest.fixture()
def cwd():
    import pathlib
    return(pathlib.Path(__file__).parent.absolute())
