import re, json, datetime, os, shutil
from collections import defaultdict

re_day = re.compile(r'^(\d\d\d\d-\d\d-\d\d)$')
re_time = re.compile(r'^(\d\d\d\d)$')
re_time_tag = re.compile(r'^(\d\d\d\d)\s(\w+)$')
re_newlines = re.compile(r'\n\n\n', re.MULTILINE)

class Journal(object):
    def __init__(self, export_path):
        from Gthnk import app
        self.app = app
        self.export_path = export_path
        self.entries = defaultdict(lambda : defaultdict(str))

    def parse(self, journal_filename):
        with open(journal_filename) as f:
            contents = f.read()

        current_day = None
        current_time = None

        for line in contents.splitlines():
            line = line.rstrip()

            match_day = re_day.match(line)
            match_time = re_time.match(line)
            match_time_tag = re_time_tag.match(line)
            tag = ""

            if match_day:
                current_day = match_day.group(1)
                current_time = None
            elif not current_day and line == '':
                # skip blank lines before the first date stamp
                continue
            elif not current_time and line == '':
                continue
            elif current_time and line == '' and current_time not in self.entries[current_day]:
                # skip blank lines at the beginning of an entry
                continue
            elif match_time:
                if current_time and int(current_time[:4]) < int(match_time.group(1)):
                    self.app.logger.warning("times appear to be out of order")
                current_time = match_time.group(1)
            elif match_time_tag:
                current_time = match_time_tag.group(1)
                tag = match_time_tag.group(2)
                current_time = "%s %s" % (current_time, tag)
            else:
                self.entries[current_day][current_time] += "%s\n" % line

        for day in self.entries:
            for timestamp in self.entries[day]:
                self.entries[day][timestamp] = self.entries[day][timestamp].rstrip()

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

