from gthnk.filetree.buffer import FileBuffer


def test_timestamp_ordering(cwd, journal):
    "timestamps are not in the correct order; should warn about this"
    FileBuffer(f"{cwd}/data/out_of_order_times.txt", journal=journal).read()
    assert len(journal.days) == 1
    assert len(journal.days["2012-10-04"].entries) == 4

def test_merge(cwd, journal, correct_merge):
    "combine two files with interwoven timestamps"
    FileBuffer(f"{cwd}/data/source_a.txt", journal=journal).read()
    FileBuffer(f"{cwd}/data/source_b.txt", journal=journal).read()
    a_day = journal.days["2012-10-04"]
    assert str(a_day) == correct_merge

def test_newlines(cwd, journal, correct_output):
    "see if a whole horde of weird newlines screws anything up"
    FileBuffer(f"{cwd}/data/excessive_newlines.txt", journal=journal).read()
    a_day = journal.days["2012-10-04"]
    assert str(a_day) == correct_output

def test_twodays(cwd, journal, correct_twodays):
    "ensure journals with several days in them continue to work"
    FileBuffer(f"{cwd}/data/two_days_input.txt", journal=journal).read()
    assert len(journal.days) == 4

    # now concatenate some days and verify that it matches
    buf = str(journal.days["2012-10-04"]) + \
        str(journal.days["2012-10-05"]) + \
        str(journal.days["2012-10-06"]) + \
        str(journal.days["2012-10-07"])
    assert buf == correct_twodays
