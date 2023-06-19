import re
from collections import defaultdict


re_day = re.compile(r'^(\d\d\d\d-\d\d-\d\d)\s*$')
re_time = re.compile(r'^(\d\d\d\d)\s*$')
re_time_tag = re.compile(r'^(\d\d\d\d)\s(\w+)\s*$')
re_newlines = re.compile(r'\n\n\n', re.MULTILINE)


def parse_text(raw_text):
    """
    parse a Journal-encoded text string; add content to an Entries dictionary, with timestamp.
    """
    entries = defaultdict(lambda: defaultdict(str))

    current_day = None
    current_time = None

    for line in raw_text.splitlines():
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
        elif current_time and line == '' and current_time not in entries[current_day]:
            # skip blank lines at the beginning of an entry
            continue
        elif match_time:
            #if current_time and int(current_time[:4]) < int(match_time.group(1)):
            #    self.app.logger.warning("times appear to be out of order")
            current_time = match_time.group(1)
        elif match_time_tag:
            current_time = match_time_tag.group(1)
            tag = match_time_tag.group(2)
            #current_time = "%s %s" % (current_time, tag)
        else:
            entries[current_day][current_time] += "{0}\n".format(line)

    for day in entries:
        for timestamp in entries[day]:
            entries[day][timestamp] = entries[day][timestamp].rstrip()
    
    return entries
