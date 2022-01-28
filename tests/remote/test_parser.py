import re

from quickclone.remote.parser import extract_groups


def test_extract_groups():
    regex_string = r"^((?P<a>\w)|(?P<b>\d))$"
    input_string = "a"
    matches = re.search(regex_string, input_string)
    groups = extract_groups(matches, ["character"], combine={"character": ["a", "b"]})
    assert groups["character"] == "a"
