from __future__ import annotations
import re
import typing as t


# Taken from validators.domain.pattern
DOMAIN_REGEX_RAW: str = (
    r"(?:[a-zA-Z0-9]"  # First character of the domain
    r"(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)"  # Sub domain + hostname
    r"+[A-Za-z0-9][A-Za-z0-9-_]{0,61}"  # First 61 characters of the gTLD
    r"[A-Za-z]"  # Last character of the gTLD
)

# Taken from https://ihateregex.io/expr/ip/
IPV4_REGEX_RAW: str = (
    r"(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
)

# Taken from https://stackoverflow.com/a/17871737
IPV6_REGEX_RAW: str = (
    r"("
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


HOST_REGEX_RAW: str = f"({DOMAIN_REGEX_RAW}|{IPV4_REGEX_RAW}|{IPV6_REGEX_RAW})"


#                           Normal ASCII|Percent-encoding|Sub-delims
USERNAME_REGEX_RAW: str = r"([0-9a-zA-Z]|%[0-9a-fA-F]{2}|[!\$&'\(\)\*\+\,\;\=])+"
PASSWORD_REGEX_RAW: str = r"([0-9a-zA-Z:]|%[0-9a-fA-F]{2})+"


USERINFO_REGEX_RAW: str = f"{USERNAME_REGEX_RAW}(:{PASSWORD_REGEX_RAW})?"


AUTHORITY_REGEX_RAW: str = f"({USERINFO_REGEX_RAW}@)?({HOST_REGEX_RAW})"


def parse_authority(authority: str) -> t.Dict[str, str]:
    pass
