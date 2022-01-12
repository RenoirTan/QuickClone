from __future__ import annotations
import re
import typing as t
from urllib.parse import urlparse, urlunparse, ParseResult

import validators


class LocatorBuilder(object):
    DEFAULT_SCHEME: str = "https"
    DEFAULT_HOST: str = "github.com"

    def __init__(
        self,
        scheme: t.Optional[str],
        host: t.Optional[str],
        username: t.Optional[str],
        password: t.Optional[str],
        path: t.Optional[str],
        query: t.Optional[str],
        fragment: t.Optional[str]
    ) -> None:
        self.scheme = scheme
        self.host = host
        self.username = username
        self.password = password
        self.path = path
        self.query = query
        self.fragment = fragment

    def get_scheme(self) -> str:
        return self.DEFAULT_SCHEME if self.scheme is None else self.scheme

    def get_host(self) -> str:
        return self.DEFAULT_HOST if self.host is None else self.host

    def get_username(self) -> t.Optional[str]:
        return self.username

    def get_password(self) -> t.Optional[str]:
        return self.password

    def get_path(self) -> t.Optional[str]:
        return self.path

    def get_query(self) -> t.Optional[str]:
        return self.query

    def get_fragment(self) -> t.Optional[str]:
        return self.fragment

    def process_input(input: str) -> str:
        raw_parse_result = urlparse(input)
        if raw_parse_result.scheme == "":
            raw_parse_result.scheme = self.get_scheme()
        return urlunparse(raw_parse_result)


class UrlAuthority(object):
    def __init__(
        self,
        host: str,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None
    ) -> None:
        pass

    @classmethod
    def process_url_parse_result(cls, url_parse_result: ParseResult) -> UrlAuthority:
        processed_url = process_url_for_tentative_authority(url_parse_result)
        authority = processed_url.netloc
        colon_index = authority.find(":")
        at_index = authority.find("@")
        if colon_index != -1 and at_index == -1:
            username = authority[:colon_index]
            hostname = authority[colon_index+1:]
            raise ValueError(
                f"Invalid syntax: {username}:{hostname}. Suggestion: {username}@{hostname}"
            )
        if at_index == -1:
            hostname = authority
            username, password = None, None
        else:
            hostname = authority[at_index+1]
            if colon_index == -1:
                username = authority[:at_index]
                password = None
            else:
                username = authority[:colon_index]
                password = authority[colon_index+1:at_index]
        return cls(hostname, username, password)


def process_url_for_tentative_authority(url_parse_result: ParseResult) -> ParseResult:
    return_value = ParseResult(**url_parse_result._asdict())
    if url_parse_result.netloc == "":
        path_parts = url_parse_result.path.split("/")
        return_value.netloc = path_parts[0]
        return_value.path = "/".join(path_parts[1:])
    return return_value

