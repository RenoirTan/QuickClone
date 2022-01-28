from quickclone.remote import UniformResourceLocator, remote_to_string


def test_remotetostring_https():
    url = UniformResourceLocator.process_url("https://github.com/RenoirTan/QuickClone.git")
    assert remote_to_string(url, "") == "https://github.com/RenoirTan/QuickClone.git"


def test_remotetostring_ssh():
    url = UniformResourceLocator.process_url("ssh://git@github.com/RenoirTan/QuickClone.git")
    assert remote_to_string(url, "") == "ssh://git@github.com/RenoirTan/QuickClone.git"


def test_remotetostring_scpgit():
    url = UniformResourceLocator.process_url("ssh://git@github.com/RenoirTan/QuickClone.git")
    url.kwargs["explicit_scp"] = True
    assert remote_to_string(url, "git") == "git@github.com:RenoirTan/QuickClone.git"
