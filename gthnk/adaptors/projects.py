# -*- coding: utf-8 -*-
# gthnk (c) 2014-2016 Ian Dennis Miller

import os
import time
import subprocess
import flask


def pipe(cmd):
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = sp.stdout.read()
    sp.stdout.close()
    sp.wait()
    return output


def recently_modified_git(dirpath):
    cmd = "find %s -name '.git' -depth 2" % dirpath
    output = pipe(cmd).strip()
    entries = output.split("\n")
    timestamped = ((os.stat(fname).st_mtime, fname) for fname in entries)
    s_entries = sorted(timestamped)
    s_entries.reverse()

    files = list(
        (time.ctime(cdate), os.path.basename(os.path.dirname(path))) for cdate, path in s_entries
    )
    return files


class ProjectList(object):
    def __init__(self):
        pass

    def get_recent(self):
        files = recently_modified_git(flask.current_app.config["PROJECT_PATH"])
        return files[:20]

    def get_readme(self, project_name):
        target_file = os.path.join(
            flask.current_app.config["PROJECT_PATH"], project_name, "Readme.md"
        )
        if os.path.exists(target_file):
            with open(target_file, "r") as f:
                buf = f.read()
        else:
            buf = "# Empty Readme"
        return buf
