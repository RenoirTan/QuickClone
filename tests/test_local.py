from quickclone.local import make_path


def test_makepath_empty():
    assert make_path("") == ""


def test_makepath_nonempty():
    assert make_path("/path") == "/path"


def test_makepath_suffixed():
    assert make_path("/path.git") == "/path"
