import shutil
import warnings

import pytest

from quickclone.config.configurator import SmartConfigurator
from quickclone.delegation.errors import InvalidVcsError
from quickclone.delegation.tasks import create_clone_command
from quickclone.remote.locators import DirtyLocator, UniformResourceLocator


def test_create_gitclonecommand_dirty():
    git_where = shutil.which("git")
    if git_where is None:
        warnings.warn(Warning("git not found in path"))
        return
    configs = SmartConfigurator({})
    url = UniformResourceLocator.from_user_and_defaults(
        DirtyLocator.process_dirty_url("RenoirTan/QuickClone.git"),
        configs.to_locator_builder()
    )
    gcc = create_clone_command(
        vcs="git",
        configs=configs,
        built_url=url,
        dest_path="/tmp/somewhere",
        cla_list=[],
        cla_dict={},
        ignored=set()
    )
    assert gcc.format_command_list() == [
        git_where,
        "clone",
        "https://github.com/RenoirTan/QuickClone.git",
        "/tmp/somewhere"
    ]


def test_create_mercurialclonecommand_dirty():
    hg_where = shutil.which("hg")
    if hg_where is None:
        warnings.warn(Warning("hg not found in path"))
        return
    configs = SmartConfigurator({})
    url = UniformResourceLocator.process_url("https://gmplib.org/repo/gmp/")
    mcc = create_clone_command(
        vcs="hg",
        configs=configs,
        built_url=url,
        dest_path="/tmp/somewhere",
        cla_list=[],
        cla_dict={},
        ignored=set()
    )
    assert mcc.format_command_list() == [
        hg_where,
        "clone",
        "https://gmplib.org/repo/gmp/",
        "/tmp/somewhere"
    ]


def test_create_mercurialclonecommand_nicknames():
    hg_where = shutil.which("hg")
    if hg_where is None:
        warnings.warn(Warning("hg not found in path"))
        return
    configs = SmartConfigurator({})
    url = UniformResourceLocator.process_url("https://gmplib.org/repo/gmp/")
    other_args = {
        "configs": configs,
        "built_url": url,
        "dest_path": "/tmp/somewhere",
        "cla_list": None,
        "cla_dict": None,
        "ignored": None
    }
    hgcc = create_clone_command(vcs="hg", **other_args)
    mercc = create_clone_command(vcs="mercurial", **other_args)
    assert hgcc.format_command_list() == mercc.format_command_list()
