from __future__ import annotations
import re
import typing as t
from urllib.parse import urlparse, urlunparse, ParseResult

import validators

from . import parser


class LocatorBuilder(object):
    """
    A builder which stores user/program specified defaults to generate valid
    URLs from user inputs.

    Parameters
    ----------
    self: LocatorBuilder
        The LocatorBuilder object to be initialised.

    scheme: str = ""
        The scheme used to access the remote repository.
        Comes before everything else in a URL and is suffixed by '://'.
        Examples: https, ssh

    host: str = ""
        The host where the remote repository is located.
        Examples: github.com, 1.1.1.1

    username: str = ""
        The username used to access the remote repository.
        Comes before the host and is separated from the latter by '@'.
        Examples: git (in git@github.com)

    password: str = ""
        Password of the user used to authenticate themselves.
        If present, must come after a username (separated by ':') and before
        a host name (separated by '@').
        RFC 3986 recommends that you don't ever use this because it's a huge
        security vulnerability.
        However, this is still used by github when you use HTTPS.

    path: str = ""
        The path to the remote repository
        (not referring to where the local clone is located).
        Comes after the host and separated from it by '/'.
        Examples: RenoirTan/QuickClone
        (in https://github.com/RenoirTan/QuickClone)

    query: str = ""
        The parameters in the URL.
        Comes after the path or host and the start of the query section is
        denoted by '?'.
        You can chain multiple key-value pairs using '&' as the separator.
        Examples: key=value (in https://example.com?key=value)

    fragment: str = ""
        The fragment identifying a secondary resource.
        The last part of the URL. The fragment section is denoted by '#'.
        Examples: History
        (in https://en.wikipedia.org/wiki/Python_(programming_language)#History)
    """

    DEFAULT_SCHEME: str = "https"
    """
    The default scheme used to access the remote repository. By default this is "https".
    """

    DEFAULT_HOST: str = "github.com"
    """
    The default host where the remote repository is located. By default this is "github.com".
    """

    def __init__(
        self,
        scheme: str = "",
        host: str = "",
        username: str = "",
        password: str = "",
        path: str = "",
        query: str = "",
        fragment: str = ""
    ) -> None:
        self.scheme = scheme
        self.host = host
        self.username = username
        self.password = password
        self.path = path
        self.query = query
        self.fragment = fragment

    def get_scheme(self) -> str:
        """Get the scheme used to access the remote repository."""
        return self.DEFAULT_SCHEME if self.scheme is None else self.scheme

    def get_host(self) -> str:
        """Get the host name of the website hosting the remote repository."""
        return self.DEFAULT_HOST if self.host is None else self.host

    def get_username(self) -> str:
        """Get the username used to access the remote repository."""
        return self.username

    def get_password(self) -> str:
        """Get the password used to access the remote repository."""
        return self.password

    def get_path(self) -> str:
        """Get the path of the remote repository (in the website)."""
        return self.path

    def get_query(self) -> str:
        """Get the parameters (as a single string)."""
        return self.query

    def get_fragment(self) -> str:
        """Get the fragment."""
        return self.fragment

    def process_input(self, input: str) -> str:
        """
        Process an input URL so that it has a scheme,
        meaning that the authority (host, username and password) do not
        end up under path.

        Parameters
        ----------
        self: LocatorBuilder
            A LocatorBuilder object, from which this method borrows the scheme
            used to supplement the input URL.

        input: str
            The input URL.
        """
        raw_parse_result = urlparse(input)
        if raw_parse_result.scheme == "":
            raw_parse_result.scheme = self.get_scheme()
        return urlunparse(raw_parse_result)


class UrlAuthority(object):
    """
    The authority component in a URL. This includes the host name, username
    and password in the URL. Example: username:password@example.com.

    Parameters
    ----------
    self: UrlAuthority
        The UrlAuthority object to be initialised.

    host: str
        The host name of the URL.

    username: str = ""
        The username in the URL.

    password: str = ""
        The password in the URL.
    """

    def __init__(
        self,
        host: str,
        username: str = "",
        password: str = ""
    ) -> None:
        self.host = host
        self.username = username
        self.password = password

    @classmethod
    def process_authority(cls, authority: str) -> UrlAuthority:
        """
        Convert an authority (as a string) into a `UrlAuthority` object.
        `authority` can be taking from the `urllib.parse.ParseResult.netloc`
        attribute from the parsed URL as the source.
        Although `urllib.parse.ParseResult` has its own `hostname`, `username`
        and `password` methods, it cannot handle invalid numbers of ':' and
        '&' and treats every netloc as valid.

        Parameters
        ----------
        cls: typing.Type[UrlAuthority]
            The UrlAuthority class.

        authority: str
            The authority section in the URL. This can be obtained from the
            `netloc` attribute from a `urllib.parse.ParseResult` object which
            is the return value from `urllib.parse.urlparse`.

        Returns
        -------
        UrlAuthority
        """

        colon_index = authority.find(":")
        colon_rindex = authority.rfind(":")
        if colon_index != colon_rindex:
            raise ValueError("Multiple ':' found in {authority}")

        at_index = authority.find("@")
        at_rindex = authority.rfind("@")
        if at_index != at_rindex:
            raise ValueError("Multiple '@' found in {authority}")

        if colon_index != -1 and at_index == -1:
            username = authority[:colon_index]
            hostname = authority[colon_index+1:]
            raise ValueError(
                f"Invalid syntax: {username}:{hostname}. Suggestion: {username}@{hostname}"
            )

        if at_index == -1:
            hostname = authority
            username, password = "", ""
        else:
            hostname = authority[at_index+1]
            if colon_index == -1:
                username = authority[:at_index]
                password = ""
            else:
                username = authority[:colon_index]
                password = authority[colon_index+1:at_index]
        return cls(hostname, username, password)


def process_url_for_tentative_authority(url_parse_result: ParseResult) -> ParseResult:
    """
    Find the authority in a parsed URL and return a new parsed URL with the
    expected authority. If there is an authority in the parsed URL, a copy of
    the parsed URL is returned.

    Parameters
    ----------
    url_parse_result: urllib.parse.ParseResult
        The parsed URL created by `urllib.parse.urlparse`.

    Returns
    -------
    urllib.parse.ParseResult
    """
    return_value = ParseResult(**url_parse_result._asdict())
    if url_parse_result.netloc == "":
        path_parts = url_parse_result.path.split("/")
        return_value.netloc = path_parts[0]
        return_value.path = "/".join(path_parts[1:])
    return return_value

