# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.diamond.utils.mixins import CRUDMixin
from flask.ext.diamond.models import User
from Gthnk import db, security

class Journal(object):
    """
    a Day is a collection of Entry objects from a single day.
    This is sortof a virtual object...  but it might become a real object.
    """
    def __init__(self):
        pass

    def dump(self):
        buf = ""
        for day in sorted(self.entries.keys()):
            buf += self.dump_day(day)
        return buf

    def dump_day(self, day):
        buf = "%s" % day
        for timestamp in sorted(self.entries[day].keys()):
            buf += "\n\n%s\n\n" % timestamp
            buf += self.entries[day][timestamp]
        buf += "\n"
        return buf

    def export_day(self, day):
        """
        export a file, named after the date it contains, in the export path
        """
        out_file = os.path.join(self.export_path, "%s.txt" % day)
        with open(out_file, 'w') as f:
            f.write(self.dump_day(day))

    def export_week_old(self):
        """
        export all of the entries that are more than one week old
        """
        exported = 0
        week_ago = datetime.date.today() - datetime.timedelta(days=8)

        for day in sorted(self.entries.keys()):
            date = datetime.datetime.strptime(day, '%Y-%m-%d').date()
            if week_ago > date:
                # export it
                self.export_day(day)
                exported += 1
        return exported

    def list_recent_days(self, num_days):
        """
        get a list of timestamps pertaining to [num_days] recent days
        """
        included = []
        week_ago = datetime.date.today() - datetime.timedelta(days=num_days)
        for day in sorted(self.entries.keys()):
            date = datetime.datetime.strptime(day, '%Y-%m-%d').date()
            if week_ago <= date:
                included.append(day)
        return included

    def get_recent_days(self, num_days):
        """
        retrieve the text from [num_days] recent days
        """
        buf = ""
        week_ago = datetime.date.today() - datetime.timedelta(days=num_days)
        for day in sorted(self.entries.keys()):
            date = datetime.datetime.strptime(day, '%Y-%m-%d').date()
            if week_ago <= date:
                if buf == "":
                    buf += self.dump_day(day)
                else:
                    buf += "\n" + self.dump_day(day)
        return buf

    def purge_week_old(self, journal_filename):
        """
        remove the entries that are more than a week old (which presumably have been exported already)
        """
        retained = self.get_recent_days(num_days=8)
        retained_list = self.list_recent_days(num_days=8)
        with open(journal_filename, 'w') as f:
            f.write(retained)
        message = "journal rotate: pruned %s, retained: %s" % (journal_filename, retained_list)
        self.app.logger.debug(message)

    def get_tag(self, tagname):
        results = []
        for day in self.entries:
            for timestamp in self.entries[day]:
                match_time_tag = re_time_tag.match(timestamp)
                if match_time_tag and match_time_tag.group(2) == tagname:
                    results.append(self.entries[day][timestamp])
        return results

