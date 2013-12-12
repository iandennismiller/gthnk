#!/usr/bin/env python

from GT import app
import GT.journal
import datetime, os

app.logger.debug("START")

now = datetime.datetime.utcnow()
datestamp = "%s-%s-%s" % (now.year, now.month, now.day)

# set up filenames

journal_path = "/Users/idm/Library/Journal"
backup_path = os.path.join(journal_path, "backup")
export_path = os.path.join(journal_path, "auto")
dropbox_path = "/Users/idm/Dropbox/journal"

http_file = os.path.join(journal_path, 'http/latest.txt')
live_file = os.path.join(journal_path, 'journal.txt')
dropbox_file = os.path.join(dropbox_path, 'journal.txt')

# create backups

os.system("cp %s %s/%s-journal.txt" % (live_file, backup_path, datestamp))
os.system("cp %s %s/%s-dropbox.txt" % (dropbox_file, backup_path, datestamp))

# download HTTP and purge/rotate

app.logger.debug("start web clipboard download")
os.system("/Users/idm/.virtualenvs/greenthink/bin/journal_get.sh")
app.logger.debug("finish web clipboard download")
os.system("/Users/idm/.virtualenvs/greenthink/bin/journal_delete.sh")
app.logger.debug("clear web clipboard")

# now deal with the local journal

app.logger.debug("start rotating journal")

j = GT.journal.Journal(export_path)
j.parse(live_file)
j.parse(http_file)
j.parse(dropbox_file)

exported = j.export_week_old()
if exported:
    j.purge_week_old(live_file)

app.logger.debug("finish rotating journal")

# rotate out Dropbox file

app.logger.debug("clear dropbox journal.txt")
os.system("echo '' > %s" % dropbox_file)

app.logger.debug("DONE")
