# coding=utf-8
from py.path import local
import pytest


@pytest.fixture
def fileutf8(tmpdir):
    #text = u"Jan Vlčinský".encode("utf-8")
    text = u"Jan Vlčinský"
    print text
    fname = tmpdir / "fileutf8.txt"
    with fname.open("w") as f:
        f.write(text)
    assert fname.exists()
    return fileutf8


def test_it(fileutf8):
    cat = local.sysfind("cat")
    cat.sysexec(fileutf8.strpath)
