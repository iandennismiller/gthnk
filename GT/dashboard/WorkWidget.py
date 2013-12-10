# (c) 2013 Ian Dennis Miller
# -*- coding: utf-8 -*-

import os, sys, time, json
from stat import S_ISREG, ST_CTIME, ST_MODE
from GT.dashboard import DashboardWidget

def newest_file_in_tree(rootfolder):
    # http://stackoverflow.com/questions/837606/find-the-oldest-file-recursively-in-a-directory
    try:
        return max(
            (os.path.join(dirname, filename)
            for dirname, dirnames, filenames in os.walk(rootfolder)
            #for filename in filenames if not filename[0] == '.'),
            for filename in dirnames if dirname[0] != '.' and filename[0] != "."),
            key=lambda fn: os.stat(fn).st_mtime)
    except (ValueError, OSError):
        return

def recently_modified(dirpath):
    # http://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python

    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((newest_file_in_tree(path), path) for path in entries)
    entries = ((os.stat(newest).st_mtime, newest, path) for (newest, path) in entries if newest)

    s_entries = sorted(entries)
    s_entries.reverse()

    files = list((time.ctime(cdate), os.path.basename(path)) for cdate, newest, path in s_entries)
    return files

class WorkWidget(DashboardWidget):
    def render(self):
        dirpath = sys.argv[1] if len(sys.argv) == 2 else r'.'
        files = recently_modified(dirpath)
        return json.dumps(files, indent=4)
