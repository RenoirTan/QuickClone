import pytest

from quickclone.remote.locators import DirtyLocator, UniformResourceLocator, UrlAuthority, FIELDS


TEST_URL = "https://username:password@example.com:443/path/to/resource?a=1&b=2#fragment"
PARTS = {
    "scheme": "https",
    "username": "username",
    "password": "password",
    "host": "example.com",
    "port": "443",
    "path": "path/to/resource",
    "query": "a=1&b=2",
    "fragment": "fragment"
}


DIRTY_URL = "RenoirTan/QuickClone.git"
DIRTY_PARTS = {"path": "RenoirTan/QuickClone.git"}


def test_uniformresourcelocator_from_parts():
    url = UniformResourceLocator(**PARTS)
    assert str(url) == TEST_URL


def test_uniformresourcelocator_parse():
    url = UniformResourceLocator.process_url(TEST_URL)
    dicted = dict(url)
    assert {field: dicted[field] for field in FIELDS} == PARTS


def test_uniformresourcelocator_faults_passwordnousername():
    parts = PARTS.copy()
    del parts["username"]
    url = UniformResourceLocator(**parts)
    assert not url.validate()


def test_uniformresourcelocator_faults_noscheme():
    parts = PARTS.copy()
    del parts["scheme"]
    url = UniformResourceLocator(**parts)
    assert not url.validate()


def test_uniformresourcelocator_faults_nohost():
    parts = PARTS.copy()
    del parts["host"]
    url = UniformResourceLocator(**parts)
    assert not url.validate()


def test_dirtylocator_from_parts():
    url = DirtyLocator(**DIRTY_PARTS)
    assert str(url) == f"/{DIRTY_URL}"


def test_dirtylocator_parse():
    url = DirtyLocator.process_dirty_url(DIRTY_URL)
    assert url.get_path() == DIRTY_URL


def test_urlauthority_parse():
    url = UrlAuthority.process_authority("username:password@example.com")
    assert url.username == "username"
    assert url.password == "password"
    assert url.host == "example.com"


def test_urlauthority_passwordnousername():
    with pytest.raises(Exception):
        UrlAuthority.process_authority(":password@github.com")
