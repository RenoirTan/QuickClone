from __future__ import annotations
import re
import typing as t


def extract_groups(matches: re.Match, names: t.Iterable[str]) -> t.Dict[str, t.Optional[str]]:
    """
    Extract named groups from a `re.Match` object to a dictionary.
    These named groups are delimited by `(?P<name>)`.
    
    Parameters
    ----------
    matches: re.Match
        The matches created by `re.search`.
    
    names: Iterable[str]
        A list of named groups found in the regex string.
    
    Returns
    -------
    Dict[str, Optional[str]]
        A dictionary of named groups and their associated values.
    """
    result = {}
    for name in names:
        try:
            result[name] = matches.group(name)
        except IndexError:
            result[name] = None
    return result


UNRESERVED: str = r"[0-9a-zA-Z._~\-]"
PERCENT_ENCODED: str = r"%[0-9a-fA-F]{2}"
SUB_DELIMS: str = r"[!\$&'\(\)\*\+\,\;\=]"
CHAR: str = f"{UNRESERVED}|{PERCENT_ENCODED}|{SUB_DELIMS}"


# Taken from validators.domain.pattern
DOMAIN_REGEX_RAW: str = (
    r"(?P<domain>"
    r"(?:[a-zA-Z0-9]"  # First character of the domain
    r"(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)+"  # Sub domain + hostname
    r"[A-Za-z0-9][A-Za-z0-9-_]{0,61}"  # First 61 characters of the gTLD
    r"[A-Za-z]"  # Last character of the gTLD
    r")"
)

# Taken from https://ihateregex.io/expr/ip/
IPV4_REGEX_RAW: str = (
    r"(?P<ipv4>"
    r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}"
    r")"
)

# Taken from https://stackoverflow.com/a/17871737
IPV6_REGEX_RAW: str = (
    r"(?P<ipv6>"
    r"([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|"          # 1:2:3:4:5:6:7:8
    r"([0-9a-fA-F]{1,4}:){1,7}:|"                         # 1::                              1:2:3:4:5:6:7::
    r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|"         # 1::8             1:2:3:4:5:6::8  1:2:3:4:5:6::8
    r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|"  # 1::7:8           1:2:3:4:5::7:8  1:2:3:4:5::8
    r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|"  # 1::6:7:8         1:2:3:4::6:7:8  1:2:3:4::8
    r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|"  # 1::5:6:7:8       1:2:3::5:6:7:8  1:2:3::8
    r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|"  # 1::4:5:6:7:8     1:2::4:5:6:7:8  1:2::8
    r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|"       # 1::3:4:5:6:7:8   1::3:4:5:6:7:8  1::8  
    r":((:[0-9a-fA-F]{1,4}){1,7}|:)|"                     # ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8 ::8       ::     
    r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|"     # fe80::7:8%eth0   fe80::7:8%1     (link-local IPv6 addresses with zone index)
    r"::(ffff(:0{1,4}){0,1}:){0,1}"
    r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}"
    r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|"          # ::255.255.255.255   ::ffff:255.255.255.255  ::ffff:0:255.255.255.255  (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
    r"([0-9a-fA-F]{1,4}:){1,4}:"
    r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}"
    r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])"           # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
    r")"
)


HOST_REGEX_RAW: str = f"(?P<host>{DOMAIN_REGEX_RAW}|{IPV4_REGEX_RAW}|{IPV6_REGEX_RAW})"


USERNAME_REGEX_RAW: str = f"(?P<username>({CHAR})+)"
PASSWORD_REGEX_RAW: str = f"(?P<password>({CHAR}|[:])+)"


USERINFO_REGEX_RAW: str = f"{USERNAME_REGEX_RAW}(:{PASSWORD_REGEX_RAW})?"


# 0 to 65535
PORT_REGEX_RAW: str = (
    r"(?P<port>"
    r"(6553[0-5]|655[0-2]\d|65[0-4]\d\d|6[0-4]\d\d\d|[1-5]?\d\d\d\d|[1-9]\d{0,3}|[0-9])"
    r")"
)


AUTHORITY_REGEX_RAW: str = (
    r"(?P<authority>"
    f"({USERINFO_REGEX_RAW}@)?({HOST_REGEX_RAW})(:{PORT_REGEX_RAW})?"
    r")"
)
AUTHORITY_REGEX: re.Pattern[str] = re.compile(f"^{AUTHORITY_REGEX_RAW}$")


SCHEME_REGEX_RAW: str = r"(?P<scheme>[a-zA-Z][a-zA-Z0-9+.-]*)"
PATH_REGEX_RAW: str = (
    r"(?P<path>"
    f"(({CHAR}|[@])+(/({CHAR}|[@])+)*)/?|/?"
    r")"
)
QUERY_REGEX_RAW: str = f"(?P<query>({CHAR}|[/\?])*)"
FRAGMENT_REGEX_RAW: str = f"(?P<fragment>({CHAR}|[/\?])*)"


FULL_URL_REGEX_RAW: str = (
    r"(?P<full_url>"
    f"{SCHEME_REGEX_RAW}://{AUTHORITY_REGEX_RAW}(/{PATH_REGEX_RAW})?(\?{QUERY_REGEX_RAW})?(#{FRAGMENT_REGEX_RAW})?"
    r")"
)
FULL_URL_REGEX: re.Pattern[str] = re.compile(f"^{FULL_URL_REGEX_RAW}$")


def parse_authority(authority: str) -> t.Dict[str, t.Optional[str]]:
    """
    Parse the authority segment in a URL and split it into its consituent parts.
    
    Parameters
    ----------
    authority: str
        The authority segment in a URL.
    
    Returns
    -------
    Dict[str, Optional[str]]
        The parts of the authority segment.
    """
    matches = AUTHORITY_REGEX.search(authority)
    if matches is None:
        return {}
    return extract_groups(
        matches,
        ["authority", "domain", "ipv4", "ipv6", "username", "password", "port"]
    )


def parse_full_url(url: str) -> t.Dict[str, t.Optional[str]]:
    """
    Parse a full URL and split it into its constituent parts.
    
    Parameters
    ----------
    url: str
        The full URL.
    
    Returns
    -------
    Dict[str, Optional[str]]
        The parts of the URL.
    """
    matches = FULL_URL_REGEX.search(url)
    if matches is None:
        return {}
    return extract_groups(
        matches,
        [
            "full_url",
            "scheme",
            "authority",
            "domain",
            "ipv4",
            "ipv6",
            "username",
            "password",
            "port",
            "path",
            "query",
            "fragment"
        ]
    )
