import argparse
import typing as t
import sys

from quickclone import DESCRIPTION, NAME, VERSION
from quickclone.remote import DirtyLocator, LocatorBuilder, UniformResourceLocator, UrlAuthority


def program():
    sys.exit(main(sys.argv))


def create_argument_parser() -> argparse.ArgumentParser:
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
    return app


def main(argv: t.List[str]) -> int:
    app = create_argument_parser()
    args = app.parse_args(argv[1:])
    if args.show_version:
        print(f"{NAME} v{VERSION}")
        return 0
    if len(args.tests) > 0:
        successes, test_count = conduct_tests(args.tests, args.remote_url)
        if successes < test_count:
            print("Not all tests succeeded")
            return 1
        else:
            return 0
    else:
        dirty = DirtyLocator.process_dirty_url(args.remote_url)
        builder = LocatorBuilder()
        try:
            final_url = UniformResourceLocator.from_user_and_defaults(dirty, builder)
            print(f"Final URL: {str(final_url)}")
        except Exception as e:
            print(f"Error occurred:\n{e}")
            return 1
        else:
            return 0


def conduct_tests(tests: t.List[str], remote_url: str) -> t.Tuple[int, int]:
    success_counts: int = 0
    for test in tests:
        try:
            if test == "parse_authority":
                authority = UrlAuthority.process_authority(remote_url)
                print(authority)
                success_counts += 1
            elif test == "parse_full_url":
                url = UniformResourceLocator.process_url(remote_url)
                print(url)
                success_counts += 1
            elif test == "parse_dirty_url":
                dirty_url = DirtyLocator.process_dirty_url(remote_url)
                print(dirty_url)
                success_counts += 1
            else:
                print(f"Unrecognised test: {test}")
        except:
            pass
    return success_counts, len(tests)


if __name__ == "__main__":
    program()
