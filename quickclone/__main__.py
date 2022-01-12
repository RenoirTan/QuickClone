import argparse
import typing as t
import sys

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
    args = app.parse_args()
    if args.show_version:
        print(f"{NAME} v{VERSION}")
        return 0
    return 0


sys.exit(main(sys.argv))
