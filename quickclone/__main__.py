import argparse
import typing as t
import sys

import quickclone
from quickclone import DESCRIPTION, NAME, VERSION


def main(argv: t.List[str]) -> int:
    app = argparse.ArgumentParser(description=f"{NAME} v{VERSION}: {DESCRIPTION}")
    app.add_argument(
        "--version",
        "-v",
        dest="show_version",
        help="display the version number and exit",
        action="store_const",
        const=True,
        default=False
    )
    app.add_argument(
        "remote_url",
        metavar="REMOTE_URL",
        nargs="?",
        type=str,
        help="the url of the remote to be cloned"
    )
    app.add_argument(
        "--test",
        "-T",
        dest="tests",
        metavar="TEST",
        action="append",
        required=False,
        default=[],
        help="which tests to conduct: parse_authority, parse_full_url"
    )
    args = app.parse_args()
    if args.show_version:
        print(f"{NAME} v{VERSION}")
        return 0
    print(args.remote_url)
    print(args.tests)
    conduct_tests(args.tests, args.remote_url)
    return 0


def conduct_tests(tests: t.List[str], remote_url: str) -> int:
    success_counts: int = 0
    for test in tests:
        if test == "parse_authority":
            print(quickclone.remote.parser.parse_authority(remote_url))
            success_counts += 1
        elif test == "parse_full_url":
            print(quickclone.remote.parser.parse_full_url(remote_url))
            success_counts += 1
        elif test == "parse_dirty_url":
            print(quickclone.remote.parser.parse_dirty_url(remote_url))
            success_counts += 1
        else:
            print(f"Unrecognised test: {test}")
    return success_counts


sys.exit(main(sys.argv))
