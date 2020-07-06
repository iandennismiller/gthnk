import sys
import os

def env_vscode():
    "prepare environment so tests can be detected by vscode"
    cwd = os.getcwd()
    os.environ["SETTINGS"] = os.path.join(cwd, "usr/conf/testing.conf")
    sys.path.insert(0, "src")
