import pytest

from gthnk.model.journal import Journal


@pytest.fixture()
def journal():
    return Journal()
