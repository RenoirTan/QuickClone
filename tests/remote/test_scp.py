from quickclone.remote.scp import ScpLocator


LOCATOR = "git@github.com:RenoirTan/QuickClone.git"
PARTS = {
    "username": "git",
    "host": "github.com",
    "path": "RenoirTan/QuickClone.git"
}


def test_scplocator_from_parts():
    scp = ScpLocator(**PARTS)
    assert str(scp) == LOCATOR
