# (c) 2013 Ian Dennis Miller
# -*- coding: utf-8 -*-

import os, sys, time, json
from stat import S_ISREG, ST_CTIME, ST_MODE
from GT.dashboard import DashboardWidget
import subprocess

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

    files = list((time.ctime(cdate), os.path.basename(os.path.dirname(path))) for cdate, path in s_entries)
    return files

class WorkWidget(DashboardWidget):
    def render(self):
        dirpath = "/Users/idm/Work"
        files = recently_modified_git(dirpath)
        return files[:20]
