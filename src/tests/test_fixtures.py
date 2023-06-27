def test_journal_obj(journal):
    assert journal is not None

def test_gthnk_obj(gthnk):
    assert gthnk is not None
    assert gthnk.config["INPUT_FILES"] == "/tmp/gthnk/journal.txt"
    assert gthnk.journal is not None
