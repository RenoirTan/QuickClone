import shutil

from quickclone.delegation.vcs.git import GitCloneCommand


REMOTE = "https://github.com/RenoirTan/QuickClone/.git"
DEST_PATH = "/tmp/somewhere"


def test_gitclonecommand_1():
    git_where = shutil.which("git")
    if git_where is None:
        return
    gcc = GitCloneCommand(REMOTE, DEST_PATH)
    assert gcc.format_command_list() == [git_where, "clone", REMOTE, DEST_PATH]


def test_gitclonecommand_2():
    git_where = shutil.which("git")
    if git_where is None:
        return
    gcc = GitCloneCommand(REMOTE, "")
    assert gcc.format_command_list() == [git_where, "clone", REMOTE]
