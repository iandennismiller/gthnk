#!/usr/bin/env python

from GT import app
import GT.journal
import datetime, os

app.logger.debug("start clipboard download")
os.system("/Users/idm/.virtualenvs/greenthink/bin/journal_get.sh")
app.logger.debug("finish clipboard download")
os.system("/Users/idm/.virtualenvs/greenthink/bin/journal_delete.sh")
app.logger.debug("clear clipboard")

app.logger.debug("start rotating journal")

journal_path = "/Users/idm/Library/Journal"
export_path = os.path.join(journal_path, "auto")
backup_path = os.path.join(journal_path, "backup")

http_file = os.path.join(journal_path, 'http/latest.txt')
live_file = os.path.join(journal_path, 'journal.txt')

now = datetime.datetime.utcnow()
datestamp = "%s-%s-%s.txt" % (now.year, now.month, now.day)

os.system("cp %s %s/%s" % (live_file, backup_path, datestamp))

j = GT.journal.Journal(export_path)
j.parse(live_file)
j.parse(http_file)

exported = j.export_week_old()
if exported:
    j.purge_week_old(live_file)

app.logger.debug("finish rotating journal")
