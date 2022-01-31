import shutil

from quickclone.delegation.vcs.mercurial import MercurialCloneCommand


REMOTE = "https://gmplib.org/repo/gmp/"
DEST_PATH = "/tmp/somewhere"


def test_mercurialclonecommand():
    hg_where = shutil.which("hg")
    if hg_where is None:
        return
    mcc = MercurialCloneCommand(REMOTE, DEST_PATH)
    assert mcc.format_command_list() == [hg_where, "clone", REMOTE, DEST_PATH]


def test_mercurialclonecommand_nodestpath():
    hg_where = shutil.which("hg")
    if hg_where is None:
        return
    mcc = MercurialCloneCommand(REMOTE, "")
    assert mcc.format_command_list() == [hg_where, "clone", REMOTE]
